# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import os
import pathlib
import time
from graphlib import TopologicalSorter

from tqdm.auto import tqdm

from pymbse.client.cache import PymbseCache, PymbseExec
from pymbse.client.config import (
    ModelSourceConfig,
    ModelSourceType,
    ModelStructure,
    PymbseConfig,
)
from pymbse.commons.schemas import (
    ExecutionJob,
    ModelExecutionReference,
    ModelReference,
    ModelSource,
)


class ExecutionError(RuntimeError):
    def __init__(self, *args, job: ExecutionJob, ref: ModelExecutionReference) -> None:
        super().__init__(*args)
        self.job = job
        self.ref = ref


class ModelSourceHandler:
    def __init__(self, source: ModelSourceConfig) -> None:
        self.source = source
        pass

    @staticmethod
    def create(source: ModelSourceConfig) -> "ModelSourceHandler":
        return ModelSourceHandler(source)


class PymbseManage:
    """Class to handle global actions with Pymbse
    - Storing and loading models from external sources
    - Creation of models
    - Synchorization with cache
    """

    def __init__(
        self,
        config: PymbseConfig,
    ) -> None:
        self.config = config
        self.cache = PymbseCache(config.config.cache_uri)
        self.exec = PymbseExec(config.config.exec_uri)
        self.model_cache_source = ModelSource(
            name="pymbse-cache",
            uri=config.config.cache_uri,
        )

    @staticmethod
    def create(config_path: str | os.PathLike) -> "PymbseManage":
        return PymbseManage(PymbseConfig.load_from_file(config_path))

    def setup_cache_models(self, model_structure: ModelStructure | None = None) -> None:
        if model_structure is None:
            model_structure = self.config.get_model_structure()
        for model in reversed(model_structure.execution_order):
            remote_model = self.cache.find_model(model)
            if remote_model:
                self.cache.delete_model(model)
        for model in model_structure.execution_order:
            local_model = self.config.to_cache_model(model)

            remote_model = self.cache.find_model(model)

            if remote_model is None:
                self.cache.create_model(local_model)
            elif remote_model != local_model:
                self.cache.replace_model(local_model)

    def clear_cache(self) -> None:
        self.cache.clear_all()

    def run_model_dependencies(
        self,
        model_reference: ModelReference,
        include_model: bool = False,
        force_all: bool = False,
    ) -> str:
        """Run all models for given dependency

        Create a ExecutionJob for all models in the structure which depend on the given model_reference,
        schedule models by dependencies and execute them.

        :param model_reference: model reference
        :type model_reference: ModelReference
        :param include_model: Also run (system,model) itself
        :type include_model: bool
        :param force_all: Force all executions (even if no input changed)
        :type force_all: bool
        :return: Execution reference
        :rtype: str
        """
        structure = self.config.get_model_structure().get_model_dependencies(
            model_reference, include_model
        )

        return self.run_models(structure, force_all)

    def run_models(self, structure: ModelStructure, force_all: bool = False) -> str:
        """Run all models for the given modelStructure

        Create a ExecutionJob for all models in the structure, schedule models by
        dependencies and execute them.

        :param structure: model structure
        :type structure: ModelStructure
        :param force_all: Force all executions (even if no input changed)
        :type force_all: bool
        :return: Execution reference
        :rtype: str
        """
        executions = self.cache.create_executions(structure.execution_order)
        execution_ref = executions[0].execution  # All have the same reference
        exec_dict = {
            modref: exec_ref
            for modref, exec_ref in zip(structure.execution_order, executions)
        }
        jobs = {}

        ts = TopologicalSorter(structure.dependency_graph)
        ts.prepare()
        active_jobs = ""
        with tqdm(total=len(structure.execution_order)) as pbar:
            while ts.is_active():
                for node in ts.get_ready():
                    _exec, output = self.init_upload_run(exec_dict[node], force_all)
                    if output.status == "SKIPPED":
                        tqdm.write(
                            f"Using existing exection for Model {node.system}.{node.model}"
                        )
                        pbar.update(1)
                        ts.done(node)
                    else:
                        jobs[node] = output
                active_jobs_new = ", ".join(
                    [f"{job.system}.{job.model}" for job in jobs]
                )
                if active_jobs_new != active_jobs:
                    active_jobs = active_jobs_new
                    pbar.set_description(f"Running models: {active_jobs}")

                wait_on_job = False
                finished_jobs = []
                for job in jobs:
                    if jobs[job].status == "SUCCESS":
                        self.cache.forward_outputs(exec_dict[job])
                        ts.done(job)
                        pbar.update(1)
                        tqdm.write(
                            f"Execution of Model {job.system}.{job.model} finished successfully"
                        )
                        finished_jobs.append(job)
                    elif jobs[job].status == "FAILURE":
                        tqdm.write(
                            f"Execution of Model {job.system}.{job.model} failed."
                        )
                        self.on_execution_error(jobs[job], exec_dict[job])
                    else:
                        jobs[job] = self.exec.get_status(jobs[job])
                        wait_on_job = True
                for job in finished_jobs:
                    del jobs[job]
                if wait_on_job:
                    time.sleep(1)

        return execution_ref

    def on_execution_error(self, job: ExecutionJob, reference: ModelExecutionReference):
        # Todo, print nice exception handling
        raise ExecutionError(f"Execution of {reference} failed", job=job, ref=reference)

    def init_upload_run(
        self, reference: ModelReference, force_execution: bool = False
    ) -> tuple[ModelExecutionReference, ExecutionJob]:
        if isinstance(reference, ModelExecutionReference):
            model_execution = reference
        else:
            model_execution = self.cache.create_execution(reference).get_reference()

        model_conf = self.config.get_model(reference)
        source = self.config.get_source(reference)
        if source.data_source == ModelSourceType.LOCAL:
            # upload from local file system
            source_top_path = pathlib.Path(source.source_url)
            model_path = source_top_path / reference.system / reference.model
            for inp_name, inp in model_conf.inputs.items():
                # References are pushed via cache automatically
                if not inp.reference:
                    if not inp.filename:
                        raise ValueError(
                            f"Input {inp_name} has neither reference nor filename"
                        )
                    file_path = model_path / inp.filename

                    self.cache.upload_input(model_execution, inp_name, file_path)

        elif source.data_source == ModelSourceType.CACHE:
            # All input files should be uploaded already, otherwise we don't know where to retreive them
            pass
        elif source.data_source == ModelSourceType.MMBSE:
            # Synchronize with MMBSE DB, load execution, upload to cache
            pass

        self.cache.lock_inputs(model_execution)
        # Check if need to be run
        exec_past = None
        if not force_execution:
            exec_past = self.cache.link_from_existing_exec(model_execution)
        if exec_past:
            return model_execution, ExecutionJob(
                id=exec_past.execution, status="SKIPPED"
            )
        else:
            exec_env = self.config.execution_environments[model_conf.exec_env]
            return model_execution, self.exec.execute_model(
                model_execution, exec_env, self.model_cache_source
            )

    def load_external_sources(self):
        pass

    def store_external_sources(self):
        pass
