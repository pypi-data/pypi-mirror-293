from typing import Callable, Optional, Dict, List, Any
import inspect
import json
import os

from kubernetes import client, config
from kubernetes.client import (
    V1Container,
    V1ContainerPort,
    V1EnvVar,
    V1EnvVarSource,
    V1Job,
    V1JobSpec,
    V1ObjectMeta,
    V1Pod,
    V1PodSpec,
    V1PodTemplateSpec,
    V1Secret,
    V1SecretKeySelector,
)
from kubernetes.client.exceptions import ApiException

from kubicle.runner.base import JobRunner, DEFAULT_OWNER_REF, InputType, OutputType
from kubicle.base import Job, JobStatus, JobRuntime
from kubicle.server.models import V1UserProfile
from kubicle.util import get_random_characters


class K8sJobRunner(JobRunner):
    """
    A Kubernetes job runner
    """

    def __init__(
        self,
        namespace: Optional[str] = None,
        owner_ref: V1UserProfile = DEFAULT_OWNER_REF,
        img: Optional[str] = None,
        envs: Dict[str, str] = {},
        include_env: List[str] = [],
    ) -> None:

        try:
            # Try to load in-cluster configuration
            config.load_incluster_config()
            print("Loaded in-cluster Kubernetes config.")
        except config.ConfigException:
            # Fallback to load kubeconfig (typically for local development)
            config.load_kube_config()
            print("Loaded kubeconfig (out-of-cluster config).")

        if not namespace:
            namespace = os.getenv("NAMESPACE")
            if not namespace:
                namespace = "default"

        self.namespace = namespace
        self.owner = owner_ref

        if not img:
            img = os.getenv("JOB_IMG")
        if not img:
            raise ValueError("`img` parameter or $JOB_IMG env var must be set")

        self.img = img
        self.envs = envs
        self.include_env = include_env

    def run(self, fn: Callable[[InputType], OutputType], input: InputType) -> Job:
        run_module = inspect.getmodule(fn).__name__  # type: ignore
        run_fn_name = fn.__name__

        print(f"RUN_MODULE: {run_module}")
        print(f"RUN_FN: {run_fn_name}")

        job_name = f"{run_fn_name}-{get_random_characters()}".lower()

        if not self.owner.email:
            raise Exception("Owner email is not set")
        job = Job(
            self.owner.email,
            JobStatus.PENDING,
            JobRuntime.K8s.value,
            job_name,
            namespace=self.namespace,
        )

        input_json: str = json.dumps(input.model_dump(), default=str)
        owner_json: str = json.dumps(self.owner.model_dump(), default=str)

        common_name = f"kjob-{run_fn_name}-{job.id}".lower()
        job.metadata["pod_name"] = common_name
        job.save()

        env_vars = gather_env_vars(self.include_env)
        env_vars.update(self.envs)
        env_vars["OWNER_JSON"] = owner_json
        env_vars["INPUT_JSON"] = input_json
        env_vars["JOB_ID"] = job.id

        db_host = os.getenv("DB_HOST") or os.getenv("KUBICLE_DB_HOST")
        if not db_host:
            raise ValueError("DB_HOST env var must be set")
        env_vars["DB_HOST"] = db_host

        db_name = os.getenv("DB_NAME") or os.getenv("KUBICLE_DB_NAME")
        if not db_name:
            raise ValueError("DB_NAME env var must be set")
        env_vars["DB_NAME"] = db_name

        db_user = os.getenv("DB_USER") or os.getenv("KUBICLE_DB_USER")
        if not db_user:
            raise ValueError("DB_USER env var must be set")
        env_vars["DB_USER"] = db_user

        db_password = os.getenv("DB_PASS") or os.getenv("KUBICLE_DB_PASS")
        if not db_password:
            raise ValueError("DB_PASS env var must be set")
        env_vars["DB_PASS"] = db_password

        db_type = os.getenv("DB_TYPE") or os.getenv("KUBICLE_DB_TYPE")
        if not db_type:
            raise ValueError("DB_TYPE env var must be set")
        env_vars["DB_TYPE"] = db_type

        create_secret_with_env_vars(
            secret_name=common_name,
            namespace=self.namespace,
            env_vars=env_vars,
        )
        env: List[V1EnvVar] = get_env_vars_from_secret(
            list(env_vars.keys()), common_name
        )
        env.append(V1EnvVar(name="JOB_ID", value=job.id))

        container_image_uri = get_container_image_uri()
        print("container image uri: ", container_image_uri)

        container: V1Container = V1Container(
            name="kubicle-job",
            image=container_image_uri,
            ports=[V1ContainerPort(container_port=8080)],
            env=env,
            command=[
                "poetry",
                "run",
                "python",
                "-m",
                "kubicle.runner.k8s.main",
            ],  # TODO: we need to make this configurable
        )

        job_labels = {
            "job_id": job.id,
            "job_name": job.name,
            "app": "kubicle",
        }
        template: V1PodTemplateSpec = V1PodTemplateSpec(
            metadata=V1ObjectMeta(labels=job_labels),
            spec=V1PodSpec(
                containers=[container],
                service_account_name="kubicle",
                restart_policy="Never",
            ),
        )

        job_spec: V1JobSpec = V1JobSpec(
            template=template, backoff_limit=0, ttl_seconds_after_finished=86400
        )
        v1job: V1Job = V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=V1ObjectMeta(name=common_name, labels=job_labels),
            spec=job_spec,
        )

        batch_v1 = client.BatchV1Api()
        v1job_result = batch_v1.create_namespaced_job(
            body=v1job,
            namespace=self.namespace,
        )

        update_secret_with_owner_reference(common_name, self.namespace, v1job_result)  # type: ignore

        return job


