"""
Type annotations for mq service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mq.client import MQClient

    session = get_session()
    async with session.create_client("mq") as client:
        client: MQClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AuthenticationStrategyType,
    BrokerStorageTypeType,
    DataReplicationModeType,
    DeploymentModeType,
    EngineTypeType,
    PromoteModeType,
)
from .paginator import ListBrokersPaginator
from .type_defs import (
    ConfigurationIdTypeDef,
    CreateBrokerResponseTypeDef,
    CreateConfigurationResponseTypeDef,
    DeleteBrokerResponseTypeDef,
    DescribeBrokerEngineTypesResponseTypeDef,
    DescribeBrokerInstanceOptionsResponseTypeDef,
    DescribeBrokerResponseTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeUserResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionOptionsTypeDef,
    LdapServerMetadataInputTypeDef,
    ListBrokersResponseTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsResponseTypeDef,
    ListTagsResponseTypeDef,
    ListUsersResponseTypeDef,
    LogsTypeDef,
    PromoteResponseTypeDef,
    UpdateBrokerResponseTypeDef,
    UpdateConfigurationResponseTypeDef,
    UserTypeDef,
    WeeklyStartTimeTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("MQClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class MQClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MQClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#close)
        """

    async def create_broker(
        self,
        *,
        BrokerName: str,
        DeploymentMode: DeploymentModeType,
        EngineType: EngineTypeType,
        HostInstanceType: str,
        PubliclyAccessible: bool,
        Users: Sequence[UserTypeDef],
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Configuration: ConfigurationIdTypeDef = ...,
        CreatorRequestId: str = ...,
        EncryptionOptions: EncryptionOptionsTypeDef = ...,
        EngineVersion: str = ...,
        LdapServerMetadata: LdapServerMetadataInputTypeDef = ...,
        Logs: LogsTypeDef = ...,
        MaintenanceWindowStartTime: WeeklyStartTimeTypeDef = ...,
        SecurityGroups: Sequence[str] = ...,
        StorageType: BrokerStorageTypeType = ...,
        SubnetIds: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...,
        DataReplicationMode: DataReplicationModeType = ...,
        DataReplicationPrimaryBrokerArn: str = ...,
    ) -> CreateBrokerResponseTypeDef:
        """
        Creates a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_broker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#create_broker)
        """

    async def create_configuration(
        self,
        *,
        EngineType: EngineTypeType,
        Name: str,
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        EngineVersion: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new configuration for the specified configuration name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#create_configuration)
        """

    async def create_tags(
        self, *, ResourceArn: str, Tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#create_tags)
        """

    async def create_user(
        self,
        *,
        BrokerId: str,
        Password: str,
        Username: str,
        ConsoleAccess: bool = ...,
        Groups: Sequence[str] = ...,
        ReplicationUser: bool = ...,
    ) -> Dict[str, Any]:
        """
        Creates an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#create_user)
        """

    async def delete_broker(self, *, BrokerId: str) -> DeleteBrokerResponseTypeDef:
        """
        Deletes a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_broker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#delete_broker)
        """

    async def delete_tags(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#delete_tags)
        """

    async def delete_user(self, *, BrokerId: str, Username: str) -> Dict[str, Any]:
        """
        Deletes an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#delete_user)
        """

    async def describe_broker(self, *, BrokerId: str) -> DescribeBrokerResponseTypeDef:
        """
        Returns information about the specified broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_broker)
        """

    async def describe_broker_engine_types(
        self, *, EngineType: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeBrokerEngineTypesResponseTypeDef:
        """
        Describe available engine types and versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker_engine_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_broker_engine_types)
        """

    async def describe_broker_instance_options(
        self,
        *,
        EngineType: str = ...,
        HostInstanceType: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        StorageType: str = ...,
    ) -> DescribeBrokerInstanceOptionsResponseTypeDef:
        """
        Describe available broker instance options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_broker_instance_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_broker_instance_options)
        """

    async def describe_configuration(
        self, *, ConfigurationId: str
    ) -> DescribeConfigurationResponseTypeDef:
        """
        Returns information about the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_configuration)
        """

    async def describe_configuration_revision(
        self, *, ConfigurationId: str, ConfigurationRevision: str
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns the specified configuration revision for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_configuration_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_configuration_revision)
        """

    async def describe_user(self, *, BrokerId: str, Username: str) -> DescribeUserResponseTypeDef:
        """
        Returns information about an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#describe_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#generate_presigned_url)
        """

    async def list_brokers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListBrokersResponseTypeDef:
        """
        Returns a list of all brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_brokers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#list_brokers)
        """

    async def list_configuration_revisions(
        self, *, ConfigurationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all revisions for the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_configuration_revisions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#list_configuration_revisions)
        """

    async def list_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#list_configurations)
        """

    async def list_tags(self, *, ResourceArn: str) -> ListTagsResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#list_tags)
        """

    async def list_users(
        self, *, BrokerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Returns a list of all ActiveMQ users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#list_users)
        """

    async def promote(self, *, BrokerId: str, Mode: PromoteModeType) -> PromoteResponseTypeDef:
        """
        Promotes a data replication replica broker to the primary broker role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.promote)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#promote)
        """

    async def reboot_broker(self, *, BrokerId: str) -> Dict[str, Any]:
        """
        Reboots a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.reboot_broker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#reboot_broker)
        """

    async def update_broker(
        self,
        *,
        BrokerId: str,
        AuthenticationStrategy: AuthenticationStrategyType = ...,
        AutoMinorVersionUpgrade: bool = ...,
        Configuration: ConfigurationIdTypeDef = ...,
        EngineVersion: str = ...,
        HostInstanceType: str = ...,
        LdapServerMetadata: LdapServerMetadataInputTypeDef = ...,
        Logs: LogsTypeDef = ...,
        MaintenanceWindowStartTime: WeeklyStartTimeTypeDef = ...,
        SecurityGroups: Sequence[str] = ...,
        DataReplicationMode: DataReplicationModeType = ...,
    ) -> UpdateBrokerResponseTypeDef:
        """
        Adds a pending configuration change to a broker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_broker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#update_broker)
        """

    async def update_configuration(
        self, *, ConfigurationId: str, Data: str, Description: str = ...
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#update_configuration)
        """

    async def update_user(
        self,
        *,
        BrokerId: str,
        Username: str,
        ConsoleAccess: bool = ...,
        Groups: Sequence[str] = ...,
        Password: str = ...,
        ReplicationUser: bool = ...,
    ) -> Dict[str, Any]:
        """
        Updates the information for an ActiveMQ user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#update_user)
        """

    def get_paginator(self, operation_name: Literal["list_brokers"]) -> ListBrokersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/#get_paginator)
        """

    async def __aenter__(self) -> "MQClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq.html#MQ.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/client/)
        """
