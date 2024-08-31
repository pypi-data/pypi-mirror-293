"""
Type annotations for ivs-realtime service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ivs_realtime.client import IvsrealtimeClient

    session = get_session()
    async with session.create_client("ivs-realtime") as client:
        client: IvsrealtimeClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CreateEncoderConfigurationRequestRequestTypeDef,
    CreateEncoderConfigurationResponseTypeDef,
    CreateParticipantTokenRequestRequestTypeDef,
    CreateParticipantTokenResponseTypeDef,
    CreateStageRequestRequestTypeDef,
    CreateStageResponseTypeDef,
    CreateStorageConfigurationRequestRequestTypeDef,
    CreateStorageConfigurationResponseTypeDef,
    DeleteEncoderConfigurationRequestRequestTypeDef,
    DeleteStageRequestRequestTypeDef,
    DeleteStorageConfigurationRequestRequestTypeDef,
    DisconnectParticipantRequestRequestTypeDef,
    GetCompositionRequestRequestTypeDef,
    GetCompositionResponseTypeDef,
    GetEncoderConfigurationRequestRequestTypeDef,
    GetEncoderConfigurationResponseTypeDef,
    GetParticipantRequestRequestTypeDef,
    GetParticipantResponseTypeDef,
    GetStageRequestRequestTypeDef,
    GetStageResponseTypeDef,
    GetStageSessionRequestRequestTypeDef,
    GetStageSessionResponseTypeDef,
    GetStorageConfigurationRequestRequestTypeDef,
    GetStorageConfigurationResponseTypeDef,
    ListCompositionsRequestRequestTypeDef,
    ListCompositionsResponseTypeDef,
    ListEncoderConfigurationsRequestRequestTypeDef,
    ListEncoderConfigurationsResponseTypeDef,
    ListParticipantEventsRequestRequestTypeDef,
    ListParticipantEventsResponseTypeDef,
    ListParticipantsRequestRequestTypeDef,
    ListParticipantsResponseTypeDef,
    ListStageSessionsRequestRequestTypeDef,
    ListStageSessionsResponseTypeDef,
    ListStagesRequestRequestTypeDef,
    ListStagesResponseTypeDef,
    ListStorageConfigurationsRequestRequestTypeDef,
    ListStorageConfigurationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartCompositionRequestRequestTypeDef,
    StartCompositionResponseTypeDef,
    StopCompositionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateStageRequestRequestTypeDef,
    UpdateStageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IvsrealtimeClient",)

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
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IvsrealtimeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IvsrealtimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#close)
        """

    async def create_encoder_configuration(
        self, **kwargs: Unpack[CreateEncoderConfigurationRequestRequestTypeDef]
    ) -> CreateEncoderConfigurationResponseTypeDef:
        """
        Creates an EncoderConfiguration object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.create_encoder_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#create_encoder_configuration)
        """

    async def create_participant_token(
        self, **kwargs: Unpack[CreateParticipantTokenRequestRequestTypeDef]
    ) -> CreateParticipantTokenResponseTypeDef:
        """
        Creates an additional token for a specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.create_participant_token)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#create_participant_token)
        """

    async def create_stage(
        self, **kwargs: Unpack[CreateStageRequestRequestTypeDef]
    ) -> CreateStageResponseTypeDef:
        """
        Creates a new stage (and optionally participant tokens).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.create_stage)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#create_stage)
        """

    async def create_storage_configuration(
        self, **kwargs: Unpack[CreateStorageConfigurationRequestRequestTypeDef]
    ) -> CreateStorageConfigurationResponseTypeDef:
        """
        Creates a new storage configuration, used to enable recording to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.create_storage_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#create_storage_configuration)
        """

    async def delete_encoder_configuration(
        self, **kwargs: Unpack[DeleteEncoderConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an EncoderConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.delete_encoder_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#delete_encoder_configuration)
        """

    async def delete_stage(
        self, **kwargs: Unpack[DeleteStageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Shuts down and deletes the specified stage (disconnecting all participants).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.delete_stage)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#delete_stage)
        """

    async def delete_storage_configuration(
        self, **kwargs: Unpack[DeleteStorageConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the storage configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.delete_storage_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#delete_storage_configuration)
        """

    async def disconnect_participant(
        self, **kwargs: Unpack[DisconnectParticipantRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disconnects a specified participant and revokes the participant permanently
        from a specified
        stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.disconnect_participant)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#disconnect_participant)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#generate_presigned_url)
        """

    async def get_composition(
        self, **kwargs: Unpack[GetCompositionRequestRequestTypeDef]
    ) -> GetCompositionResponseTypeDef:
        """
        Get information about the specified Composition resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_composition)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_composition)
        """

    async def get_encoder_configuration(
        self, **kwargs: Unpack[GetEncoderConfigurationRequestRequestTypeDef]
    ) -> GetEncoderConfigurationResponseTypeDef:
        """
        Gets information about the specified EncoderConfiguration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_encoder_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_encoder_configuration)
        """

    async def get_participant(
        self, **kwargs: Unpack[GetParticipantRequestRequestTypeDef]
    ) -> GetParticipantResponseTypeDef:
        """
        Gets information about the specified participant token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_participant)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_participant)
        """

    async def get_stage(
        self, **kwargs: Unpack[GetStageRequestRequestTypeDef]
    ) -> GetStageResponseTypeDef:
        """
        Gets information for the specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_stage)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_stage)
        """

    async def get_stage_session(
        self, **kwargs: Unpack[GetStageSessionRequestRequestTypeDef]
    ) -> GetStageSessionResponseTypeDef:
        """
        Gets information for the specified stage session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_stage_session)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_stage_session)
        """

    async def get_storage_configuration(
        self, **kwargs: Unpack[GetStorageConfigurationRequestRequestTypeDef]
    ) -> GetStorageConfigurationResponseTypeDef:
        """
        Gets the storage configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.get_storage_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#get_storage_configuration)
        """

    async def list_compositions(
        self, **kwargs: Unpack[ListCompositionsRequestRequestTypeDef]
    ) -> ListCompositionsResponseTypeDef:
        """
        Gets summary information about all Compositions in your account, in the AWS
        region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_compositions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_compositions)
        """

    async def list_encoder_configurations(
        self, **kwargs: Unpack[ListEncoderConfigurationsRequestRequestTypeDef]
    ) -> ListEncoderConfigurationsResponseTypeDef:
        """
        Gets summary information about all EncoderConfigurations in your account, in
        the AWS region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_encoder_configurations)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_encoder_configurations)
        """

    async def list_participant_events(
        self, **kwargs: Unpack[ListParticipantEventsRequestRequestTypeDef]
    ) -> ListParticipantEventsResponseTypeDef:
        """
        Lists events for a specified participant that occurred during a specified stage
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_participant_events)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_participant_events)
        """

    async def list_participants(
        self, **kwargs: Unpack[ListParticipantsRequestRequestTypeDef]
    ) -> ListParticipantsResponseTypeDef:
        """
        Lists all participants in a specified stage session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_participants)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_participants)
        """

    async def list_stage_sessions(
        self, **kwargs: Unpack[ListStageSessionsRequestRequestTypeDef]
    ) -> ListStageSessionsResponseTypeDef:
        """
        Gets all sessions for a specified stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_stage_sessions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_stage_sessions)
        """

    async def list_stages(
        self, **kwargs: Unpack[ListStagesRequestRequestTypeDef]
    ) -> ListStagesResponseTypeDef:
        """
        Gets summary information about all stages in your account, in the AWS region
        where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_stages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_stages)
        """

    async def list_storage_configurations(
        self, **kwargs: Unpack[ListStorageConfigurationsRequestRequestTypeDef]
    ) -> ListStorageConfigurationsResponseTypeDef:
        """
        Gets summary information about all storage configurations in your account, in
        the AWS region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_storage_configurations)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_storage_configurations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about AWS tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.list_tags_for_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#list_tags_for_resource)
        """

    async def start_composition(
        self, **kwargs: Unpack[StartCompositionRequestRequestTypeDef]
    ) -> StartCompositionResponseTypeDef:
        """
        Starts a Composition from a stage based on the configuration provided in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.start_composition)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#start_composition)
        """

    async def stop_composition(
        self, **kwargs: Unpack[StopCompositionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops and deletes a Composition resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.stop_composition)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#stop_composition)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates tags for the AWS resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.tag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.untag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#untag_resource)
        """

    async def update_stage(
        self, **kwargs: Unpack[UpdateStageRequestRequestTypeDef]
    ) -> UpdateStageResponseTypeDef:
        """
        Updates a stage's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client.update_stage)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/#update_stage)
        """

    async def __aenter__(self) -> "IvsrealtimeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime.html#Ivsrealtime.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/client/)
        """
