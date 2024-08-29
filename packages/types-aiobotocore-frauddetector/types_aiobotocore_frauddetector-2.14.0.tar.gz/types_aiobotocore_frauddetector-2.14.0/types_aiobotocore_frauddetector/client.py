"""
Type annotations for frauddetector service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_frauddetector.client import FraudDetectorClient

    session = get_session()
    async with session.create_client("frauddetector") as client:
        client: FraudDetectorClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    DataSourceType,
    DataTypeType,
    DetectorVersionStatusType,
    EventIngestionType,
    ListUpdateModeType,
    ModelEndpointStatusType,
    ModelTypeEnumType,
    ModelVersionStatusType,
    RuleExecutionModeType,
    TrainingDataSourceEnumType,
)
from .type_defs import (
    BatchCreateVariableResultTypeDef,
    BatchGetVariableResultTypeDef,
    CreateDetectorVersionResultTypeDef,
    CreateModelVersionResultTypeDef,
    CreateRuleResultTypeDef,
    DeleteEventsByEventTypeResultTypeDef,
    DescribeDetectorResultTypeDef,
    DescribeModelVersionsResultTypeDef,
    EntityTypeDef,
    EventOrchestrationTypeDef,
    ExternalEventsDetailTypeDef,
    FilterConditionTypeDef,
    GetBatchImportJobsResultTypeDef,
    GetBatchPredictionJobsResultTypeDef,
    GetDeleteEventsByEventTypeStatusResultTypeDef,
    GetDetectorsResultTypeDef,
    GetDetectorVersionResultTypeDef,
    GetEntityTypesResultTypeDef,
    GetEventPredictionMetadataResultTypeDef,
    GetEventPredictionResultTypeDef,
    GetEventResultTypeDef,
    GetEventTypesResultTypeDef,
    GetExternalModelsResultTypeDef,
    GetKMSEncryptionKeyResultTypeDef,
    GetLabelsResultTypeDef,
    GetListElementsResultTypeDef,
    GetListsMetadataResultTypeDef,
    GetModelsResultTypeDef,
    GetModelVersionResultTypeDef,
    GetOutcomesResultTypeDef,
    GetRulesResultTypeDef,
    GetVariablesResultTypeDef,
    IngestedEventsDetailTypeDef,
    ListEventPredictionsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    ModelEndpointDataBlobTypeDef,
    ModelInputConfigurationTypeDef,
    ModelOutputConfigurationUnionTypeDef,
    ModelVersionTypeDef,
    PredictionTimeRangeTypeDef,
    RuleTypeDef,
    TagTypeDef,
    TrainingDataSchemaUnionTypeDef,
    UpdateModelVersionResultTypeDef,
    UpdateRuleVersionResultTypeDef,
    VariableEntryTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("FraudDetectorClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class FraudDetectorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FraudDetectorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#exceptions)
        """

    async def batch_create_variable(
        self, *, variableEntries: Sequence[VariableEntryTypeDef], tags: Sequence[TagTypeDef] = ...
    ) -> BatchCreateVariableResultTypeDef:
        """
        Creates a batch of variables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.batch_create_variable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#batch_create_variable)
        """

    async def batch_get_variable(self, *, names: Sequence[str]) -> BatchGetVariableResultTypeDef:
        """
        Gets a batch of variables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.batch_get_variable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#batch_get_variable)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#can_paginate)
        """

    async def cancel_batch_import_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Cancels an in-progress batch import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.cancel_batch_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#cancel_batch_import_job)
        """

    async def cancel_batch_prediction_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Cancels the specified batch prediction job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.cancel_batch_prediction_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#cancel_batch_prediction_job)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#close)
        """

    async def create_batch_import_job(
        self,
        *,
        jobId: str,
        inputPath: str,
        outputPath: str,
        eventTypeName: str,
        iamRoleArn: str,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a batch import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_batch_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_batch_import_job)
        """

    async def create_batch_prediction_job(
        self,
        *,
        jobId: str,
        inputPath: str,
        outputPath: str,
        eventTypeName: str,
        detectorName: str,
        iamRoleArn: str,
        detectorVersion: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a batch prediction job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_batch_prediction_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_batch_prediction_job)
        """

    async def create_detector_version(
        self,
        *,
        detectorId: str,
        rules: Sequence[RuleTypeDef],
        description: str = ...,
        externalModelEndpoints: Sequence[str] = ...,
        modelVersions: Sequence[ModelVersionTypeDef] = ...,
        ruleExecutionMode: RuleExecutionModeType = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateDetectorVersionResultTypeDef:
        """
        Creates a detector version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_detector_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_detector_version)
        """

    async def create_list(
        self,
        *,
        name: str,
        elements: Sequence[str] = ...,
        variableType: str = ...,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_list)
        """

    async def create_model(
        self,
        *,
        modelId: str,
        modelType: ModelTypeEnumType,
        eventTypeName: str,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a model using the specified model type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_model)
        """

    async def create_model_version(
        self,
        *,
        modelId: str,
        modelType: ModelTypeEnumType,
        trainingDataSource: TrainingDataSourceEnumType,
        trainingDataSchema: TrainingDataSchemaUnionTypeDef,
        externalEventsDetail: ExternalEventsDetailTypeDef = ...,
        ingestedEventsDetail: IngestedEventsDetailTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateModelVersionResultTypeDef:
        """
        Creates a version of the model using the specified model type and model id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_model_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_model_version)
        """

    async def create_rule(
        self,
        *,
        ruleId: str,
        detectorId: str,
        expression: str,
        language: Literal["DETECTORPL"],
        outcomes: Sequence[str],
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateRuleResultTypeDef:
        """
        Creates a rule for use with the specified detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_rule)
        """

    async def create_variable(
        self,
        *,
        name: str,
        dataType: DataTypeType,
        dataSource: DataSourceType,
        defaultValue: str,
        description: str = ...,
        variableType: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a variable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.create_variable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#create_variable)
        """

    async def delete_batch_import_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Deletes the specified batch import job ID record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_batch_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_batch_import_job)
        """

    async def delete_batch_prediction_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Deletes a batch prediction job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_batch_prediction_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_batch_prediction_job)
        """

    async def delete_detector(self, *, detectorId: str) -> Dict[str, Any]:
        """
        Deletes the detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_detector)
        """

    async def delete_detector_version(
        self, *, detectorId: str, detectorVersionId: str
    ) -> Dict[str, Any]:
        """
        Deletes the detector version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_detector_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_detector_version)
        """

    async def delete_entity_type(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes an entity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_entity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_entity_type)
        """

    async def delete_event(
        self, *, eventId: str, eventTypeName: str, deleteAuditHistory: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_event)
        """

    async def delete_event_type(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes an event type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_event_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_event_type)
        """

    async def delete_events_by_event_type(
        self, *, eventTypeName: str
    ) -> DeleteEventsByEventTypeResultTypeDef:
        """
        Deletes all events of a particular event type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_events_by_event_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_events_by_event_type)
        """

    async def delete_external_model(self, *, modelEndpoint: str) -> Dict[str, Any]:
        """
        Removes a SageMaker model from Amazon Fraud Detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_external_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_external_model)
        """

    async def delete_label(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes a label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_label)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_label)
        """

    async def delete_list(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes the list, provided it is not used in a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_list)
        """

    async def delete_model(self, *, modelId: str, modelType: ModelTypeEnumType) -> Dict[str, Any]:
        """
        Deletes a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_model)
        """

    async def delete_model_version(
        self, *, modelId: str, modelType: ModelTypeEnumType, modelVersionNumber: str
    ) -> Dict[str, Any]:
        """
        Deletes a model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_model_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_model_version)
        """

    async def delete_outcome(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes an outcome.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_outcome)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_outcome)
        """

    async def delete_rule(self, *, rule: RuleTypeDef) -> Dict[str, Any]:
        """
        Deletes the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_rule)
        """

    async def delete_variable(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes a variable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.delete_variable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#delete_variable)
        """

    async def describe_detector(
        self, *, detectorId: str, nextToken: str = ..., maxResults: int = ...
    ) -> DescribeDetectorResultTypeDef:
        """
        Gets all versions for a specified detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.describe_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#describe_detector)
        """

    async def describe_model_versions(
        self,
        *,
        modelId: str = ...,
        modelVersionNumber: str = ...,
        modelType: ModelTypeEnumType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> DescribeModelVersionsResultTypeDef:
        """
        Gets all of the model versions for the specified model type or for the
        specified model type and model
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.describe_model_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#describe_model_versions)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#generate_presigned_url)
        """

    async def get_batch_import_jobs(
        self, *, jobId: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> GetBatchImportJobsResultTypeDef:
        """
        Gets all batch import jobs or a specific job of the specified ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_batch_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_batch_import_jobs)
        """

    async def get_batch_prediction_jobs(
        self, *, jobId: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> GetBatchPredictionJobsResultTypeDef:
        """
        Gets all batch prediction jobs or a specific job if you specify a job ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_batch_prediction_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_batch_prediction_jobs)
        """

    async def get_delete_events_by_event_type_status(
        self, *, eventTypeName: str
    ) -> GetDeleteEventsByEventTypeStatusResultTypeDef:
        """
        Retrieves the status of a `DeleteEventsByEventType` action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_delete_events_by_event_type_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_delete_events_by_event_type_status)
        """

    async def get_detector_version(
        self, *, detectorId: str, detectorVersionId: str
    ) -> GetDetectorVersionResultTypeDef:
        """
        Gets a particular detector version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_detector_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_detector_version)
        """

    async def get_detectors(
        self, *, detectorId: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetDetectorsResultTypeDef:
        """
        Gets all detectors or a single detector if a `detectorId` is specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_detectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_detectors)
        """

    async def get_entity_types(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetEntityTypesResultTypeDef:
        """
        Gets all entity types or a specific entity type if a name is specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_entity_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_entity_types)
        """

    async def get_event(self, *, eventId: str, eventTypeName: str) -> GetEventResultTypeDef:
        """
        Retrieves details of events stored with Amazon Fraud Detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_event)
        """

    async def get_event_prediction(
        self,
        *,
        detectorId: str,
        eventId: str,
        eventTypeName: str,
        entities: Sequence[EntityTypeDef],
        eventTimestamp: str,
        eventVariables: Mapping[str, str],
        detectorVersionId: str = ...,
        externalModelEndpointDataBlobs: Mapping[str, ModelEndpointDataBlobTypeDef] = ...,
    ) -> GetEventPredictionResultTypeDef:
        """
        Evaluates an event against a detector version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_event_prediction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_event_prediction)
        """

    async def get_event_prediction_metadata(
        self,
        *,
        eventId: str,
        eventTypeName: str,
        detectorId: str,
        detectorVersionId: str,
        predictionTimestamp: str,
    ) -> GetEventPredictionMetadataResultTypeDef:
        """
        Gets details of the past fraud predictions for the specified event ID, event
        type, detector ID, and detector version ID that was generated in the specified
        time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_event_prediction_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_event_prediction_metadata)
        """

    async def get_event_types(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetEventTypesResultTypeDef:
        """
        Gets all event types or a specific event type if name is provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_event_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_event_types)
        """

    async def get_external_models(
        self, *, modelEndpoint: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetExternalModelsResultTypeDef:
        """
        Gets the details for one or more Amazon SageMaker models that have been
        imported into the
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_external_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_external_models)
        """

    async def get_kms_encryption_key(self) -> GetKMSEncryptionKeyResultTypeDef:
        """
        Gets the encryption key if a KMS key has been specified to be used to encrypt
        content in Amazon Fraud
        Detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_kms_encryption_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_kms_encryption_key)
        """

    async def get_labels(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetLabelsResultTypeDef:
        """
        Gets all labels or a specific label if name is provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_labels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_labels)
        """

    async def get_list_elements(
        self, *, name: str, nextToken: str = ..., maxResults: int = ...
    ) -> GetListElementsResultTypeDef:
        """
        Gets all the elements in the specified list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_list_elements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_list_elements)
        """

    async def get_lists_metadata(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetListsMetadataResultTypeDef:
        """
        Gets the metadata of either all the lists under the account or the specified
        list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_lists_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_lists_metadata)
        """

    async def get_model_version(
        self, *, modelId: str, modelType: ModelTypeEnumType, modelVersionNumber: str
    ) -> GetModelVersionResultTypeDef:
        """
        Gets the details of the specified model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_model_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_model_version)
        """

    async def get_models(
        self,
        *,
        modelId: str = ...,
        modelType: ModelTypeEnumType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetModelsResultTypeDef:
        """
        Gets one or more models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_models)
        """

    async def get_outcomes(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetOutcomesResultTypeDef:
        """
        Gets one or more outcomes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_outcomes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_outcomes)
        """

    async def get_rules(
        self,
        *,
        detectorId: str,
        ruleId: str = ...,
        ruleVersion: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetRulesResultTypeDef:
        """
        Get all rules for a detector (paginated) if `ruleId` and `ruleVersion` are not
        specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_rules)
        """

    async def get_variables(
        self, *, name: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> GetVariablesResultTypeDef:
        """
        Gets all of the variables or the specific variable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.get_variables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#get_variables)
        """

    async def list_event_predictions(
        self,
        *,
        eventId: FilterConditionTypeDef = ...,
        eventType: FilterConditionTypeDef = ...,
        detectorId: FilterConditionTypeDef = ...,
        detectorVersionId: FilterConditionTypeDef = ...,
        predictionTimeRange: PredictionTimeRangeTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListEventPredictionsResultTypeDef:
        """
        Gets a list of past predictions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.list_event_predictions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#list_event_predictions)
        """

    async def list_tags_for_resource(
        self, *, resourceARN: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTagsForResourceResultTypeDef:
        """
        Lists all tags associated with the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#list_tags_for_resource)
        """

    async def put_detector(
        self,
        *,
        detectorId: str,
        eventTypeName: str,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates or updates a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_detector)
        """

    async def put_entity_type(
        self, *, name: str, description: str = ..., tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates an entity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_entity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_entity_type)
        """

    async def put_event_type(
        self,
        *,
        name: str,
        eventVariables: Sequence[str],
        entityTypes: Sequence[str],
        description: str = ...,
        labels: Sequence[str] = ...,
        eventIngestion: EventIngestionType = ...,
        tags: Sequence[TagTypeDef] = ...,
        eventOrchestration: EventOrchestrationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Creates or updates an event type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_event_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_event_type)
        """

    async def put_external_model(
        self,
        *,
        modelEndpoint: str,
        modelSource: Literal["SAGEMAKER"],
        invokeModelEndpointRoleArn: str,
        inputConfiguration: ModelInputConfigurationTypeDef,
        outputConfiguration: ModelOutputConfigurationUnionTypeDef,
        modelEndpointStatus: ModelEndpointStatusType,
        tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates or updates an Amazon SageMaker model endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_external_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_external_model)
        """

    async def put_kms_encryption_key(self, *, kmsEncryptionKeyArn: str) -> Dict[str, Any]:
        """
        Specifies the KMS key to be used to encrypt content in Amazon Fraud Detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_kms_encryption_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_kms_encryption_key)
        """

    async def put_label(
        self, *, name: str, description: str = ..., tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_label)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_label)
        """

    async def put_outcome(
        self, *, name: str, description: str = ..., tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates an outcome.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.put_outcome)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#put_outcome)
        """

    async def send_event(
        self,
        *,
        eventId: str,
        eventTypeName: str,
        eventTimestamp: str,
        eventVariables: Mapping[str, str],
        entities: Sequence[EntityTypeDef],
        assignedLabel: str = ...,
        labelTimestamp: str = ...,
    ) -> Dict[str, Any]:
        """
        Stores events in Amazon Fraud Detector without generating fraud predictions for
        those
        events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.send_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#send_event)
        """

    async def tag_resource(self, *, resourceARN: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Assigns tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#untag_resource)
        """

    async def update_detector_version(
        self,
        *,
        detectorId: str,
        detectorVersionId: str,
        externalModelEndpoints: Sequence[str],
        rules: Sequence[RuleTypeDef],
        description: str = ...,
        modelVersions: Sequence[ModelVersionTypeDef] = ...,
        ruleExecutionMode: RuleExecutionModeType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a detector version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_detector_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_detector_version)
        """

    async def update_detector_version_metadata(
        self, *, detectorId: str, detectorVersionId: str, description: str
    ) -> Dict[str, Any]:
        """
        Updates the detector version's description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_detector_version_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_detector_version_metadata)
        """

    async def update_detector_version_status(
        self, *, detectorId: str, detectorVersionId: str, status: DetectorVersionStatusType
    ) -> Dict[str, Any]:
        """
        Updates the detector version's status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_detector_version_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_detector_version_status)
        """

    async def update_event_label(
        self, *, eventId: str, eventTypeName: str, assignedLabel: str, labelTimestamp: str
    ) -> Dict[str, Any]:
        """
        Updates the specified event with a new label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_event_label)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_event_label)
        """

    async def update_list(
        self,
        *,
        name: str,
        elements: Sequence[str] = ...,
        description: str = ...,
        updateMode: ListUpdateModeType = ...,
        variableType: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_list)
        """

    async def update_model(
        self, *, modelId: str, modelType: ModelTypeEnumType, description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates model description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_model)
        """

    async def update_model_version(
        self,
        *,
        modelId: str,
        modelType: ModelTypeEnumType,
        majorVersionNumber: str,
        externalEventsDetail: ExternalEventsDetailTypeDef = ...,
        ingestedEventsDetail: IngestedEventsDetailTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> UpdateModelVersionResultTypeDef:
        """
        Updates a model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_model_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_model_version)
        """

    async def update_model_version_status(
        self,
        *,
        modelId: str,
        modelType: ModelTypeEnumType,
        modelVersionNumber: str,
        status: ModelVersionStatusType,
    ) -> Dict[str, Any]:
        """
        Updates the status of a model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_model_version_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_model_version_status)
        """

    async def update_rule_metadata(self, *, rule: RuleTypeDef, description: str) -> Dict[str, Any]:
        """
        Updates a rule's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_rule_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_rule_metadata)
        """

    async def update_rule_version(
        self,
        *,
        rule: RuleTypeDef,
        expression: str,
        language: Literal["DETECTORPL"],
        outcomes: Sequence[str],
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> UpdateRuleVersionResultTypeDef:
        """
        Updates a rule version resulting in a new rule version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_rule_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_rule_version)
        """

    async def update_variable(
        self, *, name: str, defaultValue: str = ..., description: str = ..., variableType: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a variable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client.update_variable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/#update_variable)
        """

    async def __aenter__(self) -> "FraudDetectorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/frauddetector.html#FraudDetector.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_frauddetector/client/)
        """
