"""
Type annotations for pi service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pi.client import PIClient

    session = get_session()
    async with session.create_client("pi") as client:
        client: PIClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import FineGrainedActionType, PeriodAlignmentType, ServiceTypeType, TextFormatType
from .type_defs import (
    CreatePerformanceAnalysisReportResponseTypeDef,
    DescribeDimensionKeysResponseTypeDef,
    DimensionGroupTypeDef,
    GetDimensionKeyDetailsResponseTypeDef,
    GetPerformanceAnalysisReportResponseTypeDef,
    GetResourceMetadataResponseTypeDef,
    GetResourceMetricsResponseTypeDef,
    ListAvailableResourceDimensionsResponseTypeDef,
    ListAvailableResourceMetricsResponseTypeDef,
    ListPerformanceAnalysisReportsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MetricQueryTypeDef,
    TagTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("PIClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]


class PIClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#close)
        """

    async def create_performance_analysis_report(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreatePerformanceAnalysisReportResponseTypeDef:
        """
        Creates a new performance analysis report for a specific time period for the DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.create_performance_analysis_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#create_performance_analysis_report)
        """

    async def delete_performance_analysis_report(
        self, *, ServiceType: ServiceTypeType, Identifier: str, AnalysisReportId: str
    ) -> Dict[str, Any]:
        """
        Deletes a performance analysis report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.delete_performance_analysis_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#delete_performance_analysis_report)
        """

    async def describe_dimension_keys(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        Metric: str,
        GroupBy: DimensionGroupTypeDef,
        PeriodInSeconds: int = ...,
        AdditionalMetrics: Sequence[str] = ...,
        PartitionBy: DimensionGroupTypeDef = ...,
        Filter: Mapping[str, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeDimensionKeysResponseTypeDef:
        """
        For a specific time period, retrieve the top `N` dimension keys for a metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.describe_dimension_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#describe_dimension_keys)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#generate_presigned_url)
        """

    async def get_dimension_key_details(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        Group: str,
        GroupIdentifier: str,
        RequestedDimensions: Sequence[str] = ...,
    ) -> GetDimensionKeyDetailsResponseTypeDef:
        """
        Get the attributes of the specified dimension group for a DB instance or data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_dimension_key_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#get_dimension_key_details)
        """

    async def get_performance_analysis_report(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        AnalysisReportId: str,
        TextFormat: TextFormatType = ...,
        AcceptLanguage: Literal["EN_US"] = ...,
    ) -> GetPerformanceAnalysisReportResponseTypeDef:
        """
        Retrieves the report including the report ID, status, time details, and the
        insights with
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_performance_analysis_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#get_performance_analysis_report)
        """

    async def get_resource_metadata(
        self, *, ServiceType: ServiceTypeType, Identifier: str
    ) -> GetResourceMetadataResponseTypeDef:
        """
        Retrieve the metadata for different features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_resource_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#get_resource_metadata)
        """

    async def get_resource_metrics(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        MetricQueries: Sequence[MetricQueryTypeDef],
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        PeriodInSeconds: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        PeriodAlignment: PeriodAlignmentType = ...,
    ) -> GetResourceMetricsResponseTypeDef:
        """
        Retrieve Performance Insights metrics for a set of data sources over a time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.get_resource_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#get_resource_metrics)
        """

    async def list_available_resource_dimensions(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        Metrics: Sequence[str],
        MaxResults: int = ...,
        NextToken: str = ...,
        AuthorizedActions: Sequence[FineGrainedActionType] = ...,
    ) -> ListAvailableResourceDimensionsResponseTypeDef:
        """
        Retrieve the dimensions that can be queried for each specified metric type on a
        specified DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_available_resource_dimensions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#list_available_resource_dimensions)
        """

    async def list_available_resource_metrics(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        MetricTypes: Sequence[str],
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListAvailableResourceMetricsResponseTypeDef:
        """
        Retrieve metrics of the specified types that can be queried for a specified DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_available_resource_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#list_available_resource_metrics)
        """

    async def list_performance_analysis_reports(
        self,
        *,
        ServiceType: ServiceTypeType,
        Identifier: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        ListTags: bool = ...,
    ) -> ListPerformanceAnalysisReportsResponseTypeDef:
        """
        Lists all the analysis reports created for the DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_performance_analysis_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#list_performance_analysis_reports)
        """

    async def list_tags_for_resource(
        self, *, ServiceType: ServiceTypeType, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all the metadata tags associated with Amazon RDS Performance Insights
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, *, ServiceType: ServiceTypeType, ResourceARN: str, Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds metadata tags to the Amazon RDS Performance Insights resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#tag_resource)
        """

    async def untag_resource(
        self, *, ServiceType: ServiceTypeType, ResourceARN: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Deletes the metadata tags from the Amazon RDS Performance Insights resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/#untag_resource)
        """

    async def __aenter__(self) -> "PIClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pi.html#PI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pi/client/)
        """
