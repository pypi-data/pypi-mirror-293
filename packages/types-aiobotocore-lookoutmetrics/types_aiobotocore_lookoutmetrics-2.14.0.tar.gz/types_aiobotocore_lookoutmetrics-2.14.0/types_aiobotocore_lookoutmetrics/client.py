"""
Type annotations for lookoutmetrics service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutmetrics.client import LookoutMetricsClient

    session = get_session()
    async with session.create_client("lookoutmetrics") as client:
        client: LookoutMetricsClient
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import FrequencyType, RelationshipTypeType
from .type_defs import (
    ActionTypeDef,
    AlertFiltersUnionTypeDef,
    AnomalyDetectorConfigTypeDef,
    AnomalyGroupTimeSeriesFeedbackTypeDef,
    AnomalyGroupTimeSeriesTypeDef,
    AutoDetectionMetricSourceTypeDef,
    CreateAlertResponseTypeDef,
    CreateAnomalyDetectorResponseTypeDef,
    CreateMetricSetResponseTypeDef,
    DescribeAlertResponseTypeDef,
    DescribeAnomalyDetectionExecutionsResponseTypeDef,
    DescribeAnomalyDetectorResponseTypeDef,
    DescribeMetricSetResponseTypeDef,
    DetectMetricSetConfigResponseTypeDef,
    GetAnomalyGroupResponseTypeDef,
    GetDataQualityMetricsResponseTypeDef,
    GetFeedbackResponseTypeDef,
    GetSampleDataResponseTypeDef,
    ListAlertsResponseTypeDef,
    ListAnomalyDetectorsResponseTypeDef,
    ListAnomalyGroupRelatedMetricsResponseTypeDef,
    ListAnomalyGroupSummariesResponseTypeDef,
    ListAnomalyGroupTimeSeriesResponseTypeDef,
    ListMetricSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MetricSetDimensionFilterUnionTypeDef,
    MetricSourceUnionTypeDef,
    MetricTypeDef,
    SampleDataS3SourceConfigTypeDef,
    TimestampColumnTypeDef,
    UpdateAlertResponseTypeDef,
    UpdateAnomalyDetectorResponseTypeDef,
    UpdateMetricSetResponseTypeDef,
)

__all__ = ("LookoutMetricsClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LookoutMetricsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutMetricsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#exceptions)
        """

    async def activate_anomaly_detector(self, *, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        Activates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.activate_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#activate_anomaly_detector)
        """

    async def back_test_anomaly_detector(self, *, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        Runs a backtest for anomaly detection for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.back_test_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#back_test_anomaly_detector)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#close)
        """

    async def create_alert(
        self,
        *,
        AlertName: str,
        AnomalyDetectorArn: str,
        Action: ActionTypeDef,
        AlertSensitivityThreshold: int = ...,
        AlertDescription: str = ...,
        Tags: Mapping[str, str] = ...,
        AlertFilters: AlertFiltersUnionTypeDef = ...,
    ) -> CreateAlertResponseTypeDef:
        """
        Creates an alert for an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_alert)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_alert)
        """

    async def create_anomaly_detector(
        self,
        *,
        AnomalyDetectorName: str,
        AnomalyDetectorConfig: AnomalyDetectorConfigTypeDef,
        AnomalyDetectorDescription: str = ...,
        KmsKeyArn: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateAnomalyDetectorResponseTypeDef:
        """
        Creates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_anomaly_detector)
        """

    async def create_metric_set(
        self,
        *,
        AnomalyDetectorArn: str,
        MetricSetName: str,
        MetricList: Sequence[MetricTypeDef],
        MetricSource: MetricSourceUnionTypeDef,
        MetricSetDescription: str = ...,
        Offset: int = ...,
        TimestampColumn: TimestampColumnTypeDef = ...,
        DimensionList: Sequence[str] = ...,
        MetricSetFrequency: FrequencyType = ...,
        Timezone: str = ...,
        Tags: Mapping[str, str] = ...,
        DimensionFilterList: Sequence[MetricSetDimensionFilterUnionTypeDef] = ...,
    ) -> CreateMetricSetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.create_metric_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_metric_set)
        """

    async def deactivate_anomaly_detector(self, *, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        Deactivates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.deactivate_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#deactivate_anomaly_detector)
        """

    async def delete_alert(self, *, AlertArn: str) -> Dict[str, Any]:
        """
        Deletes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.delete_alert)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#delete_alert)
        """

    async def delete_anomaly_detector(self, *, AnomalyDetectorArn: str) -> Dict[str, Any]:
        """
        Deletes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.delete_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#delete_anomaly_detector)
        """

    async def describe_alert(self, *, AlertArn: str) -> DescribeAlertResponseTypeDef:
        """
        Describes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_alert)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_alert)
        """

    async def describe_anomaly_detection_executions(
        self,
        *,
        AnomalyDetectorArn: str,
        Timestamp: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAnomalyDetectionExecutionsResponseTypeDef:
        """
        Returns information about the status of the specified anomaly detection jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_anomaly_detection_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_anomaly_detection_executions)
        """

    async def describe_anomaly_detector(
        self, *, AnomalyDetectorArn: str
    ) -> DescribeAnomalyDetectorResponseTypeDef:
        """
        Describes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_anomaly_detector)
        """

    async def describe_metric_set(self, *, MetricSetArn: str) -> DescribeMetricSetResponseTypeDef:
        """
        Describes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.describe_metric_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_metric_set)
        """

    async def detect_metric_set_config(
        self,
        *,
        AnomalyDetectorArn: str,
        AutoDetectionMetricSource: AutoDetectionMetricSourceTypeDef,
    ) -> DetectMetricSetConfigResponseTypeDef:
        """
        Detects an Amazon S3 dataset's file format, interval, and offset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.detect_metric_set_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#detect_metric_set_config)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#generate_presigned_url)
        """

    async def get_anomaly_group(
        self, *, AnomalyGroupId: str, AnomalyDetectorArn: str
    ) -> GetAnomalyGroupResponseTypeDef:
        """
        Returns details about a group of anomalous metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_anomaly_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_anomaly_group)
        """

    async def get_data_quality_metrics(
        self, *, AnomalyDetectorArn: str, MetricSetArn: str = ...
    ) -> GetDataQualityMetricsResponseTypeDef:
        """
        Returns details about the requested data quality metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_data_quality_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_data_quality_metrics)
        """

    async def get_feedback(
        self,
        *,
        AnomalyDetectorArn: str,
        AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesTypeDef,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> GetFeedbackResponseTypeDef:
        """
        Get feedback for an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_feedback)
        """

    async def get_sample_data(
        self, *, S3SourceConfig: SampleDataS3SourceConfigTypeDef = ...
    ) -> GetSampleDataResponseTypeDef:
        """
        Returns a selection of sample records from an Amazon S3 datasource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.get_sample_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_sample_data)
        """

    async def list_alerts(
        self, *, AnomalyDetectorArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListAlertsResponseTypeDef:
        """
        Lists the alerts attached to a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_alerts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_alerts)
        """

    async def list_anomaly_detectors(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAnomalyDetectorsResponseTypeDef:
        """
        Lists the detectors in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_detectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_detectors)
        """

    async def list_anomaly_group_related_metrics(
        self,
        *,
        AnomalyDetectorArn: str,
        AnomalyGroupId: str,
        RelationshipTypeFilter: RelationshipTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListAnomalyGroupRelatedMetricsResponseTypeDef:
        """
        Returns a list of measures that are potential causes or effects of an anomaly
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_group_related_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_related_metrics)
        """

    async def list_anomaly_group_summaries(
        self,
        *,
        AnomalyDetectorArn: str,
        SensitivityThreshold: int,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListAnomalyGroupSummariesResponseTypeDef:
        """
        Returns a list of anomaly groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_group_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_summaries)
        """

    async def list_anomaly_group_time_series(
        self,
        *,
        AnomalyDetectorArn: str,
        AnomalyGroupId: str,
        MetricName: str,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListAnomalyGroupTimeSeriesResponseTypeDef:
        """
        Gets a list of anomalous metrics for a measure in an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_anomaly_group_time_series)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_time_series)
        """

    async def list_metric_sets(
        self, *, AnomalyDetectorArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListMetricSetsResponseTypeDef:
        """
        Lists the datasets in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_metric_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_metric_sets)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        for a detector, dataset, or
        alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_tags_for_resource)
        """

    async def put_feedback(
        self,
        *,
        AnomalyDetectorArn: str,
        AnomalyGroupTimeSeriesFeedback: AnomalyGroupTimeSeriesFeedbackTypeDef,
    ) -> Dict[str, Any]:
        """
        Add feedback for an anomalous metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.put_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#put_feedback)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        to a detector, dataset, or
        alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes
        [tags](https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html)
        from a detector, dataset, or
        alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#untag_resource)
        """

    async def update_alert(
        self,
        *,
        AlertArn: str,
        AlertDescription: str = ...,
        AlertSensitivityThreshold: int = ...,
        Action: ActionTypeDef = ...,
        AlertFilters: AlertFiltersUnionTypeDef = ...,
    ) -> UpdateAlertResponseTypeDef:
        """
        Make changes to an existing alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.update_alert)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_alert)
        """

    async def update_anomaly_detector(
        self,
        *,
        AnomalyDetectorArn: str,
        KmsKeyArn: str = ...,
        AnomalyDetectorDescription: str = ...,
        AnomalyDetectorConfig: AnomalyDetectorConfigTypeDef = ...,
    ) -> UpdateAnomalyDetectorResponseTypeDef:
        """
        Updates a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.update_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_anomaly_detector)
        """

    async def update_metric_set(
        self,
        *,
        MetricSetArn: str,
        MetricSetDescription: str = ...,
        MetricList: Sequence[MetricTypeDef] = ...,
        Offset: int = ...,
        TimestampColumn: TimestampColumnTypeDef = ...,
        DimensionList: Sequence[str] = ...,
        MetricSetFrequency: FrequencyType = ...,
        MetricSource: MetricSourceUnionTypeDef = ...,
        DimensionFilterList: Sequence[MetricSetDimensionFilterUnionTypeDef] = ...,
    ) -> UpdateMetricSetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client.update_metric_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_metric_set)
        """

    async def __aenter__(self) -> "LookoutMetricsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
        """
