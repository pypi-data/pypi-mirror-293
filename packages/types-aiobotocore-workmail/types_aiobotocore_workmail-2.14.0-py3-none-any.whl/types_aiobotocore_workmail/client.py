"""
Type annotations for workmail service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workmail.client import WorkMailClient

    session = get_session()
    async with session.create_client("workmail") as client:
        client: WorkMailClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AccessControlRuleEffectType,
    ImpersonationRoleTypeType,
    MobileDeviceAccessRuleEffectType,
    PermissionTypeType,
    ResourceTypeType,
    UserRoleType,
)
from .paginator import (
    ListAliasesPaginator,
    ListAvailabilityConfigurationsPaginator,
    ListGroupMembersPaginator,
    ListGroupsPaginator,
    ListMailboxPermissionsPaginator,
    ListOrganizationsPaginator,
    ListResourceDelegatesPaginator,
    ListResourcesPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssumeImpersonationRoleResponseTypeDef,
    BookingOptionsTypeDef,
    CreateGroupResponseTypeDef,
    CreateImpersonationRoleResponseTypeDef,
    CreateMobileDeviceAccessRuleResponseTypeDef,
    CreateOrganizationResponseTypeDef,
    CreateResourceResponseTypeDef,
    CreateUserResponseTypeDef,
    DeleteOrganizationResponseTypeDef,
    DescribeEmailMonitoringConfigurationResponseTypeDef,
    DescribeEntityResponseTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeInboundDmarcSettingsResponseTypeDef,
    DescribeMailboxExportJobResponseTypeDef,
    DescribeOrganizationResponseTypeDef,
    DescribeResourceResponseTypeDef,
    DescribeUserResponseTypeDef,
    DomainTypeDef,
    EwsAvailabilityProviderTypeDef,
    FolderConfigurationTypeDef,
    GetAccessControlEffectResponseTypeDef,
    GetDefaultRetentionPolicyResponseTypeDef,
    GetImpersonationRoleEffectResponseTypeDef,
    GetImpersonationRoleResponseTypeDef,
    GetMailboxDetailsResponseTypeDef,
    GetMailDomainResponseTypeDef,
    GetMobileDeviceAccessEffectResponseTypeDef,
    GetMobileDeviceAccessOverrideResponseTypeDef,
    ImpersonationRuleUnionTypeDef,
    LambdaAvailabilityProviderTypeDef,
    ListAccessControlRulesResponseTypeDef,
    ListAliasesResponseTypeDef,
    ListAvailabilityConfigurationsResponseTypeDef,
    ListGroupMembersResponseTypeDef,
    ListGroupsFiltersTypeDef,
    ListGroupsForEntityFiltersTypeDef,
    ListGroupsForEntityResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListImpersonationRolesResponseTypeDef,
    ListMailboxExportJobsResponseTypeDef,
    ListMailboxPermissionsResponseTypeDef,
    ListMailDomainsResponseTypeDef,
    ListMobileDeviceAccessOverridesResponseTypeDef,
    ListMobileDeviceAccessRulesResponseTypeDef,
    ListOrganizationsResponseTypeDef,
    ListResourceDelegatesResponseTypeDef,
    ListResourcesFiltersTypeDef,
    ListResourcesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersFiltersTypeDef,
    ListUsersResponseTypeDef,
    StartMailboxExportJobResponseTypeDef,
    TagTypeDef,
    TestAvailabilityConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("WorkMailClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DirectoryInUseException: Type[BotocoreClientError]
    DirectoryServiceAuthenticationFailedException: Type[BotocoreClientError]
    DirectoryUnavailableException: Type[BotocoreClientError]
    EmailAddressInUseException: Type[BotocoreClientError]
    EntityAlreadyRegisteredException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    EntityStateException: Type[BotocoreClientError]
    InvalidConfigurationException: Type[BotocoreClientError]
    InvalidCustomSesConfigurationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailDomainInUseException: Type[BotocoreClientError]
    MailDomainNotFoundException: Type[BotocoreClientError]
    MailDomainStateException: Type[BotocoreClientError]
    NameAvailabilityException: Type[BotocoreClientError]
    OrganizationNotFoundException: Type[BotocoreClientError]
    OrganizationStateException: Type[BotocoreClientError]
    ReservedNameException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class WorkMailClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkMailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#exceptions)
        """

    async def associate_delegate_to_resource(
        self, *, OrganizationId: str, ResourceId: str, EntityId: str
    ) -> Dict[str, Any]:
        """
        Adds a member (user or group) to the resource's set of delegates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.associate_delegate_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#associate_delegate_to_resource)
        """

    async def associate_member_to_group(
        self, *, OrganizationId: str, GroupId: str, MemberId: str
    ) -> Dict[str, Any]:
        """
        Adds a member (user or group) to the group's set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.associate_member_to_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#associate_member_to_group)
        """

    async def assume_impersonation_role(
        self, *, OrganizationId: str, ImpersonationRoleId: str
    ) -> AssumeImpersonationRoleResponseTypeDef:
        """
        Assumes an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.assume_impersonation_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#assume_impersonation_role)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#can_paginate)
        """

    async def cancel_mailbox_export_job(
        self, *, ClientToken: str, JobId: str, OrganizationId: str
    ) -> Dict[str, Any]:
        """
        Cancels a mailbox export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.cancel_mailbox_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#cancel_mailbox_export_job)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#close)
        """

    async def create_alias(
        self, *, OrganizationId: str, EntityId: str, Alias: str
    ) -> Dict[str, Any]:
        """
        Adds an alias to the set of a given member (user or group) of WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_alias)
        """

    async def create_availability_configuration(
        self,
        *,
        OrganizationId: str,
        DomainName: str,
        ClientToken: str = ...,
        EwsProvider: EwsAvailabilityProviderTypeDef = ...,
        LambdaProvider: LambdaAvailabilityProviderTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Creates an `AvailabilityConfiguration` for the given WorkMail organization and
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_availability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_availability_configuration)
        """

    async def create_group(
        self, *, OrganizationId: str, Name: str, HiddenFromGlobalAddressList: bool = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group that can be used in WorkMail by calling the  RegisterToWorkMail
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_group)
        """

    async def create_impersonation_role(
        self,
        *,
        OrganizationId: str,
        Name: str,
        Type: ImpersonationRoleTypeType,
        Rules: Sequence[ImpersonationRuleUnionTypeDef],
        ClientToken: str = ...,
        Description: str = ...,
    ) -> CreateImpersonationRoleResponseTypeDef:
        """
        Creates an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_impersonation_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_impersonation_role)
        """

    async def create_mobile_device_access_rule(
        self,
        *,
        OrganizationId: str,
        Name: str,
        Effect: MobileDeviceAccessRuleEffectType,
        ClientToken: str = ...,
        Description: str = ...,
        DeviceTypes: Sequence[str] = ...,
        NotDeviceTypes: Sequence[str] = ...,
        DeviceModels: Sequence[str] = ...,
        NotDeviceModels: Sequence[str] = ...,
        DeviceOperatingSystems: Sequence[str] = ...,
        NotDeviceOperatingSystems: Sequence[str] = ...,
        DeviceUserAgents: Sequence[str] = ...,
        NotDeviceUserAgents: Sequence[str] = ...,
    ) -> CreateMobileDeviceAccessRuleResponseTypeDef:
        """
        Creates a new mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_mobile_device_access_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_mobile_device_access_rule)
        """

    async def create_organization(
        self,
        *,
        Alias: str,
        DirectoryId: str = ...,
        ClientToken: str = ...,
        Domains: Sequence[DomainTypeDef] = ...,
        KmsKeyArn: str = ...,
        EnableInteroperability: bool = ...,
    ) -> CreateOrganizationResponseTypeDef:
        """
        Creates a new WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_organization)
        """

    async def create_resource(
        self,
        *,
        OrganizationId: str,
        Name: str,
        Type: ResourceTypeType,
        Description: str = ...,
        HiddenFromGlobalAddressList: bool = ...,
    ) -> CreateResourceResponseTypeDef:
        """
        Creates a new WorkMail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_resource)
        """

    async def create_user(
        self,
        *,
        OrganizationId: str,
        Name: str,
        DisplayName: str,
        Password: str = ...,
        Role: UserRoleType = ...,
        FirstName: str = ...,
        LastName: str = ...,
        HiddenFromGlobalAddressList: bool = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user who can be used in WorkMail by calling the  RegisterToWorkMail
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_user)
        """

    async def delete_access_control_rule(self, *, OrganizationId: str, Name: str) -> Dict[str, Any]:
        """
        Deletes an access control rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_access_control_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_access_control_rule)
        """

    async def delete_alias(
        self, *, OrganizationId: str, EntityId: str, Alias: str
    ) -> Dict[str, Any]:
        """
        Remove one or more specified aliases from a set of aliases for a given user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_alias)
        """

    async def delete_availability_configuration(
        self, *, OrganizationId: str, DomainName: str
    ) -> Dict[str, Any]:
        """
        Deletes the `AvailabilityConfiguration` for the given WorkMail organization and
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_availability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_availability_configuration)
        """

    async def delete_email_monitoring_configuration(self, *, OrganizationId: str) -> Dict[str, Any]:
        """
        Deletes the email monitoring configuration for a specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_email_monitoring_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_email_monitoring_configuration)
        """

    async def delete_group(self, *, OrganizationId: str, GroupId: str) -> Dict[str, Any]:
        """
        Deletes a group from WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_group)
        """

    async def delete_impersonation_role(
        self, *, OrganizationId: str, ImpersonationRoleId: str
    ) -> Dict[str, Any]:
        """
        Deletes an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_impersonation_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_impersonation_role)
        """

    async def delete_mailbox_permissions(
        self, *, OrganizationId: str, EntityId: str, GranteeId: str
    ) -> Dict[str, Any]:
        """
        Deletes permissions granted to a member (user or group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_mailbox_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mailbox_permissions)
        """

    async def delete_mobile_device_access_override(
        self, *, OrganizationId: str, UserId: str, DeviceId: str
    ) -> Dict[str, Any]:
        """
        Deletes the mobile device access override for the given WorkMail organization,
        user, and
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_mobile_device_access_override)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mobile_device_access_override)
        """

    async def delete_mobile_device_access_rule(
        self, *, OrganizationId: str, MobileDeviceAccessRuleId: str
    ) -> Dict[str, Any]:
        """
        Deletes a mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_mobile_device_access_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mobile_device_access_rule)
        """

    async def delete_organization(
        self,
        *,
        OrganizationId: str,
        DeleteDirectory: bool,
        ClientToken: str = ...,
        ForceDelete: bool = ...,
    ) -> DeleteOrganizationResponseTypeDef:
        """
        Deletes an WorkMail organization and all underlying AWS resources managed by
        WorkMail as part of the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_organization)
        """

    async def delete_resource(self, *, OrganizationId: str, ResourceId: str) -> Dict[str, Any]:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_resource)
        """

    async def delete_retention_policy(self, *, OrganizationId: str, Id: str) -> Dict[str, Any]:
        """
        Deletes the specified retention policy from the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_retention_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_retention_policy)
        """

    async def delete_user(self, *, OrganizationId: str, UserId: str) -> Dict[str, Any]:
        """
        Deletes a user from WorkMail and all subsequent systems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_user)
        """

    async def deregister_from_work_mail(
        self, *, OrganizationId: str, EntityId: str
    ) -> Dict[str, Any]:
        """
        Mark a user, group, or resource as no longer used in WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.deregister_from_work_mail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#deregister_from_work_mail)
        """

    async def deregister_mail_domain(
        self, *, OrganizationId: str, DomainName: str
    ) -> Dict[str, Any]:
        """
        Removes a domain from WorkMail, stops email routing to WorkMail, and removes
        the authorization allowing WorkMail
        use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.deregister_mail_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#deregister_mail_domain)
        """

    async def describe_email_monitoring_configuration(
        self, *, OrganizationId: str
    ) -> DescribeEmailMonitoringConfigurationResponseTypeDef:
        """
        Describes the current email monitoring configuration for a specified
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_email_monitoring_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_email_monitoring_configuration)
        """

    async def describe_entity(
        self, *, OrganizationId: str, Email: str
    ) -> DescribeEntityResponseTypeDef:
        """
        Returns basic details about an entity in WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_entity)
        """

    async def describe_group(
        self, *, OrganizationId: str, GroupId: str
    ) -> DescribeGroupResponseTypeDef:
        """
        Returns the data available for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_group)
        """

    async def describe_inbound_dmarc_settings(
        self, *, OrganizationId: str
    ) -> DescribeInboundDmarcSettingsResponseTypeDef:
        """
        Lists the settings in a DMARC policy for a specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_inbound_dmarc_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_inbound_dmarc_settings)
        """

    async def describe_mailbox_export_job(
        self, *, JobId: str, OrganizationId: str
    ) -> DescribeMailboxExportJobResponseTypeDef:
        """
        Describes the current status of a mailbox export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_mailbox_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_mailbox_export_job)
        """

    async def describe_organization(
        self, *, OrganizationId: str
    ) -> DescribeOrganizationResponseTypeDef:
        """
        Provides more information regarding a given organization based on its
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_organization)
        """

    async def describe_resource(
        self, *, OrganizationId: str, ResourceId: str
    ) -> DescribeResourceResponseTypeDef:
        """
        Returns the data available for the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_resource)
        """

    async def describe_user(
        self, *, OrganizationId: str, UserId: str
    ) -> DescribeUserResponseTypeDef:
        """
        Provides information regarding the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_user)
        """

    async def disassociate_delegate_from_resource(
        self, *, OrganizationId: str, ResourceId: str, EntityId: str
    ) -> Dict[str, Any]:
        """
        Removes a member from the resource's set of delegates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.disassociate_delegate_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#disassociate_delegate_from_resource)
        """

    async def disassociate_member_from_group(
        self, *, OrganizationId: str, GroupId: str, MemberId: str
    ) -> Dict[str, Any]:
        """
        Removes a member from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.disassociate_member_from_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#disassociate_member_from_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#generate_presigned_url)
        """

    async def get_access_control_effect(
        self,
        *,
        OrganizationId: str,
        IpAddress: str,
        Action: str,
        UserId: str = ...,
        ImpersonationRoleId: str = ...,
    ) -> GetAccessControlEffectResponseTypeDef:
        """
        Gets the effects of an organization's access control rules as they apply to a
        specified IPv4 address, access protocol action, and user ID or impersonation
        role
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_access_control_effect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_access_control_effect)
        """

    async def get_default_retention_policy(
        self, *, OrganizationId: str
    ) -> GetDefaultRetentionPolicyResponseTypeDef:
        """
        Gets the default retention policy details for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_default_retention_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_default_retention_policy)
        """

    async def get_impersonation_role(
        self, *, OrganizationId: str, ImpersonationRoleId: str
    ) -> GetImpersonationRoleResponseTypeDef:
        """
        Gets the impersonation role details for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_impersonation_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_impersonation_role)
        """

    async def get_impersonation_role_effect(
        self, *, OrganizationId: str, ImpersonationRoleId: str, TargetUser: str
    ) -> GetImpersonationRoleEffectResponseTypeDef:
        """
        Tests whether the given impersonation role can impersonate a target user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_impersonation_role_effect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_impersonation_role_effect)
        """

    async def get_mail_domain(
        self, *, OrganizationId: str, DomainName: str
    ) -> GetMailDomainResponseTypeDef:
        """
        Gets details for a mail domain, including domain records required to configure
        your domain with recommended
        security.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_mail_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mail_domain)
        """

    async def get_mailbox_details(
        self, *, OrganizationId: str, UserId: str
    ) -> GetMailboxDetailsResponseTypeDef:
        """
        Requests a user's mailbox details for a specified organization and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_mailbox_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mailbox_details)
        """

    async def get_mobile_device_access_effect(
        self,
        *,
        OrganizationId: str,
        DeviceType: str = ...,
        DeviceModel: str = ...,
        DeviceOperatingSystem: str = ...,
        DeviceUserAgent: str = ...,
    ) -> GetMobileDeviceAccessEffectResponseTypeDef:
        """
        Simulates the effect of the mobile device access rules for the given attributes
        of a sample access
        event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_mobile_device_access_effect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mobile_device_access_effect)
        """

    async def get_mobile_device_access_override(
        self, *, OrganizationId: str, UserId: str, DeviceId: str
    ) -> GetMobileDeviceAccessOverrideResponseTypeDef:
        """
        Gets the mobile device access override for the given WorkMail organization,
        user, and
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_mobile_device_access_override)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mobile_device_access_override)
        """

    async def list_access_control_rules(
        self, *, OrganizationId: str
    ) -> ListAccessControlRulesResponseTypeDef:
        """
        Lists the access control rules for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_access_control_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_access_control_rules)
        """

    async def list_aliases(
        self, *, OrganizationId: str, EntityId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAliasesResponseTypeDef:
        """
        Creates a paginated call to list the aliases associated with a given entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_aliases)
        """

    async def list_availability_configurations(
        self, *, OrganizationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAvailabilityConfigurationsResponseTypeDef:
        """
        List all the `AvailabilityConfiguration`'s for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_availability_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_availability_configurations)
        """

    async def list_group_members(
        self, *, OrganizationId: str, GroupId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGroupMembersResponseTypeDef:
        """
        Returns an overview of the members of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_group_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_group_members)
        """

    async def list_groups(
        self,
        *,
        OrganizationId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: ListGroupsFiltersTypeDef = ...,
    ) -> ListGroupsResponseTypeDef:
        """
        Returns summaries of the organization's groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_groups)
        """

    async def list_groups_for_entity(
        self,
        *,
        OrganizationId: str,
        EntityId: str,
        Filters: ListGroupsForEntityFiltersTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListGroupsForEntityResponseTypeDef:
        """
        Returns all the groups to which an entity belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_groups_for_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_groups_for_entity)
        """

    async def list_impersonation_roles(
        self, *, OrganizationId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListImpersonationRolesResponseTypeDef:
        """
        Lists all the impersonation roles for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_impersonation_roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_impersonation_roles)
        """

    async def list_mail_domains(
        self, *, OrganizationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListMailDomainsResponseTypeDef:
        """
        Lists the mail domains in a given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_mail_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mail_domains)
        """

    async def list_mailbox_export_jobs(
        self, *, OrganizationId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMailboxExportJobsResponseTypeDef:
        """
        Lists the mailbox export jobs started for the specified organization within the
        last seven
        days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_mailbox_export_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mailbox_export_jobs)
        """

    async def list_mailbox_permissions(
        self, *, OrganizationId: str, EntityId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMailboxPermissionsResponseTypeDef:
        """
        Lists the mailbox permissions associated with a user, group, or resource
        mailbox.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_mailbox_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mailbox_permissions)
        """

    async def list_mobile_device_access_overrides(
        self,
        *,
        OrganizationId: str,
        UserId: str = ...,
        DeviceId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListMobileDeviceAccessOverridesResponseTypeDef:
        """
        Lists all the mobile device access overrides for any given combination of
        WorkMail organization, user, or
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_mobile_device_access_overrides)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mobile_device_access_overrides)
        """

    async def list_mobile_device_access_rules(
        self, *, OrganizationId: str
    ) -> ListMobileDeviceAccessRulesResponseTypeDef:
        """
        Lists the mobile device access rules for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_mobile_device_access_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mobile_device_access_rules)
        """

    async def list_organizations(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrganizationsResponseTypeDef:
        """
        Returns summaries of the customer's organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_organizations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_organizations)
        """

    async def list_resource_delegates(
        self, *, OrganizationId: str, ResourceId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListResourceDelegatesResponseTypeDef:
        """
        Lists the delegates associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_resource_delegates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_resource_delegates)
        """

    async def list_resources(
        self,
        *,
        OrganizationId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: ListResourcesFiltersTypeDef = ...,
    ) -> ListResourcesResponseTypeDef:
        """
        Returns summaries of the organization's resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_resources)
        """

    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an WorkMail organization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_tags_for_resource)
        """

    async def list_users(
        self,
        *,
        OrganizationId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: ListUsersFiltersTypeDef = ...,
    ) -> ListUsersResponseTypeDef:
        """
        Returns summaries of the organization's users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_users)
        """

    async def put_access_control_rule(
        self,
        *,
        Name: str,
        Effect: AccessControlRuleEffectType,
        Description: str,
        OrganizationId: str,
        IpRanges: Sequence[str] = ...,
        NotIpRanges: Sequence[str] = ...,
        Actions: Sequence[str] = ...,
        NotActions: Sequence[str] = ...,
        UserIds: Sequence[str] = ...,
        NotUserIds: Sequence[str] = ...,
        ImpersonationRoleIds: Sequence[str] = ...,
        NotImpersonationRoleIds: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Adds a new access control rule for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_access_control_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_access_control_rule)
        """

    async def put_email_monitoring_configuration(
        self, *, OrganizationId: str, RoleArn: str, LogGroupArn: str
    ) -> Dict[str, Any]:
        """
        Creates or updates the email monitoring configuration for a specified
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_email_monitoring_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_email_monitoring_configuration)
        """

    async def put_inbound_dmarc_settings(
        self, *, OrganizationId: str, Enforced: bool
    ) -> Dict[str, Any]:
        """
        Enables or disables a DMARC policy for a given organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_inbound_dmarc_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_inbound_dmarc_settings)
        """

    async def put_mailbox_permissions(
        self,
        *,
        OrganizationId: str,
        EntityId: str,
        GranteeId: str,
        PermissionValues: Sequence[PermissionTypeType],
    ) -> Dict[str, Any]:
        """
        Sets permissions for a user, group, or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_mailbox_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_mailbox_permissions)
        """

    async def put_mobile_device_access_override(
        self,
        *,
        OrganizationId: str,
        UserId: str,
        DeviceId: str,
        Effect: MobileDeviceAccessRuleEffectType,
        Description: str = ...,
    ) -> Dict[str, Any]:
        """
        Creates or updates a mobile device access override for the given WorkMail
        organization, user, and
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_mobile_device_access_override)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_mobile_device_access_override)
        """

    async def put_retention_policy(
        self,
        *,
        OrganizationId: str,
        Name: str,
        FolderConfigurations: Sequence[FolderConfigurationTypeDef],
        Id: str = ...,
        Description: str = ...,
    ) -> Dict[str, Any]:
        """
        Puts a retention policy to the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.put_retention_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_retention_policy)
        """

    async def register_mail_domain(
        self, *, OrganizationId: str, DomainName: str, ClientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Registers a new domain in WorkMail and SES, and configures it for use by
        WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.register_mail_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#register_mail_domain)
        """

    async def register_to_work_mail(
        self, *, OrganizationId: str, EntityId: str, Email: str
    ) -> Dict[str, Any]:
        """
        Registers an existing and disabled user, group, or resource for WorkMail use by
        associating a mailbox and calendaring
        capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.register_to_work_mail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#register_to_work_mail)
        """

    async def reset_password(
        self, *, OrganizationId: str, UserId: str, Password: str
    ) -> Dict[str, Any]:
        """
        Allows the administrator to reset the password for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.reset_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#reset_password)
        """

    async def start_mailbox_export_job(
        self,
        *,
        ClientToken: str,
        OrganizationId: str,
        EntityId: str,
        RoleArn: str,
        KmsKeyArn: str,
        S3BucketName: str,
        S3Prefix: str,
        Description: str = ...,
    ) -> StartMailboxExportJobResponseTypeDef:
        """
        Starts a mailbox export job to export MIME-format email messages and calendar
        items from the specified mailbox to the specified Amazon Simple Storage Service
        (Amazon S3)
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.start_mailbox_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#start_mailbox_export_job)
        """

    async def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Applies the specified tags to the specified WorkMailorganization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#tag_resource)
        """

    async def test_availability_configuration(
        self,
        *,
        OrganizationId: str,
        DomainName: str = ...,
        EwsProvider: EwsAvailabilityProviderTypeDef = ...,
        LambdaProvider: LambdaAvailabilityProviderTypeDef = ...,
    ) -> TestAvailabilityConfigurationResponseTypeDef:
        """
        Performs a test on an availability provider to ensure that access is allowed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.test_availability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#test_availability_configuration)
        """

    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags the specified tags from the specified WorkMail organization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#untag_resource)
        """

    async def update_availability_configuration(
        self,
        *,
        OrganizationId: str,
        DomainName: str,
        EwsProvider: EwsAvailabilityProviderTypeDef = ...,
        LambdaProvider: LambdaAvailabilityProviderTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an existing `AvailabilityConfiguration` for the given WorkMail
        organization and
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_availability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_availability_configuration)
        """

    async def update_default_mail_domain(
        self, *, OrganizationId: str, DomainName: str
    ) -> Dict[str, Any]:
        """
        Updates the default mail domain for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_default_mail_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_default_mail_domain)
        """

    async def update_group(
        self, *, OrganizationId: str, GroupId: str, HiddenFromGlobalAddressList: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates attibutes in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_group)
        """

    async def update_impersonation_role(
        self,
        *,
        OrganizationId: str,
        ImpersonationRoleId: str,
        Name: str,
        Type: ImpersonationRoleTypeType,
        Rules: Sequence[ImpersonationRuleUnionTypeDef],
        Description: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_impersonation_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_impersonation_role)
        """

    async def update_mailbox_quota(
        self, *, OrganizationId: str, UserId: str, MailboxQuota: int
    ) -> Dict[str, Any]:
        """
        Updates a user's current mailbox quota for a specified organization and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_mailbox_quota)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_mailbox_quota)
        """

    async def update_mobile_device_access_rule(
        self,
        *,
        OrganizationId: str,
        MobileDeviceAccessRuleId: str,
        Name: str,
        Effect: MobileDeviceAccessRuleEffectType,
        Description: str = ...,
        DeviceTypes: Sequence[str] = ...,
        NotDeviceTypes: Sequence[str] = ...,
        DeviceModels: Sequence[str] = ...,
        NotDeviceModels: Sequence[str] = ...,
        DeviceOperatingSystems: Sequence[str] = ...,
        NotDeviceOperatingSystems: Sequence[str] = ...,
        DeviceUserAgents: Sequence[str] = ...,
        NotDeviceUserAgents: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Updates a mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_mobile_device_access_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_mobile_device_access_rule)
        """

    async def update_primary_email_address(
        self, *, OrganizationId: str, EntityId: str, Email: str
    ) -> Dict[str, Any]:
        """
        Updates the primary email for a user, group, or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_primary_email_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_primary_email_address)
        """

    async def update_resource(
        self,
        *,
        OrganizationId: str,
        ResourceId: str,
        Name: str = ...,
        BookingOptions: BookingOptionsTypeDef = ...,
        Description: str = ...,
        Type: ResourceTypeType = ...,
        HiddenFromGlobalAddressList: bool = ...,
    ) -> Dict[str, Any]:
        """
        Updates data for the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_resource)
        """

    async def update_user(
        self,
        *,
        OrganizationId: str,
        UserId: str,
        Role: UserRoleType = ...,
        DisplayName: str = ...,
        FirstName: str = ...,
        LastName: str = ...,
        HiddenFromGlobalAddressList: bool = ...,
        Initials: str = ...,
        Telephone: str = ...,
        Street: str = ...,
        JobTitle: str = ...,
        City: str = ...,
        Company: str = ...,
        ZipCode: str = ...,
        Department: str = ...,
        Country: str = ...,
        Office: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates data for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_availability_configurations"]
    ) -> ListAvailabilityConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_members"]
    ) -> ListGroupMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mailbox_permissions"]
    ) -> ListMailboxPermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organizations"]
    ) -> ListOrganizationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_delegates"]
    ) -> ListResourceDelegatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    async def __aenter__(self) -> "WorkMailClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
        """
