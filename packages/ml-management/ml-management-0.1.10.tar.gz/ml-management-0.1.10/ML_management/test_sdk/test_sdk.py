"""General testing of the sdk."""
import os
import unittest

import pandas

from ML_management.mlmanagement import set_server_url
from ML_management.sdk import sdk
from ML_management.sdk.parameters import (
    ArbitraryModels,
    DatasetLoaderMethodParams,
    ModelMethodParams,
    ModelVersionChoice,
    ModelWithRole,
    SingleDatasetLoader,
)
from ML_management.sdk.schema import ExecutionJob, ModelVersion

os.environ["kc_access"] = "kc_access"
os.environ["kc_state"] = "kc_state"

NAME = "name"
VERSION = 1
PARAMS = {}
ROLE = "single"


class TestSDK(unittest.TestCase):
    """Tests that sdk is supported by current server introspection."""

    def setUp(self):
        """Set mock_server url."""
        set_server_url("http://localhost:4000/")

    def test_list_model(self):
        """Test sdk.list_model method returns correct answer."""
        list_model = sdk.list_model()
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_model), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_model, pandas.core.frame.DataFrame)

    def test_list_dataset_loader(self):
        """Test sdk.list_dataset_loader method returns correct answer."""
        list_dataset_loader = sdk.list_dataset_loader()
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_dataset_loader), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_dataset_loader, pandas.core.frame.DataFrame)

    def test_list_executor(self):
        """Test sdk.list_executor method returns correct answer."""
        list_executor = sdk.list_executor()
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_executor), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_executor, pandas.core.frame.DataFrame)

    def test_add_ml_job(self):
        """Test sdk.add_ml_job method returns correct answer."""
        self.assertIsInstance(
            sdk.add_ml_job(
                job_executor_name=NAME,
                executor_params=PARAMS,
                models_pattern=ArbitraryModels(
                    models=[
                        ModelWithRole(role=ROLE, model_version_choice=ModelVersionChoice(name=NAME, version=VERSION))
                    ]
                ),
                data_pattern=SingleDatasetLoader(
                    name=NAME,
                    version=VERSION,
                    params=[DatasetLoaderMethodParams(params=PARAMS)],
                    collector_params=PARAMS,
                ),
                job_executor_version=VERSION,
            ),
            str,
        )

    def test_job_by_name(self):
        """Test sdk.job_by_name method returns correct answer."""
        job = sdk.job_by_name("job_name")
        self.assertIsInstance(job, ExecutionJob)

    def test_job_metric_by_name(self):
        """Test sdk.job_metric_by_name method returns correct answer."""
        metric = sdk.job_metric_by_name(name=NAME)
        # mock server generates non-empty result by introspection.
        self.assertEqual(len(metric), 1)
        # sdk returns an object of the correct type.
        self.assertIsInstance(sdk.job_metric_by_name(name=NAME), pandas.core.frame.DataFrame)

    def test_list_model_version(self):
        """Test sdk.list_model_version method returns correct answer."""
        list_model_version = sdk.list_model_version(name=NAME)
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_model_version), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_model_version, pandas.core.frame.DataFrame)

    def test_list_dataset_loader_version(self):
        """Test sdk.list_dataset_loader_version method returns correct answer."""
        list_dataset_loader_version = sdk.list_dataset_loader_version(name=NAME)
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_dataset_loader_version), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_dataset_loader_version, pandas.core.frame.DataFrame)

    def test_list_executor_version(self):
        """Test sdk.list_executor_version method returns correct answer."""
        list_executor_version = sdk.list_executor_version(name=NAME)
        # mock server generates non-empty result by introspection.
        self.assertGreater(len(list_executor_version), 0)
        # sdk returns an object of the correct type.
        self.assertIsInstance(list_executor_version, pandas.core.frame.DataFrame)

    def test_model_version_metainfo(self):
        """Test sdk.model_version_metainfo method returns correct answer."""
        self.assertIsInstance(sdk.model_version_metainfo(name=NAME, version=VERSION), ModelVersion)

    def test_rebuild_model_version_image(self):
        """Test sdk.rebuild_model_version_image method returns correct answer."""
        self.assertIsInstance(sdk.rebuild_model_version_image(name=NAME, version=VERSION), str)

    def test_available_metrics(self):
        """Test sdk.available_metrics method returns correct answer."""
        self.assertIsInstance(sdk.available_metrics("job_name"), list)
        self.assertIsInstance(sdk.available_metrics("job_name")[0], str)

    def test_metric_history(self):
        """Test sdk.available_metrics method returns correct answer."""
        response = sdk.metric_history("job_name", "metric")
        self.assertIsInstance(response, tuple)
        self.assertIsInstance(response[0], list)

    def test_get_required_classes_by_executor(self):
        """Test sdk.get_required_classes_by_executor method returns correct answer."""
        required_classes = sdk.get_required_classes_by_executor(name=NAME, version=VERSION)
        self.assertEqual(required_classes, {})

    def test_print_model_schema_for_executor(self):
        """Test a successful sdk.print_model_schema_for_executor call."""
        sdk.print_model_schema_for_executor(
            executor_name=NAME, models=[{"name": NAME, "version": VERSION, "role": ROLE}], executor_version=VERSION
        )

    def test_generate_model_params_for_executor(self):
        """Test sdk.generate_model_params_for_executor method returns correct answer."""
        model_params = sdk.generate_model_params_for_executor(
            executor_name=NAME, models=[{"name": NAME, "version": VERSION, "role": ROLE}], executor_version=VERSION
        )
        self.assertTrue(isinstance(model_params, list) or isinstance(model_params, ArbitraryModels))
        if isinstance(model_params, list):
            for model in model_params:
                self.assertIsInstance(model, ModelMethodParams)
        else:
            self.assertGreaterEqual(len(model_params.models), 1)
            self.assertEqual(model_params.models[0].role, ROLE)
            self.assertEqual(NAME, model_params.models[0].model_version_choice.name)
            self.assertIsInstance(model_params.models[0].params, list)
            self.assertGreaterEqual(len(model_params.models[0].params), 1)
            self.assertIsInstance(model_params.models[0].params[0], ModelMethodParams)

    def test_print_datasetloader_schema(self):
        """Test a successful sdk.print_datasetloader_schema call."""
        sdk.print_datasetloader_schema(name=NAME, version=VERSION)

    def test_print_executor_schema(self):
        """Test a successful sdk.print_executor_schema call."""
        sdk.print_executor_schema(name=NAME, version=VERSION)

    def test_print_executor_roles(self):
        """Test a successful sdk.print_executor_roles call."""
        sdk.print_executor_roles(name=NAME, version=VERSION)

    def test_cancels(self):
        """Test a successful sdk.cancel_* calls."""
        self.assertIsInstance(sdk.cancel_build_job_for_model_version(model_name=NAME, model_version=VERSION), bool)
        self.assertIsInstance(
            sdk.cancel_build_job_for_executor_version(executor_name=NAME, executor_version=VERSION), bool
        )
        self.assertIsInstance(sdk.cancel_venv_build_job_for_model_version(model_name=NAME, model_version=VERSION), bool)
        self.assertIsInstance(sdk.cancel_job("job"), bool)

    def test_delete_objects(self):
        """Test a successful sdk.delete_* calls."""
        self.assertIsInstance(sdk.delete_model_version(model_name=NAME, model_version=VERSION), bool)
        self.assertIsInstance(sdk.delete_model(model_name=NAME), bool)
        self.assertIsInstance(sdk.delete_executor_version(executor_name=NAME, executor_version=VERSION), bool)
        self.assertIsInstance(sdk.delete_executor(executor_name=NAME), bool)
        self.assertIsInstance(sdk.delete_dataset_loader(dataset_loader_name=NAME), bool)
        self.assertIsInstance(
            sdk.delete_dataset_loader_version(dataset_loader_name=NAME, dataset_loader_version=VERSION), bool
        )


if __name__ == "__main__":
    unittest.main()
