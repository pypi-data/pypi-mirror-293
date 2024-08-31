"""
Type annotations for bedrock-agent service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/type_defs/)

Usage::

    ```python
    from types_aiobotocore_bedrock_agent.type_defs import S3IdentifierTypeDef

    data: S3IdentifierTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ActionGroupStateType,
    AgentAliasStatusType,
    AgentStatusType,
    ChunkingStrategyType,
    CreationModeType,
    DataDeletionPolicyType,
    DataSourceStatusType,
    IngestionJobSortByAttributeType,
    IngestionJobStatusType,
    KnowledgeBaseStateType,
    KnowledgeBaseStatusType,
    KnowledgeBaseStorageTypeType,
    PromptStateType,
    PromptTypeType,
    SortOrderType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "S3IdentifierTypeDef",
    "ActionGroupExecutorTypeDef",
    "ActionGroupSummaryTypeDef",
    "AgentAliasRoutingConfigurationListItemTypeDef",
    "AgentKnowledgeBaseSummaryTypeDef",
    "AgentKnowledgeBaseTypeDef",
    "GuardrailConfigurationTypeDef",
    "AssociateAgentKnowledgeBaseRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BedrockEmbeddingModelConfigurationTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "S3DataSourceConfigurationOutputTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "DataSourceSummaryTypeDef",
    "DeleteAgentActionGroupRequestRequestTypeDef",
    "DeleteAgentAliasRequestRequestTypeDef",
    "DeleteAgentRequestRequestTypeDef",
    "DeleteAgentVersionRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DisassociateAgentKnowledgeBaseRequestRequestTypeDef",
    "ParameterDetailTypeDef",
    "GetAgentActionGroupRequestRequestTypeDef",
    "GetAgentAliasRequestRequestTypeDef",
    "GetAgentKnowledgeBaseRequestRequestTypeDef",
    "GetAgentRequestRequestTypeDef",
    "GetAgentVersionRequestRequestTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetIngestionJobRequestRequestTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "InferenceConfigurationOutputTypeDef",
    "InferenceConfigurationTypeDef",
    "IngestionJobFilterTypeDef",
    "IngestionJobSortByTypeDef",
    "IngestionJobStatisticsTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListAgentActionGroupsRequestRequestTypeDef",
    "ListAgentAliasesRequestRequestTypeDef",
    "ListAgentKnowledgeBasesRequestRequestTypeDef",
    "ListAgentVersionsRequestRequestTypeDef",
    "ListAgentsRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MongoDbAtlasFieldMappingTypeDef",
    "OpenSearchServerlessFieldMappingTypeDef",
    "PineconeFieldMappingTypeDef",
    "PrepareAgentRequestRequestTypeDef",
    "RdsFieldMappingTypeDef",
    "RedisEnterpriseCloudFieldMappingTypeDef",
    "StartIngestionJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentKnowledgeBaseRequestRequestTypeDef",
    "APISchemaTypeDef",
    "AgentAliasHistoryEventTypeDef",
    "AgentAliasSummaryTypeDef",
    "CreateAgentAliasRequestRequestTypeDef",
    "UpdateAgentAliasRequestRequestTypeDef",
    "AgentSummaryTypeDef",
    "AgentVersionSummaryTypeDef",
    "AssociateAgentKnowledgeBaseResponseTypeDef",
    "DeleteAgentAliasResponseTypeDef",
    "DeleteAgentResponseTypeDef",
    "DeleteAgentVersionResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteKnowledgeBaseResponseTypeDef",
    "GetAgentKnowledgeBaseResponseTypeDef",
    "ListAgentActionGroupsResponseTypeDef",
    "ListAgentKnowledgeBasesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PrepareAgentResponseTypeDef",
    "UpdateAgentKnowledgeBaseResponseTypeDef",
    "EmbeddingModelConfigurationTypeDef",
    "ChunkingConfigurationTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceConfigurationTypeDef",
    "ListDataSourcesResponseTypeDef",
    "FunctionOutputTypeDef",
    "FunctionTypeDef",
    "PromptConfigurationOutputTypeDef",
    "PromptConfigurationTypeDef",
    "ListIngestionJobsRequestRequestTypeDef",
    "IngestionJobSummaryTypeDef",
    "IngestionJobTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef",
    "ListAgentAliasesRequestListAgentAliasesPaginateTypeDef",
    "ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef",
    "ListAgentVersionsRequestListAgentVersionsPaginateTypeDef",
    "ListAgentsRequestListAgentsPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListIngestionJobsRequestListIngestionJobsPaginateTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "MongoDbAtlasConfigurationTypeDef",
    "OpenSearchServerlessConfigurationTypeDef",
    "PineconeConfigurationTypeDef",
    "RdsConfigurationTypeDef",
    "RedisEnterpriseCloudConfigurationTypeDef",
    "AgentAliasTypeDef",
    "ListAgentAliasesResponseTypeDef",
    "ListAgentsResponseTypeDef",
    "ListAgentVersionsResponseTypeDef",
    "VectorKnowledgeBaseConfigurationTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "FunctionSchemaOutputTypeDef",
    "FunctionSchemaTypeDef",
    "PromptOverrideConfigurationOutputTypeDef",
    "PromptOverrideConfigurationTypeDef",
    "ListIngestionJobsResponseTypeDef",
    "GetIngestionJobResponseTypeDef",
    "StartIngestionJobResponseTypeDef",
    "StorageConfigurationTypeDef",
    "CreateAgentAliasResponseTypeDef",
    "GetAgentAliasResponseTypeDef",
    "UpdateAgentAliasResponseTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "DataSourceTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "AgentActionGroupTypeDef",
    "CreateAgentActionGroupRequestRequestTypeDef",
    "UpdateAgentActionGroupRequestRequestTypeDef",
    "AgentTypeDef",
    "AgentVersionTypeDef",
    "CreateAgentRequestRequestTypeDef",
    "UpdateAgentRequestRequestTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "KnowledgeBaseTypeDef",
    "UpdateKnowledgeBaseRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "GetDataSourceResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "CreateAgentActionGroupResponseTypeDef",
    "GetAgentActionGroupResponseTypeDef",
    "UpdateAgentActionGroupResponseTypeDef",
    "CreateAgentResponseTypeDef",
    "GetAgentResponseTypeDef",
    "UpdateAgentResponseTypeDef",
    "GetAgentVersionResponseTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "UpdateKnowledgeBaseResponseTypeDef",
)

S3IdentifierTypeDef = TypedDict(
    "S3IdentifierTypeDef",
    {
        "s3BucketName": NotRequired[str],
        "s3ObjectKey": NotRequired[str],
    },
)
ActionGroupExecutorTypeDef = TypedDict(
    "ActionGroupExecutorTypeDef",
    {
        "customControl": NotRequired[Literal["RETURN_CONTROL"]],
        "lambda": NotRequired[str],
    },
)
ActionGroupSummaryTypeDef = TypedDict(
    "ActionGroupSummaryTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "actionGroupState": ActionGroupStateType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
AgentAliasRoutingConfigurationListItemTypeDef = TypedDict(
    "AgentAliasRoutingConfigurationListItemTypeDef",
    {
        "agentVersion": NotRequired[str],
        "provisionedThroughput": NotRequired[str],
    },
)
AgentKnowledgeBaseSummaryTypeDef = TypedDict(
    "AgentKnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseId": str,
        "knowledgeBaseState": KnowledgeBaseStateType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
AgentKnowledgeBaseTypeDef = TypedDict(
    "AgentKnowledgeBaseTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "createdAt": datetime,
        "description": str,
        "knowledgeBaseId": str,
        "knowledgeBaseState": KnowledgeBaseStateType,
        "updatedAt": datetime,
    },
)
GuardrailConfigurationTypeDef = TypedDict(
    "GuardrailConfigurationTypeDef",
    {
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
AssociateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "AssociateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "description": str,
        "knowledgeBaseId": str,
        "knowledgeBaseState": NotRequired[KnowledgeBaseStateType],
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
BedrockEmbeddingModelConfigurationTypeDef = TypedDict(
    "BedrockEmbeddingModelConfigurationTypeDef",
    {
        "dimensions": NotRequired[int],
    },
)
FixedSizeChunkingConfigurationTypeDef = TypedDict(
    "FixedSizeChunkingConfigurationTypeDef",
    {
        "maxTokens": int,
        "overlapPercentage": int,
    },
)
ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "kmsKeyArn": NotRequired[str],
    },
)
S3DataSourceConfigurationOutputTypeDef = TypedDict(
    "S3DataSourceConfigurationOutputTypeDef",
    {
        "bucketArn": str,
        "bucketOwnerAccountId": NotRequired[str],
        "inclusionPrefixes": NotRequired[List[str]],
    },
)
S3DataSourceConfigurationTypeDef = TypedDict(
    "S3DataSourceConfigurationTypeDef",
    {
        "bucketArn": str,
        "bucketOwnerAccountId": NotRequired[str],
        "inclusionPrefixes": NotRequired[Sequence[str]],
    },
)
DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "status": DataSourceStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
DeleteAgentActionGroupRequestRequestTypeDef = TypedDict(
    "DeleteAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "agentId": str,
        "agentVersion": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteAgentAliasRequestRequestTypeDef = TypedDict(
    "DeleteAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
    },
)
DeleteAgentRequestRequestTypeDef = TypedDict(
    "DeleteAgentRequestRequestTypeDef",
    {
        "agentId": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteAgentVersionRequestRequestTypeDef = TypedDict(
    "DeleteAgentVersionRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
    },
)
DeleteKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
DisassociateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DisassociateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
    },
)
ParameterDetailTypeDef = TypedDict(
    "ParameterDetailTypeDef",
    {
        "type": TypeType,
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)
GetAgentActionGroupRequestRequestTypeDef = TypedDict(
    "GetAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "agentId": str,
        "agentVersion": str,
    },
)
GetAgentAliasRequestRequestTypeDef = TypedDict(
    "GetAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
    },
)
GetAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
    },
)
GetAgentRequestRequestTypeDef = TypedDict(
    "GetAgentRequestRequestTypeDef",
    {
        "agentId": str,
    },
)
GetAgentVersionRequestRequestTypeDef = TypedDict(
    "GetAgentVersionRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
    },
)
GetDataSourceRequestRequestTypeDef = TypedDict(
    "GetDataSourceRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
    },
)
GetIngestionJobRequestRequestTypeDef = TypedDict(
    "GetIngestionJobRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
    },
)
GetKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
InferenceConfigurationOutputTypeDef = TypedDict(
    "InferenceConfigurationOutputTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[List[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[Sequence[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
IngestionJobFilterTypeDef = TypedDict(
    "IngestionJobFilterTypeDef",
    {
        "attribute": Literal["STATUS"],
        "operator": Literal["EQ"],
        "values": Sequence[str],
    },
)
IngestionJobSortByTypeDef = TypedDict(
    "IngestionJobSortByTypeDef",
    {
        "attribute": IngestionJobSortByAttributeType,
        "order": SortOrderType,
    },
)
IngestionJobStatisticsTypeDef = TypedDict(
    "IngestionJobStatisticsTypeDef",
    {
        "numberOfDocumentsDeleted": NotRequired[int],
        "numberOfDocumentsFailed": NotRequired[int],
        "numberOfDocumentsScanned": NotRequired[int],
        "numberOfMetadataDocumentsModified": NotRequired[int],
        "numberOfMetadataDocumentsScanned": NotRequired[int],
        "numberOfModifiedDocumentsIndexed": NotRequired[int],
        "numberOfNewDocumentsIndexed": NotRequired[int],
    },
)
KnowledgeBaseSummaryTypeDef = TypedDict(
    "KnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseId": str,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
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
ListAgentActionGroupsRequestRequestTypeDef = TypedDict(
    "ListAgentActionGroupsRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentAliasesRequestRequestTypeDef = TypedDict(
    "ListAgentAliasesRequestRequestTypeDef",
    {
        "agentId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListAgentKnowledgeBasesRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentVersionsRequestRequestTypeDef = TypedDict(
    "ListAgentVersionsRequestRequestTypeDef",
    {
        "agentId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentsRequestRequestTypeDef = TypedDict(
    "ListAgentsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListDataSourcesRequestRequestTypeDef = TypedDict(
    "ListDataSourcesRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListKnowledgeBasesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
MongoDbAtlasFieldMappingTypeDef = TypedDict(
    "MongoDbAtlasFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
OpenSearchServerlessFieldMappingTypeDef = TypedDict(
    "OpenSearchServerlessFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
PineconeFieldMappingTypeDef = TypedDict(
    "PineconeFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
    },
)
PrepareAgentRequestRequestTypeDef = TypedDict(
    "PrepareAgentRequestRequestTypeDef",
    {
        "agentId": str,
    },
)
RdsFieldMappingTypeDef = TypedDict(
    "RdsFieldMappingTypeDef",
    {
        "metadataField": str,
        "primaryKeyField": str,
        "textField": str,
        "vectorField": str,
    },
)
RedisEnterpriseCloudFieldMappingTypeDef = TypedDict(
    "RedisEnterpriseCloudFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
StartIngestionJobRequestRequestTypeDef = TypedDict(
    "StartIngestionJobRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "UpdateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
        "description": NotRequired[str],
        "knowledgeBaseState": NotRequired[KnowledgeBaseStateType],
    },
)
APISchemaTypeDef = TypedDict(
    "APISchemaTypeDef",
    {
        "payload": NotRequired[str],
        "s3": NotRequired[S3IdentifierTypeDef],
    },
)
AgentAliasHistoryEventTypeDef = TypedDict(
    "AgentAliasHistoryEventTypeDef",
    {
        "endDate": NotRequired[datetime],
        "routingConfiguration": NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]],
        "startDate": NotRequired[datetime],
    },
)
AgentAliasSummaryTypeDef = TypedDict(
    "AgentAliasSummaryTypeDef",
    {
        "agentAliasId": str,
        "agentAliasName": str,
        "agentAliasStatus": AgentAliasStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]],
    },
)
CreateAgentAliasRequestRequestTypeDef = TypedDict(
    "CreateAgentAliasRequestRequestTypeDef",
    {
        "agentAliasName": str,
        "agentId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[
            Sequence[AgentAliasRoutingConfigurationListItemTypeDef]
        ],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateAgentAliasRequestRequestTypeDef = TypedDict(
    "UpdateAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentAliasName": str,
        "agentId": str,
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[
            Sequence[AgentAliasRoutingConfigurationListItemTypeDef]
        ],
    },
)
AgentSummaryTypeDef = TypedDict(
    "AgentSummaryTypeDef",
    {
        "agentId": str,
        "agentName": str,
        "agentStatus": AgentStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "latestAgentVersion": NotRequired[str],
    },
)
AgentVersionSummaryTypeDef = TypedDict(
    "AgentVersionSummaryTypeDef",
    {
        "agentName": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
    },
)
AssociateAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "AssociateAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentAliasResponseTypeDef = TypedDict(
    "DeleteAgentAliasResponseTypeDef",
    {
        "agentAliasId": str,
        "agentAliasStatus": AgentAliasStatusType,
        "agentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentResponseTypeDef = TypedDict(
    "DeleteAgentResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentVersionResponseTypeDef = TypedDict(
    "DeleteAgentVersionResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "status": DataSourceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteKnowledgeBaseResponseTypeDef = TypedDict(
    "DeleteKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBaseId": str,
        "status": KnowledgeBaseStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "GetAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentActionGroupsResponseTypeDef = TypedDict(
    "ListAgentActionGroupsResponseTypeDef",
    {
        "actionGroupSummaries": List[ActionGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentKnowledgeBasesResponseTypeDef = TypedDict(
    "ListAgentKnowledgeBasesResponseTypeDef",
    {
        "agentKnowledgeBaseSummaries": List[AgentKnowledgeBaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PrepareAgentResponseTypeDef = TypedDict(
    "PrepareAgentResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "preparedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "UpdateAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EmbeddingModelConfigurationTypeDef = TypedDict(
    "EmbeddingModelConfigurationTypeDef",
    {
        "bedrockEmbeddingModelConfiguration": NotRequired[
            BedrockEmbeddingModelConfigurationTypeDef
        ],
    },
)
ChunkingConfigurationTypeDef = TypedDict(
    "ChunkingConfigurationTypeDef",
    {
        "chunkingStrategy": ChunkingStrategyType,
        "fixedSizeChunkingConfiguration": NotRequired[FixedSizeChunkingConfigurationTypeDef],
    },
)
DataSourceConfigurationOutputTypeDef = TypedDict(
    "DataSourceConfigurationOutputTypeDef",
    {
        "type": Literal["S3"],
        "s3Configuration": NotRequired[S3DataSourceConfigurationOutputTypeDef],
    },
)
DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "type": Literal["S3"],
        "s3Configuration": NotRequired[S3DataSourceConfigurationTypeDef],
    },
)
ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "dataSourceSummaries": List[DataSourceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FunctionOutputTypeDef = TypedDict(
    "FunctionOutputTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, ParameterDetailTypeDef]],
    },
)
FunctionTypeDef = TypedDict(
    "FunctionTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "parameters": NotRequired[Mapping[str, ParameterDetailTypeDef]],
    },
)
PromptConfigurationOutputTypeDef = TypedDict(
    "PromptConfigurationOutputTypeDef",
    {
        "basePromptTemplate": NotRequired[str],
        "inferenceConfiguration": NotRequired[InferenceConfigurationOutputTypeDef],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "promptState": NotRequired[PromptStateType],
        "promptType": NotRequired[PromptTypeType],
    },
)
PromptConfigurationTypeDef = TypedDict(
    "PromptConfigurationTypeDef",
    {
        "basePromptTemplate": NotRequired[str],
        "inferenceConfiguration": NotRequired[InferenceConfigurationTypeDef],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "promptState": NotRequired[PromptStateType],
        "promptType": NotRequired[PromptTypeType],
    },
)
ListIngestionJobsRequestRequestTypeDef = TypedDict(
    "ListIngestionJobsRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "filters": NotRequired[Sequence[IngestionJobFilterTypeDef]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[IngestionJobSortByTypeDef],
    },
)
IngestionJobSummaryTypeDef = TypedDict(
    "IngestionJobSummaryTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
        "startedAt": datetime,
        "status": IngestionJobStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "statistics": NotRequired[IngestionJobStatisticsTypeDef],
    },
)
IngestionJobTypeDef = TypedDict(
    "IngestionJobTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
        "startedAt": datetime,
        "status": IngestionJobStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "statistics": NotRequired[IngestionJobStatisticsTypeDef],
    },
)
ListKnowledgeBasesResponseTypeDef = TypedDict(
    "ListKnowledgeBasesResponseTypeDef",
    {
        "knowledgeBaseSummaries": List[KnowledgeBaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef = TypedDict(
    "ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentAliasesRequestListAgentAliasesPaginateTypeDef = TypedDict(
    "ListAgentAliasesRequestListAgentAliasesPaginateTypeDef",
    {
        "agentId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentVersionsRequestListAgentVersionsPaginateTypeDef = TypedDict(
    "ListAgentVersionsRequestListAgentVersionsPaginateTypeDef",
    {
        "agentId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentsRequestListAgentsPaginateTypeDef = TypedDict(
    "ListAgentsRequestListAgentsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListIngestionJobsRequestListIngestionJobsPaginateTypeDef = TypedDict(
    "ListIngestionJobsRequestListIngestionJobsPaginateTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "filters": NotRequired[Sequence[IngestionJobFilterTypeDef]],
        "sortBy": NotRequired[IngestionJobSortByTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
MongoDbAtlasConfigurationTypeDef = TypedDict(
    "MongoDbAtlasConfigurationTypeDef",
    {
        "collectionName": str,
        "credentialsSecretArn": str,
        "databaseName": str,
        "endpoint": str,
        "fieldMapping": MongoDbAtlasFieldMappingTypeDef,
        "vectorIndexName": str,
        "endpointServiceName": NotRequired[str],
    },
)
OpenSearchServerlessConfigurationTypeDef = TypedDict(
    "OpenSearchServerlessConfigurationTypeDef",
    {
        "collectionArn": str,
        "fieldMapping": OpenSearchServerlessFieldMappingTypeDef,
        "vectorIndexName": str,
    },
)
PineconeConfigurationTypeDef = TypedDict(
    "PineconeConfigurationTypeDef",
    {
        "connectionString": str,
        "credentialsSecretArn": str,
        "fieldMapping": PineconeFieldMappingTypeDef,
        "namespace": NotRequired[str],
    },
)
RdsConfigurationTypeDef = TypedDict(
    "RdsConfigurationTypeDef",
    {
        "credentialsSecretArn": str,
        "databaseName": str,
        "fieldMapping": RdsFieldMappingTypeDef,
        "resourceArn": str,
        "tableName": str,
    },
)
RedisEnterpriseCloudConfigurationTypeDef = TypedDict(
    "RedisEnterpriseCloudConfigurationTypeDef",
    {
        "credentialsSecretArn": str,
        "endpoint": str,
        "fieldMapping": RedisEnterpriseCloudFieldMappingTypeDef,
        "vectorIndexName": str,
    },
)
AgentAliasTypeDef = TypedDict(
    "AgentAliasTypeDef",
    {
        "agentAliasArn": str,
        "agentAliasId": str,
        "agentAliasName": str,
        "agentAliasStatus": AgentAliasStatusType,
        "agentId": str,
        "createdAt": datetime,
        "routingConfiguration": List[AgentAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "agentAliasHistoryEvents": NotRequired[List[AgentAliasHistoryEventTypeDef]],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
    },
)
ListAgentAliasesResponseTypeDef = TypedDict(
    "ListAgentAliasesResponseTypeDef",
    {
        "agentAliasSummaries": List[AgentAliasSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentsResponseTypeDef = TypedDict(
    "ListAgentsResponseTypeDef",
    {
        "agentSummaries": List[AgentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentVersionsResponseTypeDef = TypedDict(
    "ListAgentVersionsResponseTypeDef",
    {
        "agentVersionSummaries": List[AgentVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VectorKnowledgeBaseConfigurationTypeDef = TypedDict(
    "VectorKnowledgeBaseConfigurationTypeDef",
    {
        "embeddingModelArn": str,
        "embeddingModelConfiguration": NotRequired[EmbeddingModelConfigurationTypeDef],
    },
)
VectorIngestionConfigurationTypeDef = TypedDict(
    "VectorIngestionConfigurationTypeDef",
    {
        "chunkingConfiguration": NotRequired[ChunkingConfigurationTypeDef],
    },
)
FunctionSchemaOutputTypeDef = TypedDict(
    "FunctionSchemaOutputTypeDef",
    {
        "functions": NotRequired[List[FunctionOutputTypeDef]],
    },
)
FunctionSchemaTypeDef = TypedDict(
    "FunctionSchemaTypeDef",
    {
        "functions": NotRequired[Sequence[FunctionTypeDef]],
    },
)
PromptOverrideConfigurationOutputTypeDef = TypedDict(
    "PromptOverrideConfigurationOutputTypeDef",
    {
        "promptConfigurations": List[PromptConfigurationOutputTypeDef],
        "overrideLambda": NotRequired[str],
    },
)
PromptOverrideConfigurationTypeDef = TypedDict(
    "PromptOverrideConfigurationTypeDef",
    {
        "promptConfigurations": Sequence[PromptConfigurationTypeDef],
        "overrideLambda": NotRequired[str],
    },
)
ListIngestionJobsResponseTypeDef = TypedDict(
    "ListIngestionJobsResponseTypeDef",
    {
        "ingestionJobSummaries": List[IngestionJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIngestionJobResponseTypeDef = TypedDict(
    "GetIngestionJobResponseTypeDef",
    {
        "ingestionJob": IngestionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartIngestionJobResponseTypeDef = TypedDict(
    "StartIngestionJobResponseTypeDef",
    {
        "ingestionJob": IngestionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StorageConfigurationTypeDef = TypedDict(
    "StorageConfigurationTypeDef",
    {
        "type": KnowledgeBaseStorageTypeType,
        "mongoDbAtlasConfiguration": NotRequired[MongoDbAtlasConfigurationTypeDef],
        "opensearchServerlessConfiguration": NotRequired[OpenSearchServerlessConfigurationTypeDef],
        "pineconeConfiguration": NotRequired[PineconeConfigurationTypeDef],
        "rdsConfiguration": NotRequired[RdsConfigurationTypeDef],
        "redisEnterpriseCloudConfiguration": NotRequired[RedisEnterpriseCloudConfigurationTypeDef],
    },
)
CreateAgentAliasResponseTypeDef = TypedDict(
    "CreateAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentAliasResponseTypeDef = TypedDict(
    "GetAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentAliasResponseTypeDef = TypedDict(
    "UpdateAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KnowledgeBaseConfigurationTypeDef = TypedDict(
    "KnowledgeBaseConfigurationTypeDef",
    {
        "type": Literal["VECTOR"],
        "vectorKnowledgeBaseConfiguration": NotRequired[VectorKnowledgeBaseConfigurationTypeDef],
    },
)
CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "dataSourceConfiguration": DataSourceConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "clientToken": NotRequired[str],
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationTypeDef],
    },
)
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfiguration": DataSourceConfigurationOutputTypeDef,
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "status": DataSourceStatusType,
        "updatedAt": datetime,
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationTypeDef],
    },
)
UpdateDataSourceRequestRequestTypeDef = TypedDict(
    "UpdateDataSourceRequestRequestTypeDef",
    {
        "dataSourceConfiguration": DataSourceConfigurationTypeDef,
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationTypeDef],
    },
)
AgentActionGroupTypeDef = TypedDict(
    "AgentActionGroupTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "actionGroupState": ActionGroupStateType,
        "agentId": str,
        "agentVersion": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaOutputTypeDef],
        "parentActionSignature": NotRequired[Literal["AMAZON.UserInput"]],
    },
)
CreateAgentActionGroupRequestRequestTypeDef = TypedDict(
    "CreateAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupName": str,
        "agentId": str,
        "agentVersion": str,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "actionGroupState": NotRequired[ActionGroupStateType],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaTypeDef],
        "parentActionGroupSignature": NotRequired[Literal["AMAZON.UserInput"]],
    },
)
UpdateAgentActionGroupRequestRequestTypeDef = TypedDict(
    "UpdateAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "agentId": str,
        "agentVersion": str,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "actionGroupState": NotRequired[ActionGroupStateType],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaTypeDef],
        "parentActionGroupSignature": NotRequired[Literal["AMAZON.UserInput"]],
    },
)
AgentTypeDef = TypedDict(
    "AgentTypeDef",
    {
        "agentArn": str,
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "createdAt": datetime,
        "idleSessionTTLInSeconds": int,
        "updatedAt": datetime,
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "instruction": NotRequired[str],
        "preparedAt": NotRequired[datetime],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationOutputTypeDef],
        "recommendedActions": NotRequired[List[str]],
    },
)
AgentVersionTypeDef = TypedDict(
    "AgentVersionTypeDef",
    {
        "agentArn": str,
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "agentStatus": AgentStatusType,
        "createdAt": datetime,
        "idleSessionTTLInSeconds": int,
        "updatedAt": datetime,
        "version": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "instruction": NotRequired[str],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationOutputTypeDef],
        "recommendedActions": NotRequired[List[str]],
    },
)
CreateAgentRequestRequestTypeDef = TypedDict(
    "CreateAgentRequestRequestTypeDef",
    {
        "agentName": str,
        "agentResourceRoleArn": NotRequired[str],
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "idleSessionTTLInSeconds": NotRequired[int],
        "instruction": NotRequired[str],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateAgentRequestRequestTypeDef = TypedDict(
    "UpdateAgentRequestRequestTypeDef",
    {
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "foundationModel": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "idleSessionTTLInSeconds": NotRequired[int],
        "instruction": NotRequired[str],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationTypeDef],
    },
)
CreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "CreateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "name": str,
        "roleArn": str,
        "storageConfiguration": StorageConfigurationTypeDef,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
KnowledgeBaseTypeDef = TypedDict(
    "KnowledgeBaseTypeDef",
    {
        "createdAt": datetime,
        "knowledgeBaseArn": str,
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "roleArn": str,
        "status": KnowledgeBaseStatusType,
        "storageConfiguration": StorageConfigurationTypeDef,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
    },
)
UpdateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "UpdateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "roleArn": str,
        "storageConfiguration": StorageConfigurationTypeDef,
        "description": NotRequired[str],
    },
)
CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceResponseTypeDef = TypedDict(
    "GetDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateAgentActionGroupResponseTypeDef = TypedDict(
    "CreateAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentActionGroupResponseTypeDef = TypedDict(
    "GetAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentActionGroupResponseTypeDef = TypedDict(
    "UpdateAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateAgentResponseTypeDef = TypedDict(
    "CreateAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentResponseTypeDef = TypedDict(
    "GetAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentResponseTypeDef = TypedDict(
    "UpdateAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentVersionResponseTypeDef = TypedDict(
    "GetAgentVersionResponseTypeDef",
    {
        "agentVersion": AgentVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateKnowledgeBaseResponseTypeDef = TypedDict(
    "CreateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetKnowledgeBaseResponseTypeDef = TypedDict(
    "GetKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateKnowledgeBaseResponseTypeDef = TypedDict(
    "UpdateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
