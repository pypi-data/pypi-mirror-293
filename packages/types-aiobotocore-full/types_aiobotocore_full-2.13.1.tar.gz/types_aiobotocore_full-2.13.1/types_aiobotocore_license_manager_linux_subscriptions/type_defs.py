"""
Type annotations for license-manager-linux-subscriptions service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/type_defs/)

Usage::

    ```python
    from types_aiobotocore_license_manager_linux_subscriptions.type_defs import FilterTypeDef

    data: FilterTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

from .literals import (
    LinuxSubscriptionsDiscoveryType,
    OperatorType,
    OrganizationIntegrationType,
    StatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FilterTypeDef",
    "LinuxSubscriptionsDiscoverySettingsOutputTypeDef",
    "ResponseMetadataTypeDef",
    "InstanceTypeDef",
    "LinuxSubscriptionsDiscoverySettingsTypeDef",
    "PaginatorConfigTypeDef",
    "SubscriptionTypeDef",
    "ListLinuxSubscriptionInstancesRequestRequestTypeDef",
    "ListLinuxSubscriptionsRequestRequestTypeDef",
    "GetServiceSettingsResponseTypeDef",
    "UpdateServiceSettingsResponseTypeDef",
    "ListLinuxSubscriptionInstancesResponseTypeDef",
    "UpdateServiceSettingsRequestRequestTypeDef",
    "ListLinuxSubscriptionInstancesRequestListLinuxSubscriptionInstancesPaginateTypeDef",
    "ListLinuxSubscriptionsRequestListLinuxSubscriptionsPaginateTypeDef",
    "ListLinuxSubscriptionsResponseTypeDef",
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": NotRequired[str],
        "Operator": NotRequired[OperatorType],
        "Values": NotRequired[Sequence[str]],
    },
)
LinuxSubscriptionsDiscoverySettingsOutputTypeDef = TypedDict(
    "LinuxSubscriptionsDiscoverySettingsOutputTypeDef",
    {
        "OrganizationIntegration": OrganizationIntegrationType,
        "SourceRegions": List[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "AccountID": NotRequired[str],
        "AmiId": NotRequired[str],
        "InstanceID": NotRequired[str],
        "InstanceType": NotRequired[str],
        "LastUpdatedTime": NotRequired[str],
        "ProductCode": NotRequired[List[str]],
        "Region": NotRequired[str],
        "Status": NotRequired[str],
        "SubscriptionName": NotRequired[str],
        "UsageOperation": NotRequired[str],
    },
)
LinuxSubscriptionsDiscoverySettingsTypeDef = TypedDict(
    "LinuxSubscriptionsDiscoverySettingsTypeDef",
    {
        "OrganizationIntegration": OrganizationIntegrationType,
        "SourceRegions": Sequence[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "InstanceCount": NotRequired[int],
        "Name": NotRequired[str],
        "Type": NotRequired[str],
    },
)
ListLinuxSubscriptionInstancesRequestRequestTypeDef = TypedDict(
    "ListLinuxSubscriptionInstancesRequestRequestTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListLinuxSubscriptionsRequestRequestTypeDef = TypedDict(
    "ListLinuxSubscriptionsRequestRequestTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
GetServiceSettingsResponseTypeDef = TypedDict(
    "GetServiceSettingsResponseTypeDef",
    {
        "HomeRegions": List[str],
        "LinuxSubscriptionsDiscovery": LinuxSubscriptionsDiscoveryType,
        "LinuxSubscriptionsDiscoverySettings": LinuxSubscriptionsDiscoverySettingsOutputTypeDef,
        "Status": StatusType,
        "StatusMessage": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateServiceSettingsResponseTypeDef = TypedDict(
    "UpdateServiceSettingsResponseTypeDef",
    {
        "HomeRegions": List[str],
        "LinuxSubscriptionsDiscovery": LinuxSubscriptionsDiscoveryType,
        "LinuxSubscriptionsDiscoverySettings": LinuxSubscriptionsDiscoverySettingsOutputTypeDef,
        "Status": StatusType,
        "StatusMessage": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListLinuxSubscriptionInstancesResponseTypeDef = TypedDict(
    "ListLinuxSubscriptionInstancesResponseTypeDef",
    {
        "Instances": List[InstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
UpdateServiceSettingsRequestRequestTypeDef = TypedDict(
    "UpdateServiceSettingsRequestRequestTypeDef",
    {
        "LinuxSubscriptionsDiscovery": LinuxSubscriptionsDiscoveryType,
        "LinuxSubscriptionsDiscoverySettings": LinuxSubscriptionsDiscoverySettingsTypeDef,
        "AllowUpdate": NotRequired[bool],
    },
)
ListLinuxSubscriptionInstancesRequestListLinuxSubscriptionInstancesPaginateTypeDef = TypedDict(
    "ListLinuxSubscriptionInstancesRequestListLinuxSubscriptionInstancesPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLinuxSubscriptionsRequestListLinuxSubscriptionsPaginateTypeDef = TypedDict(
    "ListLinuxSubscriptionsRequestListLinuxSubscriptionsPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLinuxSubscriptionsResponseTypeDef = TypedDict(
    "ListLinuxSubscriptionsResponseTypeDef",
    {
        "Subscriptions": List[SubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
