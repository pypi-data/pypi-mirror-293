import logging
from typing import List, TypeVar

import mlopus
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.pipeline import Pipeline

from .input import PipelineInput
from .output import PipelineOutput

logger = logging.getLogger(__name__)

T = TypeVar("T")


class MlflowArtifacts(mlopus.mlflow.MlflowRunMixin, mlopus.kedro.HookWithFactory):
    """Hook to set up inputs and collect outputs using MLflow artifacts.

    For a fully commented example covering all settings that can be customized in this hook, have a look at:
    https://github.com/lariel-fernandes/mlopus/tree/main/examples/2_a_kedro_project/conf/full/parameters/hooks/mlflow_artifacts.yml
    """

    collect_on_error: bool = False
    inputs: List[PipelineInput] = []
    outputs: List[PipelineOutput] = []

    # =======================================================================================================
    # === Artifact handlers =================================================================================

    def _setup_inputs(self, pipeline_name: str):
        if inputs := [i for i in self.inputs if i.enabled and i.used_by(pipeline_name)]:
            logger.info("Setting up inputs for pipeline '%s'", pipeline_name)

        for i in inputs:
            lineage_arg = i.using(self.run_manager.mlflow_api).setup(default_run_id=self.run_manager.run.id)
            if i.log_lineage:
                mlopus.lineage.of(self.run_manager.run).with_input(lineage_arg).register()

    def _collect_outputs(self, pipeline_name: str):
        if outputs := [o for o in self.outputs if o.enabled and o.used_by(pipeline_name)]:
            logger.info("Collecting outputs of pipeline '%s'", pipeline_name)

        for o in outputs:
            lineage_arg = o.using(self.run_manager.mlflow_api).collect(default_run_id=self.run_manager.run.id)
            if o.log_lineage:
                mlopus.lineage.of(self.run_manager.run).with_output(lineage_arg).register()

    # =======================================================================================================
    # === Hook triggers =====================================================================================

    @hook_impl
    def before_pipeline_run(self, run_params: dict, pipeline: Pipeline, catalog: DataCatalog):  # noqa
        self._setup_inputs(run_params["pipeline_name"])

    @hook_impl
    def after_pipeline_run(self, run_params: dict, run_result: dict, pipeline: Pipeline, catalog: DataCatalog):  # noqa
        self._collect_outputs(run_params["pipeline_name"])

    @hook_impl
    def on_pipeline_error(self, error: Exception, run_params: dict, pipeline: Pipeline, catalog: DataCatalog):  # noqa
        if self.collect_on_error:
            self._collect_outputs(run_params["pipeline_name"])
