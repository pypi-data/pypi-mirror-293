"""
Type annotations for detective service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_detective.client import DetectiveClient

    session = get_session()
    async with session.create_client("detective") as client:
        client: DetectiveClient
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import DatasourcePackageType, IndicatorTypeType, StateType
from .type_defs import (
    AccountTypeDef,
    BatchGetGraphMemberDatasourcesResponseTypeDef,
    BatchGetMembershipDatasourcesResponseTypeDef,
    CreateGraphResponseTypeDef,
    CreateMembersResponseTypeDef,
    DeleteMembersResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterCriteriaTypeDef,
    GetInvestigationResponseTypeDef,
    GetMembersResponseTypeDef,
    ListDatasourcePackagesResponseTypeDef,
    ListGraphsResponseTypeDef,
    ListIndicatorsResponseTypeDef,
    ListInvestigationsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    SortCriteriaTypeDef,
    StartInvestigationResponseTypeDef,
    TimestampTypeDef,
)

__all__ = ("DetectiveClient",)


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
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DetectiveClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DetectiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#exceptions)
        """

    async def accept_invitation(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Accepts an invitation for the member account to contribute data to a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.accept_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#accept_invitation)
        """

    async def batch_get_graph_member_datasources(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> BatchGetGraphMemberDatasourcesResponseTypeDef:
        """
        Gets data source package information for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.batch_get_graph_member_datasources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#batch_get_graph_member_datasources)
        """

    async def batch_get_membership_datasources(
        self, *, GraphArns: Sequence[str]
    ) -> BatchGetMembershipDatasourcesResponseTypeDef:
        """
        Gets information on the data source package history for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.batch_get_membership_datasources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#batch_get_membership_datasources)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#close)
        """

    async def create_graph(self, *, Tags: Mapping[str, str] = ...) -> CreateGraphResponseTypeDef:
        """
        Creates a new behavior graph for the calling account, and sets that account as
        the administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_graph)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#create_graph)
        """

    async def create_members(
        self,
        *,
        GraphArn: str,
        Accounts: Sequence[AccountTypeDef],
        Message: str = ...,
        DisableEmailNotification: bool = ...,
    ) -> CreateMembersResponseTypeDef:
        """
        `CreateMembers` is used to send invitations to accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#create_members)
        """

    async def delete_graph(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified behavior graph and queues it to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_graph)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#delete_graph)
        """

    async def delete_members(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> DeleteMembersResponseTypeDef:
        """
        Removes the specified member accounts from the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#delete_members)
        """

    async def describe_organization_configuration(
        self, *, GraphArn: str
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the configuration for the organization behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.describe_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#describe_organization_configuration)
        """

    async def disable_organization_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Removes the Detective administrator account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.disable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#disable_organization_admin_account)
        """

    async def disassociate_membership(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Removes the member account from the specified behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.disassociate_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#disassociate_membership)
        """

    async def enable_organization_admin_account(
        self, *, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the Detective administrator account for the organization in the
        current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.enable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#enable_organization_admin_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#generate_presigned_url)
        """

    async def get_investigation(
        self, *, GraphArn: str, InvestigationId: str
    ) -> GetInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.get_investigation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#get_investigation)
        """

    async def get_members(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> GetMembersResponseTypeDef:
        """
        Returns the membership details for specified member accounts for a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.get_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#get_members)
        """

    async def list_datasource_packages(
        self, *, GraphArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDatasourcePackagesResponseTypeDef:
        """
        Lists data source packages in the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_datasource_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_datasource_packages)
        """

    async def list_graphs(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGraphsResponseTypeDef:
        """
        Returns the list of behavior graphs that the calling account is an
        administrator account
        of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_graphs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_graphs)
        """

    async def list_indicators(
        self,
        *,
        GraphArn: str,
        InvestigationId: str,
        IndicatorType: IndicatorTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListIndicatorsResponseTypeDef:
        """
        Gets the indicators from an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_indicators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_indicators)
        """

    async def list_investigations(
        self,
        *,
        GraphArn: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        FilterCriteria: FilterCriteriaTypeDef = ...,
        SortCriteria: SortCriteriaTypeDef = ...,
    ) -> ListInvestigationsResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_investigations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_investigations)
        """

    async def list_invitations(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves the list of open and accepted behavior graph invitations for the
        member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_invitations)
        """

    async def list_members(
        self, *, GraphArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves the list of member accounts for a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_members)
        """

    async def list_organization_admin_accounts(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Returns information about the Detective administrator account for an
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_organization_admin_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_organization_admin_accounts)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tag values that are assigned to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_tags_for_resource)
        """

    async def reject_invitation(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Rejects an invitation to contribute the account data to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.reject_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#reject_invitation)
        """

    async def start_investigation(
        self,
        *,
        GraphArn: str,
        EntityArn: str,
        ScopeStartTime: TimestampTypeDef,
        ScopeEndTime: TimestampTypeDef,
    ) -> StartInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.start_investigation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#start_investigation)
        """

    async def start_monitoring_member(
        self, *, GraphArn: str, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a request to enable data ingest for a member account that has a status of
        `ACCEPTED_BUT_DISABLED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.start_monitoring_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#start_monitoring_member)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies tag values to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#untag_resource)
        """

    async def update_datasource_packages(
        self, *, GraphArn: str, DatasourcePackages: Sequence[DatasourcePackageType]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a data source packages for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_datasource_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_datasource_packages)
        """

    async def update_investigation_state(
        self, *, GraphArn: str, InvestigationId: str, State: StateType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_investigation_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_investigation_state)
        """

    async def update_organization_configuration(
        self, *, GraphArn: str, AutoEnable: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration for the Organizations integration in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_organization_configuration)
        """

    async def __aenter__(self) -> "DetectiveClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
        """
