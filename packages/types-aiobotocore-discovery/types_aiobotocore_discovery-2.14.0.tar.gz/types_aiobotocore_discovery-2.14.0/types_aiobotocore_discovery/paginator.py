"""
Type annotations for discovery service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_discovery.client import ApplicationDiscoveryServiceClient
    from types_aiobotocore_discovery.paginator import (
        DescribeAgentsPaginator,
        DescribeContinuousExportsPaginator,
        DescribeExportConfigurationsPaginator,
        DescribeExportTasksPaginator,
        DescribeImportTasksPaginator,
        DescribeTagsPaginator,
        ListConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("discovery") as client:
        client: ApplicationDiscoveryServiceClient

        describe_agents_paginator: DescribeAgentsPaginator = client.get_paginator("describe_agents")
        describe_continuous_exports_paginator: DescribeContinuousExportsPaginator = client.get_paginator("describe_continuous_exports")
        describe_export_configurations_paginator: DescribeExportConfigurationsPaginator = client.get_paginator("describe_export_configurations")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_import_tasks_paginator: DescribeImportTasksPaginator = client.get_paginator("describe_import_tasks")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ConfigurationItemTypeType
from .type_defs import (
    DescribeAgentsResponseTypeDef,
    DescribeContinuousExportsResponseTypeDef,
    DescribeExportConfigurationsResponseTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeImportTasksResponseTypeDef,
    DescribeTagsResponseTypeDef,
    ExportFilterTypeDef,
    FilterTypeDef,
    ImportTaskFilterTypeDef,
    ListConfigurationsResponseTypeDef,
    OrderByElementTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
)

__all__ = (
    "DescribeAgentsPaginator",
    "DescribeContinuousExportsPaginator",
    "DescribeExportConfigurationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeImportTasksPaginator",
    "DescribeTagsPaginator",
    "ListConfigurationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAgentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeagentspaginator)
    """

    def paginate(
        self,
        *,
        agentIds: Sequence[str] = ...,
        filters: Sequence[FilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeagentspaginator)
        """


class DescribeContinuousExportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describecontinuousexportspaginator)
    """

    def paginate(
        self, *, exportIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeContinuousExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describecontinuousexportspaginator)
        """


class DescribeExportConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexportconfigurationspaginator)
    """

    def paginate(
        self, *, exportIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeExportConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexportconfigurationspaginator)
        """


class DescribeExportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexporttaskspaginator)
    """

    def paginate(
        self,
        *,
        exportIds: Sequence[str] = ...,
        filters: Sequence[ExportFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexporttaskspaginator)
        """


class DescribeImportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeimporttaskspaginator)
    """

    def paginate(
        self,
        *,
        filters: Sequence[ImportTaskFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeImportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeimporttaskspaginator)
        """


class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describetagspaginator)
    """

    def paginate(
        self,
        *,
        filters: Sequence[TagFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describetagspaginator)
        """


class ListConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.ListConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#listconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        configurationType: ConfigurationItemTypeType,
        filters: Sequence[FilterTypeDef] = ...,
        orderBy: Sequence[OrderByElementTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.ListConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#listconfigurationspaginator)
        """
