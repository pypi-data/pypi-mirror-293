from typing import Callable
from multiprocessing import Process
import time
import importlib
import inspect

from agentcore.models import V1UserProfile

from kubicle.base import Job, JobStatus, JobRuntime
from kubicle.runner.base import JobRunner, InputType, OutputType, DEFAULT_OWNER_REF
from kubicle.util import get_random_characters


def job_wrapper(module_name: str, function_name: str, input: InputType, job_id: str):  # type: ignore
    module = importlib.import_module(module_name)
    fn: Callable[[InputType], OutputType] = getattr(module, function_name)  # type: ignore

    jobs = Job.find(id=job_id)
    if not jobs:
        raise Exception(f"Job {job_id} not found")
    job = jobs[0]

    try:
        output = fn(input)
        job.status = JobStatus.FINISHED
        job.result = output.model_dump_json()
    except Exception as e:
        job.status = JobStatus.FAILED
        job.result = str(e)
    finally:
        job.finished = time.time()
        job.save()


class ProcessJobRunner(JobRunner):
    """
    Process job runner
    """

    def __init__(self, owner_ref: V1UserProfile = DEFAULT_OWNER_REF) -> None:
        self.owner = owner_ref
        print("ProcessJobRunner.init()", flush=True)

    def run(self, fn: Callable[[InputType], OutputType], input: InputType) -> Job:
        print("ProcessJobRunner.run()", flush=True)
        run_fn_name = fn.__name__
        run_module = inspect.getmodule(fn).__name__  # type: ignore

        print(f"RUN_MODULE: {run_module}", flush=True)
        print(f"RUN_FN: {run_fn_name}", flush=True)

        job_name = f"{run_fn_name}-{get_random_characters()}".lower().replace("_", "-")

        if not self.owner.email:
            raise Exception("Owner email is not set")

        job = Job(
            self.owner.email,
            JobStatus.RUNNING,
            JobRuntime.Process.value,
            job_name,
        )

        print("starting process...", flush=True)
        p = Process(target=job_wrapper, args=(run_module, run_fn_name, input, job.id))
        p.start()

        return job
