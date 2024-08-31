"""
Main interface for controlcatalog service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_controlcatalog import (
        Client,
        ControlCatalogClient,
        ListCommonControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = get_session()
    async with session.create_client("controlcatalog") as client:
        client: ControlCatalogClient
        ...


    list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```
"""

from .client import ControlCatalogClient
from .paginator import ListCommonControlsPaginator, ListDomainsPaginator, ListObjectivesPaginator

Client = ControlCatalogClient

__all__ = (
    "Client",
    "ControlCatalogClient",
    "ListCommonControlsPaginator",
    "ListDomainsPaginator",
    "ListObjectivesPaginator",
)
