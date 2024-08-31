"""
Type annotations for bedrock-agent service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agent.client import AgentsforBedrockClient
    from types_aiobotocore_bedrock_agent.paginator import (
        ListAgentActionGroupsPaginator,
        ListAgentAliasesPaginator,
        ListAgentKnowledgeBasesPaginator,
        ListAgentVersionsPaginator,
        ListAgentsPaginator,
        ListDataSourcesPaginator,
        ListIngestionJobsPaginator,
        ListKnowledgeBasesPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agent") as client:
        client: AgentsforBedrockClient

        list_agent_action_groups_paginator: ListAgentActionGroupsPaginator = client.get_paginator("list_agent_action_groups")
        list_agent_aliases_paginator: ListAgentAliasesPaginator = client.get_paginator("list_agent_aliases")
        list_agent_knowledge_bases_paginator: ListAgentKnowledgeBasesPaginator = client.get_paginator("list_agent_knowledge_bases")
        list_agent_versions_paginator: ListAgentVersionsPaginator = client.get_paginator("list_agent_versions")
        list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
        list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef,
    ListAgentActionGroupsResponseTypeDef,
    ListAgentAliasesRequestListAgentAliasesPaginateTypeDef,
    ListAgentAliasesResponseTypeDef,
    ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef,
    ListAgentKnowledgeBasesResponseTypeDef,
    ListAgentsRequestListAgentsPaginateTypeDef,
    ListAgentsResponseTypeDef,
    ListAgentVersionsRequestListAgentVersionsPaginateTypeDef,
    ListAgentVersionsResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListIngestionJobsRequestListIngestionJobsPaginateTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAgentActionGroupsPaginator",
    "ListAgentAliasesPaginator",
    "ListAgentKnowledgeBasesPaginator",
    "ListAgentVersionsPaginator",
    "ListAgentsPaginator",
    "ListDataSourcesPaginator",
    "ListIngestionJobsPaginator",
    "ListKnowledgeBasesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAgentActionGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentActionGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentactiongroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListAgentActionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentActionGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentactiongroupspaginator)
        """


class ListAgentAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentAliasesRequestListAgentAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAgentAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentaliasespaginator)
        """


class ListAgentKnowledgeBasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef]
    ) -> AsyncIterator[ListAgentKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentKnowledgeBases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentknowledgebasespaginator)
        """


class ListAgentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentVersionsRequestListAgentVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListAgentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgentVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentversionspaginator)
        """


class ListAgentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAgentsRequestListAgentsPaginateTypeDef]
    ) -> AsyncIterator[ListAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListAgents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listagentspaginator)
        """


class ListDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listdatasourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listdatasourcespaginator)
        """


class ListIngestionJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListIngestionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listingestionjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListIngestionJobsRequestListIngestionJobsPaginateTypeDef]
    ) -> AsyncIterator[ListIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListIngestionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listingestionjobspaginator)
        """


class ListKnowledgeBasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListKnowledgeBases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef]
    ) -> AsyncIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Paginator.ListKnowledgeBases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/paginators/#listknowledgebasespaginator)
        """