def get_container_image_uri():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    pod_name = os.getenv("HOSTNAME")
    namespace = os.getenv("NAMESPACE")
    pod: V1Pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)  # type: ignore
    for container in pod.spec.containers:  # type: ignore
        if container.name == "hub-api":
            return container.image

    raise SystemError("Could not find container image URI from current pod")


def create_secret_with_env_vars(
    secret_name: str, namespace: str, env_vars: Dict[str, str]
) -> V1Secret:
    config.load_incluster_config()
    api = client.CoreV1Api()

    secret = V1Secret(
        metadata=V1ObjectMeta(name=secret_name),
        type="Opaque",
        string_data=env_vars,
    )

    try:
        api_response = api.create_namespaced_secret(namespace=namespace, body=secret)
        print(f"Secret {secret_name} created in namespace {namespace}.")
    except ApiException as e:
        if e.status == 409:
            api_response = api.replace_namespaced_secret(
                name=secret_name, namespace=namespace, body=secret
            )
            print(f"Secret {secret_name} updated in namespace {namespace}.")
        else:
            raise
    return api_response  # type: ignore


def gather_env_vars(env_vars: List[str]) -> Dict[str, str]:
    return {var: os.getenv(var) for var in env_vars if os.getenv(var) is not None}  # type: ignore


def get_env_vars_from_secret(env_vars: List[str], secret_name: str) -> List[V1EnvVar]:
    env_var_secrets: List[V1EnvVar] = [
        V1EnvVar(
            name=env_name,
            value_from=V1EnvVarSource(
                secret_key_ref=V1SecretKeySelector(
                    name=secret_name,
                    key=env_name,
                )
            ),
        )
        for env_name in env_vars
    ]
    return env_var_secrets


def update_secret_with_owner_reference(secret_name: str, namespace: str, job: V1Job):
    config.load_incluster_config()
    api = client.CoreV1Api()

    secret = api.read_namespaced_secret(name=secret_name, namespace=namespace)

    owner_reference = client.V1OwnerReference(
        api_version=job.api_version,
        kind=job.kind,
        name=job.metadata.name,  # type: ignore
        uid=job.metadata.uid,  # type: ignore
        block_owner_deletion=True,
        controller=True,
    )

    secret.metadata.owner_references = [owner_reference]  # type: ignore

    try:
        api.replace_namespaced_secret(
            name=secret_name, namespace=namespace, body=secret
        )
        print(
            f"Secret {secret_name} updated with owner reference in namespace {namespace}."
        )
    except ApiException as e:
        raise
