"""
Main interface for appsync service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appsync import (
        AppSyncClient,
        Client,
        ListApiKeysPaginator,
        ListDataSourcesPaginator,
        ListFunctionsPaginator,
        ListGraphqlApisPaginator,
        ListResolversByFunctionPaginator,
        ListResolversPaginator,
        ListTypesPaginator,
    )

    session = get_session()
    async with session.create_client("appsync") as client:
        client: AppSyncClient
        ...


    list_api_keys_paginator: ListApiKeysPaginator = client.get_paginator("list_api_keys")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
    list_graphql_apis_paginator: ListGraphqlApisPaginator = client.get_paginator("list_graphql_apis")
    list_resolvers_paginator: ListResolversPaginator = client.get_paginator("list_resolvers")
    list_resolvers_by_function_paginator: ListResolversByFunctionPaginator = client.get_paginator("list_resolvers_by_function")
    list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```
"""

from .client import AppSyncClient
from .paginator import (
    ListApiKeysPaginator,
    ListDataSourcesPaginator,
    ListFunctionsPaginator,
    ListGraphqlApisPaginator,
    ListResolversByFunctionPaginator,
    ListResolversPaginator,
    ListTypesPaginator,
)

Client = AppSyncClient


__all__ = (
    "AppSyncClient",
    "Client",
    "ListApiKeysPaginator",
    "ListDataSourcesPaginator",
    "ListFunctionsPaginator",
    "ListGraphqlApisPaginator",
    "ListResolversByFunctionPaginator",
    "ListResolversPaginator",
    "ListTypesPaginator",
)
