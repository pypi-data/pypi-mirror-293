"""SDK for client library."""
import json
import locale
import posixpath
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote

import httpx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import websocket
from jsf import JSF
from sgqlc.operation import Operation

from ML_management.dataset_loader.dataset_loader_pattern_to_methods_map import DatasetLoaderMethodName
from ML_management.executor import BaseExecutor
from ML_management.mlmanagement import get_server_url, get_server_websocket_url
from ML_management.mlmanagement.session import AuthSession
from ML_management.mlmanagement.variables import _get_s3_gateway_url
from ML_management.mlmanagement.visibility_options import VisibilityOptions
from ML_management.model.model_type_to_methods_map import ModelMethodName
from ML_management.registry.registry_manager import RegistryManager
from ML_management.sdk import schema
from ML_management.sdk.parameters import (
    ArbitraryDatasetLoaders,
    ArbitraryModels,
    ModelMethodParams,
    ModelVersionChoice,
    ModelWithRole,
    SingleDatasetLoader,
    SingleModel,
)
from ML_management.sdk.schema import DatasetLoader, ExecutionJob, Executor, Model, ModelVersion


class JobType(str, Enum):
    """Enum job type."""

    build = "build"
    execution = "execution"
    venv = "venv"


def _to_datetime(df: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
    """
    Convert df's columns to datetime.

    Parameters
    ----------
    df: pd.DataFrame
        pd.DataFrame in which the columns will be converted.
    column_names: List[str]
        Column names to be converted.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with converted columns.
    """
    for column_name in column_names:
        df[column_name] = pd.to_datetime(df[column_name], unit="s")

    return df


def send_graphql_request(op: Operation, json_response: bool = True) -> Any:
    """Send request to server and process the response."""
    json_data = AuthSession().sgqlc_request(op)

    if "data" not in json_data or json_data["data"] is None:
        server_url = get_server_url()
        try:
            if locale.getdefaultlocale()[0][:2] == "ru":
                url_base = posixpath.join(server_url, "locales/ru/ru.json")
            else:
                url_base = posixpath.join(server_url, "locales/en/en.json")
        except Exception:
            # if there is no locale file use english by default.
            url_base = posixpath.join(server_url, "locales/en/en.json")
        translation = httpx.get(url_base).json()

        error_message = json_data["errors"][0]["message"]

        try:
            message_type, message_value = error_message.split(".")
        except Exception:
            raise Exception(error_message) from None

        if message_type not in translation:
            raise Exception(message_type)

        formatted_translated_message = translation[message_type][message_value]
        if (
            ("extensions" in json_data["errors"][0])
            and ("params" in json_data["errors"][0]["extensions"])
            and (json_data["errors"][0]["extensions"]["params"] is not None)
        ):
            raise Exception(
                formatted_translated_message.format().format(**json_data["errors"][0]["extensions"]["params"])
            )
        raise Exception(formatted_translated_message)

    if json_response:
        return json_data["data"]
    else:
        return op + json_data


def update_bucket_visibility(bucket_name: str, new_visibility: VisibilityOptions) -> None:
    with AuthSession().post(
        posixpath.join(_get_s3_gateway_url(), "update-bucket-auth", bucket_name),
        json={"visibility": new_visibility.value},
    ) as response:
        response.raise_for_status()
        print("Visibility successfully updated")


def list_model() -> pd.DataFrame:
    """
    List available models.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with list of available models.
    """
    op = Operation(schema.Query)
    op.list_model.name()
    op.list_model.description()
    op.list_model.creation_timestamp()
    op.list_model.last_updated_timestamp()
    json_data = send_graphql_request(op)
    df = pd.DataFrame.from_dict(json_data["listModel"])
    if not df.empty:
        df = _to_datetime(df, ["creationTimestamp", "lastUpdatedTimestamp"])
    return df


def available_metrics(job_name: str) -> List[str]:
    """
    List logged types of logged metrics in given job.

    Parameters
    ----------
    job_name: str
        Name of the job.

    Returns
    -------
    List[str]
        List with names of metrics.
    """
    op = Operation(schema.Query)
    base = op.job_from_name(name=job_name)
    base.available_metrics()
    job = send_graphql_request(op, False)

    return job.job_from_name.available_metrics


def metric_history(
    job_name: str, metric_name: str, x_axis: str = "step", make_graph: bool = True, **kwargs
) -> Tuple[List[float], List[float]]:
    """
    Lists history of given metric in given job and plots graph of metric's change over time.

    Parameters
    ----------
    job_name: str
        Name of the job.
    metric_name: str
        Name of the metric.
    x_axis: str
        Witch value use as x axis for graph or as return value. Possible options: "time", "step"
    make_graph: bool
        If to build graph of metric over time.
    kwargs: Any
        Any additional key arguments for plt.plot.

    Returns
    -------
    Tuple(List[float], List[float])
        First list with provided x axis of logged metric.
        Second list with values of metrics.
        Also plots graph using provided x axis and metric's values as y axis.
    """
    op = Operation(schema.Query)
    base = op.job_from_name(name=job_name)
    base.metric_history(metric=metric_name)
    job = send_graphql_request(op, False)
    metrics = job.job_from_name.metric_history
    metric_values = [metric.value for metric in metrics]
    x_values = []
    if x_axis != "step" and x_axis != "time":
        raise ValueError("x_axis value must be step or time")
    if x_axis == "step":
        x_values = [metric.step for metric in metrics]
        if np.nonzero(x_values)[0].size == 0:
            metrics = sorted(metrics, key=lambda x: x.timestamp)
            x_values = [step[0] for step in enumerate(metrics)]
        else:
            metrics = sorted(metrics, key=lambda x: x.step)
    elif x_axis == "time":
        metrics = sorted(metrics, key=lambda x: x.timestamp)
        start_timestamp = metrics[0].timestamp
        x_values = [(metric.timestamp - start_timestamp) / 1000 for metric in metrics]

    if make_graph:
        plt.grid()
        plt.xlabel("seconds" if x_axis == "time" else "step")
        plt.ylabel(metric_name)
        plt.plot(x_values, metric_values, marker=".", **kwargs)

    return x_values, metric_values


def delete_model(model_name: str) -> bool:
    """
    Delete model and all of it's versions.

    Parameters
    ----------
    model_name: str
        Name of the model to delete.
    """
    op = Operation(schema.Mutation)
    op.delete_model(name=model_name)
    return send_graphql_request(op)["deleteModel"]


def delete_model_version(model_name: str, model_version: int) -> bool:
    """
    Delete version of a model.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op = Operation(schema.Mutation)
    model_version_choice = schema.ObjectVersionInput(name=model_name, version=model_version)
    op.delete_model_version_from_name_version(model_version=model_version_choice)
    return send_graphql_request(op)["deleteModelVersionFromNameVersion"]


def delete_dataset_loader(dataset_loader_name: str) -> bool:
    """
    Delete dataset loader and all of it's versions.

    Parameters
    ----------
    dataset_loader_name: str
        Name of the dataset loader to delete.
    """
    op = Operation(schema.Mutation)
    op.delete_dataset_loader(name=dataset_loader_name)
    return send_graphql_request(op)["deleteDatasetLoader"]


def delete_dataset_loader_version(dataset_loader_name: str, dataset_loader_version: int) -> bool:
    """
    Delete version of a dataset loader.

    Parameters
    ----------
    dataset_loader_name: str
        The name of the dataset loader.
    dataset_loader_version: int
        The version of the dataset loader.
    """
    op = Operation(schema.Mutation)
    dataset_loader_version_choice = schema.ObjectVersionInput(name=dataset_loader_name, version=dataset_loader_version)
    op.delete_dataset_loader_version_from_name_version(dataset_loader_version=dataset_loader_version_choice)
    return send_graphql_request(op)["deleteDatasetLoaderVersionFromNameVersion"]


def delete_executor_version(executor_name: str, executor_version: int) -> bool:
    """
    Delete version of a executor.

    Parameters
    ----------
    executor_name: str
        The name of the executor.
    executor_version: int
        The version of the executor.
    """
    op = Operation(schema.Mutation)
    executor_version_choice = schema.ObjectVersionInput(name=executor_name, version=executor_version)
    op.delete_executor_version_from_name_version(executor_version=executor_version_choice)
    return send_graphql_request(op)["deleteExecutorVersionFromNameVersion"]


def delete_executor(executor_name: str) -> bool:
    """
    Delete executor and all of it's versions.

    Parameters
    ----------
    executor_name: str
        Name of the executor to delete.
    """
    op = Operation(schema.Mutation)
    op.delete_executor(name=executor_name)
    return send_graphql_request(op)["deleteExecutor"]


def cancel_job(job_name: str) -> bool:
    """
    Cancel running or planned execution job.

    Parameters
    ----------
    job_name: str
        Name of the job to cancel.
    """
    op = Operation(schema.Mutation)
    op.cancel_job(job_name=job_name)
    return send_graphql_request(op)["cancelJob"]


def cancel_build_job_for_model_version(model_name: str, model_version: int) -> bool:
    """
    Cancel running or planned build job of model image.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op.cancel_build_job_for_model_version(name=model_name, version=model_version)
    return send_graphql_request(op)["cancelBuildJobForModelVersion"]


def cancel_build_job_for_executor_version(executor_name: str, executor_version: int) -> bool:
    """
    Cancel running or planned build job of executor's image.

    Parameters
    ----------
    executor_name: str
        The name of the executor.
    executor_version: int
        The version of the executor.
    """
    op = Operation(schema.Mutation)
    op.cancel_build_job_for_executor_version(name=executor_name, version=executor_version)
    return send_graphql_request(op)["cancelBuildJobForExecutorVersion"]


def cancel_venv_build_job_for_model_version(model_name: str, model_version: int) -> bool:
    """
    Cancel running or planned build job of model's environment.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op.cancel_venv_build_job_for_model_version(name=model_name, version=model_version)
    return send_graphql_request(op)["cancelVenvBuildJobForModelVersion"]


def list_dataset_loader() -> pd.DataFrame:
    """
    List available dataset_loaders.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with list of available dataset_loaders.
    """
    op = Operation(schema.Query)
    op.list_dataset_loader.name()
    op.list_dataset_loader.description()
    op.list_dataset_loader.creation_timestamp()
    op.list_dataset_loader.last_updated_timestamp()
    json_data = send_graphql_request(op)
    df = pd.DataFrame.from_dict(json_data["listDatasetLoader"])
    if not df.empty:
        df = _to_datetime(df, ["creationTimestamp", "lastUpdatedTimestamp"])
    return df


def list_executor() -> pd.DataFrame:
    """
    List available executors.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with list of available executors.
    """
    op = Operation(schema.Query)
    op.list_executor.name()
    op.list_executor.description()
    op.list_executor.creation_timestamp()
    op.list_executor.last_updated_timestamp()
    json_data = send_graphql_request(op)
    df = pd.DataFrame.from_dict(json_data["listExecutor"])
    if not df.empty:
        df = _to_datetime(df, ["creationTimestamp", "lastUpdatedTimestamp"])
    return df


def add_ml_job(
    job_executor_name: str,
    executor_params: dict,
    models_pattern: Union[SingleModel, ArbitraryModels],
    data_pattern: Union[SingleDatasetLoader, ArbitraryDatasetLoaders],
    gpu: bool = False,
    job_executor_version: Optional[int] = None,
    experiment_name: str = "Default",
    cron_expression: Optional[str] = None,
    periodic_type: str = "ONCE",
    additional_system_packages: Optional[List[str]] = None,
) -> str:
    """
    Create execution job.

    Parameters
    ----------
    job_executor_name: str
        Name of the executor that will execute the job.
    executor_params: Dict[str, ...]
        Dictionary of executor parameters.
        Example::

            {
                'executor_param1': 'value1',
                'executor_param2': 'value2',
                'executor_param3': 'value3',
                ...
            }

    models_pattern: Union[SingleModel, ArbitraryModels]
        Necessary information for using the models.
    data_pattern: Union[SingleDatasetLoader, ArbitraryDatasetLoaders]
        Necessary information for using the datasets.
    gpu: bool = False
        Whether to use GPU for this job or not. Default: False
    job_executor_version: Optional[int] = None
        Version of the executor that will execute the job. Default: None, "latest" version is used.
    experiment_name: str = "Default"
        Name of the experiment. Default: "Default"
    cron_expression: str = None
        Cron expression for periodic or deferred jobs. Default: None
    periodic_type: {"ONCE", "PERIODIC"}
        Frequency of the task. Default: "ONCE"
    additional_system_packages: Optional[List[str]] = None
        List of system libraries for Debian family distributions that need to be installed in the job. Default: None

    Returns
    -------
    str
        Name of the Job.
    """
    if not isinstance(models_pattern, SingleModel) and not isinstance(models_pattern, ArbitraryModels):
        raise TypeError("Parameter models must have type SingleModel or ArbitraryModels.")
    if not isinstance(data_pattern, SingleDatasetLoader) and not isinstance(data_pattern, ArbitraryDatasetLoaders):
        raise TypeError("Parameter data_pattern must have type SingleDatasetLoader or ArbitraryDatasetLoaders.")
    models = models_pattern.serialize()
    data_params = data_pattern.serialize()
    list_role_data_params = []
    for data_param_role in data_params:
        op = Operation(schema.Query)
        data_inner_params: dict = data_param_role["data_params"]
        dataset_loader_name = data_inner_params["dataset_loader_name"]
        dataset_loader_version = data_inner_params.get("dataset_loader_version") or int(
            RegistryManager().get_latest_dataset_loader_version(name=dataset_loader_name).version
        )
        dataset_loader_version_choice = schema.ObjectVersionOptionalInput(
            name=dataset_loader_name, version=dataset_loader_version
        )

        collector_name = data_inner_params["collector_name"]
        _dataset_loader_version = schema.ObjectVersionInput(name=dataset_loader_name, version=dataset_loader_version)
        dataset_collector_schema = op.dataset_loader_version_from_name_version(
            dataset_loader_version=_dataset_loader_version
        ).data_json_schema(collector_name=collector_name)
        dataset_collector_schema.collector_method_schema.schema_name()
        dataset_loader_version_obj = send_graphql_request(op, json_response=False)
        collector_method_name = (
            dataset_loader_version_obj.dataset_loader_version_from_name_version.data_json_schema.collector_method_schema.schema_name  # noqa: E501
        )
        collector_method_params = schema.MethodParamsInput(
            method_name=collector_method_name, method_params=json.dumps(data_inner_params["collector_params"])
        )

        list_dataset_loader_method_params = []
        for item in data_inner_params["dataset_loader_params"]:
            for key in item:
                list_dataset_loader_method_params.append(
                    schema.MethodParamsInput(method_name=key, method_params=json.dumps(item[key]))
                )

        current_dataset_loader_params = schema.DataParamsInput(
            dataset_loader_version_choice=dataset_loader_version_choice,
            collector_name=collector_name,
            list_dataset_loader_method_params=list_dataset_loader_method_params,
            collector_method_params=collector_method_params,
        )

        list_role_data_params.append(
            schema.RoleDataParamsInput(role=data_param_role["role"], data_params=current_dataset_loader_params)
        )

    if job_executor_version is None:
        job_executor_version = int(RegistryManager().get_latest_executor_version(name=job_executor_name).version)

    op = Operation(schema.Query)
    _executor_version = schema.ObjectVersionInput(name=job_executor_name, version=job_executor_version)

    executor_version_choice = schema.ObjectVersionOptionalInput(name=job_executor_name, version=job_executor_version)

    executor_model_schema = op.executor_version_from_name_version(executor_version=_executor_version)
    executor_model_schema.executor_method_schema_name()

    executor_version_obj = send_graphql_request(op, json_response=False)
    executor_method_schema = executor_version_obj.executor_version_from_name_version.executor_method_schema_name

    executor_method_params = schema.MethodParamsInput(
        method_name=executor_method_schema, method_params=json.dumps(executor_params)
    )

    list_role_model_params = []

    for model in models:
        choice_criteria = model["model"].get("choice_criteria", "latest")
        version = model["model"].get("version")
        if choice_criteria == "latest" and version is None:
            version = int(RegistryManager().get_latest_model_version(name=model["model"]["name"]).version)

        metric_name = model["model"].get("metric_name")

        optimal_min = model["model"].get("optimal_min", False)

        model_version_choice = schema.ModelVersionChoice(
            name=model["model"]["name"],
            version=version,
            choice_criteria=choice_criteria,
            metric_name=metric_name,
            optimal_min=optimal_min,
        )

        model_methods_params = []

        for item in model["params"]:
            for key in item:
                model_methods_params.append(
                    schema.MethodParamsInput(method_name=key, method_params=json.dumps(item[key]))
                )

        new_model_name = model.get("new_model_name")
        new_model_description = model.get("description")
        prepare_new_model_inference = model.get("prepare_new_model_inference", False)

        current_model_params = schema.ModelParamsInput(
            model_version_choice=model_version_choice,
            list_model_method_params=model_methods_params,
            new_model_name=new_model_name,
            prepare_new_model_inference=prepare_new_model_inference,
            description=new_model_description,
        )

        model_role = schema.RoleModelParamsInput(role=model["role"], model_params=current_model_params)

        list_role_model_params.append(model_role)

    executor_params = schema.ExecutorParamsInput(
        executor_method_params=executor_method_params,
        executor_version_choice=executor_version_choice,
    )

    op = Operation(schema.Mutation)
    mutation = op.add_ml_job(
        form=schema.JobParameters(
            executor_params=executor_params,
            list_role_model_params=list_role_model_params,
            list_role_data_params=list_role_data_params,
            experiment_name=experiment_name,
            cron_expression=cron_expression,
            periodic_type=periodic_type,
            gpu=gpu,
            additional_system_packages=additional_system_packages,
        )
    )

    mutation.name()

    job = send_graphql_request(op, json_response=False)

    return job.add_ml_job.name


def job_by_name(name: str) -> ExecutionJob:
    """
    Return Job object by name.

    Parameters
    ----------
    name: str
        Name of the job.

    Returns
    -------
    Job
        Instance of the Job class.
    """
    op = Operation(schema.Query)

    base_query = op.job_from_name(name=name)
    base_query.name()
    base_query.periodic_type()
    base_query.status()
    base_query.registration_timestamp()
    base_query.start_timestamp()
    base_query.end_timestamp()
    base_query.build_job()
    base_query.exception()

    job = send_graphql_request(op, json_response=False)

    return job.job_from_name


def job_metric_by_name(name: str) -> pd.DataFrame:
    """
    Job's most recent logged metrics.

    Parameters
    ----------
    name: str
        Name of the job.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with latest metrics.
    """
    op = Operation(schema.Query)

    op.job_from_name(name=name).run.latest_metrics()
    json_data = send_graphql_request(op)

    json_data = json_data["jobFromName"]["run"]["latestMetrics"] if json_data["jobFromName"]["run"] else None

    return pd.DataFrame([json_data])


def list_model_version(name: str) -> pd.DataFrame:
    """
    List available versions of the model with such name.

    Parameters
    ----------
    name: str
        Name of the model.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with a list of available model versions.
    """
    op = Operation(schema.Query)
    base_query = op.model_from_name(name=name).list_model_version
    base_query.version()
    base_query.creation_timestamp()
    base_query.status()
    json_data = send_graphql_request(op)

    df = pd.DataFrame.from_dict(json_data["modelFromName"]["listModelVersion"])
    df = _to_datetime(df, ["creationTimestamp"])

    return df.sort_values(by=["version"], ignore_index=True)


def list_dataset_loader_version(name: str) -> pd.DataFrame:
    """
    List available versions of the dataset_loader with such name.

    Parameters
    ----------
    name: str
        Name of the DatasetLoader.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with a list of available dataset_loader versions.
    """
    op = Operation(schema.Query)
    base_query = op.dataset_loader_from_name(name=name).list_dataset_loader_version
    base_query.version()
    base_query.creation_timestamp()
    base_query.status()
    json_data = send_graphql_request(op)

    df = pd.DataFrame.from_dict(json_data["datasetLoaderFromName"]["listDatasetLoaderVersion"])
    df = _to_datetime(df, ["creationTimestamp"])

    return df.sort_values(by=["version"], ignore_index=True)


def list_executor_version(name: str) -> pd.DataFrame:
    """
    List available versions of the executor with such name.

    Parameters
    ----------
    name: str
        Name of the executor.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with a list of available executor versions.
    """
    op = Operation(schema.Query)
    base_query = op.executor_from_name(name=name).list_executor_version
    base_query.version()
    base_query.creation_timestamp()
    base_query.status()
    json_data = send_graphql_request(op)

    df = pd.DataFrame.from_dict(json_data["executorFromName"]["listExecutorVersion"])
    df = _to_datetime(df, ["creationTimestamp"])

    return df.sort_values(by=["version"], ignore_index=True)


def model_version_metainfo(name: str, version: Optional[int] = None) -> ModelVersion:
    """
    Meta information about the model version by the model name and version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    ModelVersion
        ModelVersion instance with meta information.
    """
    if version is None:
        version = int(RegistryManager().get_latest_model_version(name=name).version)

    op = Operation(schema.Query)
    _model_version = schema.ObjectVersionInput(name=name, version=version)
    base_query = op.model_version_from_name_version(model_version=_model_version)
    base_query.name()
    base_query.version()
    base_query.status()
    base_query.build_job().status()
    base_query.build_job().build_object_name()
    base_query.available_executor_versions.name()
    base_query.available_executor_versions.version()
    model_version = send_graphql_request(op, json_response=False)
    return model_version.model_version_from_name_version


def rebuild_model_version_image(name: str, version: int) -> str:
    """
    Start building new docker image for specified model version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: int
        Version of the model

    Returns
    -------
    str
        name of new docker image for specified model version.
    """
    op = Operation(schema.Mutation)
    _model_version = schema.ObjectVersionInput(name=name, version=version)
    op.rebuild_model_version_image(model_version=_model_version)
    result = send_graphql_request(op=op)
    return result["rebuildModelVersionImage"]


def _generate_fake_schema(json_schema: dict) -> dict:
    if "required" not in json_schema.keys():
        return {}

    required_properties = {key: json_schema["properties"][key] for key in json_schema["required"]}
    json_schema["properties"] = required_properties

    faker = JSF(json_schema)
    fake_json = faker.generate()
    return fake_json


def _print_params_by_schema(json_schema: Dict, schema_type: str) -> None:
    """Print entity JSON Schema and example with required params."""
    properties_and_required_dict = {key: json_schema[key] for key in ("properties", "required") if key in json_schema}

    json_formatted_str = json.dumps(properties_and_required_dict, indent=2)

    print(f"{schema_type} json-schema:")

    print(json_formatted_str)

    print(f"{schema_type} parameters example:")

    fake_json = _generate_fake_schema(json_schema)

    print(fake_json)


def _get_model_schema_for_executor(executor_name: str, executor_version: Optional[int], models: list) -> dict:
    if executor_version is None:
        executor_version = int(RegistryManager().get_latest_executor_version(name=executor_name).version)

    role_models = []

    for model in models:
        model_name = model["name"]
        model_version = model.get("version") or int(RegistryManager().get_latest_model_version(name=model_name).version)
        model_role = model.get("role", BaseExecutor.DEFAULT_ROLE)

        current_model = schema.ObjectVersionInput(name=model_name, version=model_version)
        current_role = schema.RoleObjectVersionInput(role=model_role, object_version=current_model)

        role_models.append(current_role)

    op = Operation(schema.Query)

    _executor_version = schema.ObjectVersionInput(name=executor_name, version=executor_version)
    base_query = (
        op.executor_version_from_name_version(executor_version=_executor_version)
        .job_json_schema_for_models(models=role_models)
        .list_role_model_method_schemas
    )

    base_query.role()
    base_query.list_method_schemas.schema_name()
    base_query.list_method_schemas.json_schema()

    json_data = send_graphql_request(op)
    return json_data["executorVersionFromNameVersion"]["jobJsonSchemaForModels"]["listRoleModelMethodSchemas"]


def print_model_schema_for_executor(
    executor_name: str, models: List[dict], executor_version: Optional[int] = None
) -> None:
    """
    Print model schema for particular executor.

    Parameters
    ----------
    executor_name: str
        Name of the executor.
    models: List[dict]
        Necessary information about the model.

        Example1::

            [
                {"name": "simple_model"} # str
            ]

        Example2::

            [
                {
                    "name": "model_name1", # str
                    "role": "role1", # Optional[str]
                    "version": version # Optional[int]
                },
                {
                    "name": "model_name2", # str
                    "role": "role2", # Optional[str]
                    "version": version # Optional[int]
                }
            ]
    executor_version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.
    """
    models_methods_schemas = _get_model_schema_for_executor(
        executor_name=executor_name,
        executor_version=executor_version,
        models=models,
    )
    for model_methods_schemas in models_methods_schemas:
        role = model_methods_schemas["role"]
        for model in models:
            if ("role" in model and model["role"] == role) or "role" not in model:
                model_name = model["name"]

        print(f"Model name: {model_name}, model role: {role}")
        for model_methods_schema in model_methods_schemas["listMethodSchemas"]:
            _print_params_by_schema(
                model_methods_schema["jsonSchema"], ModelMethodName(model_methods_schema["schemaName"]).name
            )
        print()


def generate_model_params_for_executor(
    executor_name: str, models: List[dict], executor_version: Optional[int] = None
) -> Union[List[ModelMethodParams], ArbitraryModels]:
    """
    Return example of model's methods parameters for executor.

    Parameters
    ----------
    executor_name: str
        Name of the executor.
    models: List[dict]
        Necessary information about the model.

        Example1::

            [
                {"name": "simple_model"}
            ];

        Example2::

            [
                {
                    "name": "model_name1", # str
                    "role": "role1", # Optional[str]
                    "version": version # Optional[int]
                },
                {
                    "name": "model_name2", # str
                    "role": "role2", # Optional[str]
                    "version": version # Optional[int]
                }
            ]

    executor_version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.

    Returns
    -------
    List[ModelMethodParams]:
        Example of model's methods parameters in case simple executor.

        Example output::

            [
                ModelMethodParams(
                    method=ModelMethodName.evaluate_function,
                    params={key1: value1, key2: value2}
                )
            ]

    ArbitraryModels:
        Example of models parameter for add_ml_job function.

        Example output::

            ArbitraryModels(
                models=[
                    ModelWithRole(
                        role="role_one",
                        model_version_choice=ModelVersionChoice(
                            name="model_1_name",
                            version=1
                        )
                        params=[
                            ModelMethodParams(
                                method=ModelMethodName.evaluate_function,
                                params={key1: value1, key2: value2}
                            ),
                            ModelMethodParams(
                                method=ModelMethodName.finetune_function,
                                params={key1: value1, key2: value2}
                            )
                        ]
                    ),
                    ModelWithRole(
                        role="role_two",
                        model_version_choice=ModelVersionChoice(
                            name="model_2_name",
                            version=1
                        )
                        params=[
                            ModelMethodParams(
                                method=ModelMethodName.evaluate_function,
                                params={key1: value1, key2: value2}
                            ),
                            ModelMethodParams(
                                method=ModelMethodName.finetune_function,
                                params={key1: value1, key2: value2}
                            )
                        ]
                    ),
                ]
            )

    """
    models_methods_schemas = _get_model_schema_for_executor(
        executor_name=executor_name,
        executor_version=executor_version,
        models=models,
    )

    sdk_models = []

    for model_methods_schemas in models_methods_schemas:
        list_model_params = []
        for model_methods_schema in model_methods_schemas["listMethodSchemas"]:
            list_model_params.append(
                ModelMethodParams(
                    method=ModelMethodName(model_methods_schema["schemaName"]),
                    params=_generate_fake_schema(model_methods_schema["jsonSchema"]),
                )
            )
        if len(models_methods_schemas) == 1:
            return list_model_params
        role = model_methods_schemas["role"]
        for model in models:
            if model["role"] == role:
                model_name = model["name"]
                model_version = model.get("version") or int(
                    RegistryManager().get_latest_model_version(name=model_name).version
                )
                break
        current_model = ModelWithRole(
            role=role,
            model_version_choice=ModelVersionChoice(name=model_name, version=model_version),
            params=list_model_params,
        )

        sdk_models.append(current_model)

    return ArbitraryModels(models=sdk_models)


def print_datasetloader_schema(name: str, version: Optional[int] = None) -> None:
    """
    Print DatasetLoader schema.

    Parameters
    ----------
    name: str
        Name of the DatasetLoader.
    version: Optional[int] = None
        Version of the DatasetLoader. Default: None, "latest" version is used.
    """
    if version is None:
        version = int(RegistryManager().get_latest_dataset_loader_version(name=name).version)

    op = Operation(schema.Query)
    _datasetloader_version = schema.ObjectVersionInput(name=name, version=version)
    base_query = op.dataset_loader_version_from_name_version(dataset_loader_version=_datasetloader_version)
    base_query.dataset_loader_method_schemas()
    json_data = send_graphql_request(op)
    json_data = json_data["datasetLoaderVersionFromNameVersion"]["datasetLoaderMethodSchemas"]
    print(f"DatasetLoader {name} version {version} json-schema:")
    for method_name, schema_ in json_data.items():
        _print_params_by_schema(json_schema=schema_, schema_type=DatasetLoaderMethodName(method_name).name)


def print_executor_schema(name: str, version: Optional[int] = None) -> None:
    """
    Print executor schema.

    Parameters
    ----------
    name: str
        Name of the executor.
    version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.
    """
    if version is None:
        version = int(RegistryManager().get_latest_executor_version(name=name).version)
    op = Operation(schema.Query)
    executor_version = schema.ObjectVersionInput(name=name, version=version)
    base_query = op.executor_version_from_name_version(executor_version=executor_version)
    base_query.executor_method_schema()
    json_data = send_graphql_request(op)

    json_data = json_data["executorVersionFromNameVersion"]["executorMethodSchema"]
    _print_params_by_schema(json_schema=json_data, schema_type="Executor")


def print_executor_roles(name: str, version: Optional[int] = None) -> None:
    """
    Print the roles required by the executor.

    Parameters
    ----------
    name: str
        Name of the executor.
    version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.
    """
    if version is None:
        version = int(RegistryManager().get_latest_executor_version(name=name).version)
    op = Operation(schema.Query)
    executor_version = schema.ObjectVersionInput(name=name, version=version)
    base_query = op.executor_version_from_name_version(executor_version=executor_version)
    base_query.desired_model_methods()
    base_query.desired_dataset_loader_methods()
    json_data = send_graphql_request(op)
    print("Desired model methods:", json_data["executorVersionFromNameVersion"]["desiredModelMethods"])
    print("Desired dataset loader methods:", json_data["executorVersionFromNameVersion"]["desiredDatasetLoaderMethods"])


def _get_logs_url(params: Dict[str, Any], job_type: JobType, stream: bool = True) -> str:
    server_url = get_server_websocket_url() if stream else get_server_url()
    url_base = posixpath.join(server_url, "logs-api")
    url_encoded_params = "&".join(f"{quote(str(key))}={quote(str(value))}" for key, value in params.items())
    local_path = f"{f'stream/{job_type.value}' if stream else f'filedump/{job_type.value}'}?{url_encoded_params}"
    return posixpath.join(url_base, local_path)


def _get_logs(job_type: JobType, params: Dict[str, Any], stream: bool = True, file_name: Optional[str] = None) -> None:
    url = _get_logs_url(params=params, stream=stream, job_type=job_type)
    if stream:
        ws = None
        file = sys.stdout
        try:
            ws = AuthSession().instantiate_websocket_connection(url)
            if file_name:
                file = open(file_name, "w")
            while True:
                data = ws.recv()
                if not data:
                    return
                data = json.loads(data)
                if "status" not in data or data["status"] != "OK":
                    raise RuntimeError("Internal Server Error")
                print("\n".join(data["logs"]), file=file)
        except KeyboardInterrupt:
            pass
        except websocket._exceptions.WebSocketBadStatusException:
            possible_reasons_msg = (
                "Model with that name and version does not exist or does not have build job"
                if job_type is not JobType.execution
                else "Job with that name does not exist"
            )
            print(
                "<Connection refused. Check your query parameters, they may be incorrect.>\n"
                "<Possible reasons:>\n"
                f"<{possible_reasons_msg}>"
            )
        except Exception as err:
            print(err)
        finally:
            if ws is not None:
                ws.close()
            if file_name:
                file.close()
        return

    with AuthSession().get(url, stream=True) as resp:
        if file_name:
            with open(file_name, "a") as f:
                for line in resp.iter_lines():
                    if line:
                        f.writelines([line, "\n"])
        else:
            for line in resp.iter_lines():
                if line:
                    print(line)


def get_logs(job_name: str, stream: bool = True, file_name: Optional[str] = None) -> None:
    """
    Stream logs of the execution job by job name.

    Parameters
    ----------
    job_name: str
        Name of the execution job whose logs we want to view.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    _get_logs(job_type=JobType.execution, stream=stream, file_name=file_name, params={"job_id": job_name})


def get_build_logs(
    model_name: str, model_version: Optional[int] = None, stream: bool = True, file_name: Optional[str] = None
) -> None:
    """
    Stream logs of the build job by model name and version.

    Parameters
    ----------
    model_name: str
        The name of the model whose docker image creation logs you want to view.
    model_version: Optional[int] = None
        The version of the model whose docker image creation logs you want to view.
        Default: None, "latest" version is used.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    model_version = (
        int(RegistryManager().get_latest_model_version(name=model_name).version)
        if model_version is None
        else model_version
    )
    _get_logs(
        job_type=JobType.build,
        stream=stream,
        file_name=file_name,
        params={"model_name": model_name, "model_version": model_version},
    )


def get_venv_build_logs(
    model_name: str, model_version: Optional[int] = None, stream: bool = True, file_name: Optional[str] = None
) -> None:
    """
    Stream logs of the venv archive creating job by model name and version.

    Parameters
    ----------
    model_name: str
        The name of the model whose venv archive creation logs you want to view.
    model_version: Optional[int] = None
        The version of the model whose venv archive creation logs you want to view.
        Default: None, "latest" version is used.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    model_version = (
        int(RegistryManager().get_latest_model_version(name=model_name).version)
        if model_version is None
        else model_version
    )
    _get_logs(
        job_type=JobType.venv,
        stream=stream,
        file_name=file_name,
        params={"model_name": model_name, "model_version": model_version},
    )


def serve_model(name: str, version: Optional[int] = None, gpu: bool = False) -> str:
    """
    Start model serving in triton service.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.
    gpu: bool
        Determine which device will be used: GPU or CPU. Default: False, CPU is used.

    Returns
    -------
    str:
        endpoint path to make inference requests for model version.
    """
    version = int(RegistryManager().get_latest_model_version(name=name).version) if version is None else version
    op = Operation(schema.Mutation)
    serving_parameters = schema.ModelServingInput(
        model_version=schema.ObjectVersionInput(name=name, version=version), gpu=gpu
    )
    op.serve_model(serving_parameters=serving_parameters)
    send_graphql_request(op)
    return f"/v2/models/{name}/versions/{version}/infer"


def stop_model_serving(name: str, version: Optional[int] = None) -> None:
    """
    Stop model serving in triton service.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.
    """
    version = int(RegistryManager().get_latest_model_version(name=name).version) if version is None else version
    op = Operation(schema.Mutation)
    op.stop_model_serving(model_version=schema.ObjectVersionInput(name=name, version=version))
    send_graphql_request(op=op)
    print("Serving has been successfully stopped.")


def check_inference_model_readiness(name: str, version: Optional[int] = None) -> Optional[str]:
    """
    Check is model ready to accept requests.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    Optional[str]:
        endpoint path to make requests if model is ready else None
    """
    version = int(RegistryManager().get_latest_model_version(name=name).version) if version is None else version
    op = Operation(schema.Query)
    op.is_inference_model_ready(model_version=schema.ObjectVersionInput(name=name, version=version))
    json_data = send_graphql_request(op=op)
    result = f"/v2/models/{name}/versions/{version}/infer" if json_data["isInferenceModelReady"] else None
    return result


def get_required_classes_by_executor(name: str, version: Optional[int] = None) -> List[str]:
    """
    Return the names of classes for the model to be inherited from, by the name of the executor.

    Parameters
    ----------
    name: str
        Name of the executor.
    executor_version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.

    Returns
    -------
    List[str]:
        List of model class names to be inherited from.
    """
    if version is None:
        version = int(RegistryManager().get_latest_executor_version(name=name).version)
    op = Operation(schema.Query)
    executor_version = schema.ObjectVersionInput(name=name, version=version)
    base_query = op.executor_version_from_name_version(executor_version=executor_version)
    base_query.desired_model_patterns()
    json_data = send_graphql_request(op)
    return json_data["executorVersionFromNameVersion"]["desiredModelPatterns"]


def set_model_tag(name: str, key: str, value: str) -> Model:
    """
    Set model tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.
    value: str
        Value tag.

    Returns
    -------
    sdk.schema.Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_tag = op.set_model_tag(name=name, key=key, value=value)
    set_tag.name()
    set_tag.tags()
    model = send_graphql_request(op=op)
    return model


def set_executor_tag(name: str, key: str, value: str) -> Executor:
    """
    Set executor tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.
    value: str
        Value tag.

    Returns
    -------
    sdk.schema.Executor
        Executor instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_tag = op.set_executor_tag(name=name, key=key, value=value)
    set_tag.name()
    set_tag.tags()
    executor = send_graphql_request(op=op)
    return executor


def set_dataset_loader_tag(name: str, key: str, value: str) -> DatasetLoader:
    """
    Set dataset loader tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.
    value: str
        Value tag.

    Returns
    -------
    sdk.schema.DatasetLoader
        DatasetLoader instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_tag = op.set_dataset_loader_tag(name=name, key=key, value=value)
    set_tag.name()
    set_tag.tags()
    dataset_loader = send_graphql_request(op=op)
    return dataset_loader


def delete_dataset_loader_tag(name: str, key: str) -> DatasetLoader:
    """
    Delete dataset loader tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.

    Returns
    -------
    sdk.schema.DatasetLoader
        DatasetLoader instance with meta information.
    """
    op = Operation(schema.Mutation)
    delete_tag = op.delete_dataset_loader_tag(name=name, key=key)
    delete_tag.name()
    delete_tag.tags()
    dataset_loader = send_graphql_request(op=op)
    return dataset_loader


def delete_executor_tag(name: str, key: str) -> Executor:
    """
    Delete executor tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.

    Returns
    -------
    sdk.schema.Executor
        Executor instance with meta information.
    """
    op = Operation(schema.Mutation)
    delete_tag = op.delete_executor_tag(name=name, key=key)
    delete_tag.name()
    delete_tag.tags()
    executor = send_graphql_request(op=op)
    return executor


def delete_model_tag(name: str, key: str) -> Model:
    """
    Delete model tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.

    Returns
    -------
    sdk.schema.Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    delete_tag = op.delete_model_tag(name=name, key=key)
    delete_tag.name()
    delete_tag.tags()
    model = send_graphql_request(op=op)
    return model


def set_dataset_loader_description(name: str, description: str) -> DatasetLoader:
    """
    Set dataset loader description.

    Parameters
    ----------
    name: str
        Name of the model.
    description: str
        Description model.

    Returns
    -------
    sdk.schema.DatasetLoader
        DatasetLoader instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_description = op.set_dataset_loader_description(name=name, description=description)
    set_description.name()
    set_description.description()
    dataset_loader = send_graphql_request(op=op)
    return dataset_loader


def set_executor_description(name: str, description: str) -> Executor:
    """
    Set executor description.

    Parameters
    ----------
    name: str
        Name of the model.
    description: str
        Description model.

    Returns
    -------
    sdk.schema.Executor
        Executor instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_description = op.set_executor_description(name=name, description=description)
    set_description.name()
    set_description.description()
    executor = send_graphql_request(op=op)
    return executor


def set_model_description(name: str, description: str) -> Model:
    """
    Set model description.

    Parameters
    ----------
    name: str
        Name of the model.
    description: str
        Description model.

    Returns
    -------
    sdk.schema.Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_description = op.set_model_description(name=name, description=description)
    set_description.name()
    set_description.description()

    model = send_graphql_request(op=op)
    return model
