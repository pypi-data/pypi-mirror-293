"""
Type annotations for bedrock service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock.client import BedrockClient
    from types_aiobotocore_bedrock.paginator import (
        ListCustomModelsPaginator,
        ListEvaluationJobsPaginator,
        ListGuardrailsPaginator,
        ListModelCustomizationJobsPaginator,
        ListProvisionedModelThroughputsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock") as client:
        client: BedrockClient

        list_custom_models_paginator: ListCustomModelsPaginator = client.get_paginator("list_custom_models")
        list_evaluation_jobs_paginator: ListEvaluationJobsPaginator = client.get_paginator("list_evaluation_jobs")
        list_guardrails_paginator: ListGuardrailsPaginator = client.get_paginator("list_guardrails")
        list_model_customization_jobs_paginator: ListModelCustomizationJobsPaginator = client.get_paginator("list_model_customization_jobs")
        list_provisioned_model_throughputs_paginator: ListProvisionedModelThroughputsPaginator = client.get_paginator("list_provisioned_model_throughputs")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCustomModelsRequestListCustomModelsPaginateTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListGuardrailsRequestListGuardrailsPaginateTypeDef,
    ListGuardrailsResponseTypeDef,
    ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCustomModelsPaginator",
    "ListEvaluationJobsPaginator",
    "ListGuardrailsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListProvisionedModelThroughputsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCustomModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListCustomModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomModelsRequestListCustomModelsPaginateTypeDef]
    ) -> AsyncIterator[ListCustomModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListCustomModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
        """

class ListEvaluationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListEvaluationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListEvaluationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListEvaluationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
        """

class ListGuardrailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListGuardrails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGuardrailsRequestListGuardrailsPaginateTypeDef]
    ) -> AsyncIterator[ListGuardrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListGuardrails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
        """

class ListModelCustomizationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListModelCustomizationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListModelCustomizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListModelCustomizationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
        """

class ListProvisionedModelThroughputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListProvisionedModelThroughputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProvisionedModelThroughputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListProvisionedModelThroughputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
        """
