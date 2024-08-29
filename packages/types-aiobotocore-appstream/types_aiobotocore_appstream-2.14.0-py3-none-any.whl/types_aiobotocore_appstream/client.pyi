"""
Type annotations for appstream service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appstream.client import AppStreamClient

    session = get_session()
    async with session.create_client("appstream") as client:
        client: AppStreamClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AppBlockBuilderAttributeType,
    ApplicationAttributeType,
    AppVisibilityType,
    AuthenticationTypeType,
    FleetAttributeType,
    FleetTypeType,
    MessageActionType,
    PackagingTypeType,
    PlatformTypeType,
    StackAttributeType,
    StreamViewType,
    ThemeStateType,
    ThemeStylingType,
    VisibilityTypeType,
)
from .paginator import (
    DescribeDirectoryConfigsPaginator,
    DescribeFleetsPaginator,
    DescribeImageBuildersPaginator,
    DescribeImagesPaginator,
    DescribeSessionsPaginator,
    DescribeStacksPaginator,
    DescribeUsersPaginator,
    DescribeUserStackAssociationsPaginator,
    ListAssociatedFleetsPaginator,
    ListAssociatedStacksPaginator,
)
from .type_defs import (
    AccessEndpointTypeDef,
    ApplicationSettingsTypeDef,
    AssociateAppBlockBuilderAppBlockResultTypeDef,
    AssociateApplicationFleetResultTypeDef,
    BatchAssociateUserStackResultTypeDef,
    BatchDisassociateUserStackResultTypeDef,
    CertificateBasedAuthPropertiesTypeDef,
    ComputeCapacityTypeDef,
    CopyImageResponseTypeDef,
    CreateAppBlockBuilderResultTypeDef,
    CreateAppBlockBuilderStreamingURLResultTypeDef,
    CreateAppBlockResultTypeDef,
    CreateApplicationResultTypeDef,
    CreateDirectoryConfigResultTypeDef,
    CreateEntitlementResultTypeDef,
    CreateFleetResultTypeDef,
    CreateImageBuilderResultTypeDef,
    CreateImageBuilderStreamingURLResultTypeDef,
    CreateStackResultTypeDef,
    CreateStreamingURLResultTypeDef,
    CreateThemeForStackResultTypeDef,
    CreateUpdatedImageResultTypeDef,
    CreateUsageReportSubscriptionResultTypeDef,
    DeleteImageBuilderResultTypeDef,
    DeleteImageResultTypeDef,
    DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef,
    DescribeAppBlockBuildersResultTypeDef,
    DescribeAppBlocksResultTypeDef,
    DescribeApplicationFleetAssociationsResultTypeDef,
    DescribeApplicationsResultTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeEntitlementsResultTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagePermissionsResultTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksResultTypeDef,
    DescribeThemeForStackResultTypeDef,
    DescribeUsageReportSubscriptionsResultTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    DomainJoinInfoTypeDef,
    EntitlementAttributeTypeDef,
    ImagePermissionsTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksResultTypeDef,
    ListEntitledApplicationsResultTypeDef,
    ListTagsForResourceResponseTypeDef,
    S3LocationTypeDef,
    ScriptDetailsTypeDef,
    ServiceAccountCredentialsTypeDef,
    StartAppBlockBuilderResultTypeDef,
    StartImageBuilderResultTypeDef,
    StopAppBlockBuilderResultTypeDef,
    StopImageBuilderResultTypeDef,
    StorageConnectorUnionTypeDef,
    StreamingExperienceSettingsTypeDef,
    ThemeFooterLinkTypeDef,
    UpdateAppBlockBuilderResultTypeDef,
    UpdateApplicationResultTypeDef,
    UpdateDirectoryConfigResultTypeDef,
    UpdateEntitlementResultTypeDef,
    UpdateFleetResultTypeDef,
    UpdateStackResultTypeDef,
    UpdateThemeForStackResultTypeDef,
    UserSettingTypeDef,
    UserStackAssociationTypeDef,
    VpcConfigUnionTypeDef,
)
from .waiter import FleetStartedWaiter, FleetStoppedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AppStreamClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    EntitlementAlreadyExistsException: Type[BotocoreClientError]
    EntitlementNotFoundException: Type[BotocoreClientError]
    IncompatibleImageException: Type[BotocoreClientError]
    InvalidAccountStatusException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidRoleException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    RequestLimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotAvailableException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class AppStreamClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppStreamClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#exceptions)
        """

    async def associate_app_block_builder_app_block(
        self, *, AppBlockArn: str, AppBlockBuilderName: str
    ) -> AssociateAppBlockBuilderAppBlockResultTypeDef:
        """
        Associates the specified app block builder with the specified app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_app_block_builder_app_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_app_block_builder_app_block)
        """

    async def associate_application_fleet(
        self, *, FleetName: str, ApplicationArn: str
    ) -> AssociateApplicationFleetResultTypeDef:
        """
        Associates the specified application with the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_application_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_application_fleet)
        """

    async def associate_application_to_entitlement(
        self, *, StackName: str, EntitlementName: str, ApplicationIdentifier: str
    ) -> Dict[str, Any]:
        """
        Associates an application to entitle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_application_to_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_application_to_entitlement)
        """

    async def associate_fleet(self, *, FleetName: str, StackName: str) -> Dict[str, Any]:
        """
        Associates the specified fleet with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.associate_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_fleet)
        """

    async def batch_associate_user_stack(
        self, *, UserStackAssociations: Sequence[UserStackAssociationTypeDef]
    ) -> BatchAssociateUserStackResultTypeDef:
        """
        Associates the specified users with the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.batch_associate_user_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#batch_associate_user_stack)
        """

    async def batch_disassociate_user_stack(
        self, *, UserStackAssociations: Sequence[UserStackAssociationTypeDef]
    ) -> BatchDisassociateUserStackResultTypeDef:
        """
        Disassociates the specified users from the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.batch_disassociate_user_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#batch_disassociate_user_stack)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#close)
        """

    async def copy_image(
        self,
        *,
        SourceImageName: str,
        DestinationImageName: str,
        DestinationRegion: str,
        DestinationImageDescription: str = ...,
    ) -> CopyImageResponseTypeDef:
        """
        Copies the image within the same region or to a new region within the same AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.copy_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#copy_image)
        """

    async def create_app_block(
        self,
        *,
        Name: str,
        SourceS3Location: S3LocationTypeDef,
        Description: str = ...,
        DisplayName: str = ...,
        SetupScriptDetails: ScriptDetailsTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        PostSetupScriptDetails: ScriptDetailsTypeDef = ...,
        PackagingType: PackagingTypeType = ...,
    ) -> CreateAppBlockResultTypeDef:
        """
        Creates an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_app_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block)
        """

    async def create_app_block_builder(
        self,
        *,
        Name: str,
        Platform: Literal["WINDOWS_SERVER_2019"],
        InstanceType: str,
        VpcConfig: VpcConfigUnionTypeDef,
        Description: str = ...,
        DisplayName: str = ...,
        Tags: Mapping[str, str] = ...,
        EnableDefaultInternetAccess: bool = ...,
        IamRoleArn: str = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
    ) -> CreateAppBlockBuilderResultTypeDef:
        """
        Creates an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_app_block_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block_builder)
        """

    async def create_app_block_builder_streaming_url(
        self, *, AppBlockBuilderName: str, Validity: int = ...
    ) -> CreateAppBlockBuilderStreamingURLResultTypeDef:
        """
        Creates a URL to start a create app block builder streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_app_block_builder_streaming_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block_builder_streaming_url)
        """

    async def create_application(
        self,
        *,
        Name: str,
        IconS3Location: S3LocationTypeDef,
        LaunchPath: str,
        Platforms: Sequence[PlatformTypeType],
        InstanceFamilies: Sequence[str],
        AppBlockArn: str,
        DisplayName: str = ...,
        Description: str = ...,
        WorkingDirectory: str = ...,
        LaunchParameters: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateApplicationResultTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_application)
        """

    async def create_directory_config(
        self,
        *,
        DirectoryName: str,
        OrganizationalUnitDistinguishedNames: Sequence[str],
        ServiceAccountCredentials: ServiceAccountCredentialsTypeDef = ...,
        CertificateBasedAuthProperties: CertificateBasedAuthPropertiesTypeDef = ...,
    ) -> CreateDirectoryConfigResultTypeDef:
        """
        Creates a Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_directory_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_directory_config)
        """

    async def create_entitlement(
        self,
        *,
        Name: str,
        StackName: str,
        AppVisibility: AppVisibilityType,
        Attributes: Sequence[EntitlementAttributeTypeDef],
        Description: str = ...,
    ) -> CreateEntitlementResultTypeDef:
        """
        Creates a new entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_entitlement)
        """

    async def create_fleet(
        self,
        *,
        Name: str,
        InstanceType: str,
        ImageName: str = ...,
        ImageArn: str = ...,
        FleetType: FleetTypeType = ...,
        ComputeCapacity: ComputeCapacityTypeDef = ...,
        VpcConfig: VpcConfigUnionTypeDef = ...,
        MaxUserDurationInSeconds: int = ...,
        DisconnectTimeoutInSeconds: int = ...,
        Description: str = ...,
        DisplayName: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        IdleDisconnectTimeoutInSeconds: int = ...,
        IamRoleArn: str = ...,
        StreamView: StreamViewType = ...,
        Platform: PlatformTypeType = ...,
        MaxConcurrentSessions: int = ...,
        UsbDeviceFilterStrings: Sequence[str] = ...,
        SessionScriptS3Location: S3LocationTypeDef = ...,
        MaxSessionsPerInstance: int = ...,
    ) -> CreateFleetResultTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_fleet)
        """

    async def create_image_builder(
        self,
        *,
        Name: str,
        InstanceType: str,
        ImageName: str = ...,
        ImageArn: str = ...,
        Description: str = ...,
        DisplayName: str = ...,
        VpcConfig: VpcConfigUnionTypeDef = ...,
        IamRoleArn: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        AppstreamAgentVersion: str = ...,
        Tags: Mapping[str, str] = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
    ) -> CreateImageBuilderResultTypeDef:
        """
        Creates an image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_image_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_image_builder)
        """

    async def create_image_builder_streaming_url(
        self, *, Name: str, Validity: int = ...
    ) -> CreateImageBuilderStreamingURLResultTypeDef:
        """
        Creates a URL to start an image builder streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_image_builder_streaming_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_image_builder_streaming_url)
        """

    async def create_stack(
        self,
        *,
        Name: str,
        Description: str = ...,
        DisplayName: str = ...,
        StorageConnectors: Sequence[StorageConnectorUnionTypeDef] = ...,
        RedirectURL: str = ...,
        FeedbackURL: str = ...,
        UserSettings: Sequence[UserSettingTypeDef] = ...,
        ApplicationSettings: ApplicationSettingsTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
        EmbedHostDomains: Sequence[str] = ...,
        StreamingExperienceSettings: StreamingExperienceSettingsTypeDef = ...,
    ) -> CreateStackResultTypeDef:
        """
        Creates a stack to start streaming applications to users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_stack)
        """

    async def create_streaming_url(
        self,
        *,
        StackName: str,
        FleetName: str,
        UserId: str,
        ApplicationId: str = ...,
        Validity: int = ...,
        SessionContext: str = ...,
    ) -> CreateStreamingURLResultTypeDef:
        """
        Creates a temporary URL to start an AppStream 2.0 streaming session for the
        specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_streaming_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_streaming_url)
        """

    async def create_theme_for_stack(
        self,
        *,
        StackName: str,
        TitleText: str,
        ThemeStyling: ThemeStylingType,
        OrganizationLogoS3Location: S3LocationTypeDef,
        FaviconS3Location: S3LocationTypeDef,
        FooterLinks: Sequence[ThemeFooterLinkTypeDef] = ...,
    ) -> CreateThemeForStackResultTypeDef:
        """
        Creates custom branding that customizes the appearance of the streaming
        application catalog
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_theme_for_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_theme_for_stack)
        """

    async def create_updated_image(
        self,
        *,
        existingImageName: str,
        newImageName: str,
        newImageDescription: str = ...,
        newImageDisplayName: str = ...,
        newImageTags: Mapping[str, str] = ...,
        dryRun: bool = ...,
    ) -> CreateUpdatedImageResultTypeDef:
        """
        Creates a new image with the latest Windows operating system updates, driver
        updates, and AppStream 2.0 agent
        software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_updated_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_updated_image)
        """

    async def create_usage_report_subscription(self) -> CreateUsageReportSubscriptionResultTypeDef:
        """
        Creates a usage report subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_usage_report_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_usage_report_subscription)
        """

    async def create_user(
        self,
        *,
        UserName: str,
        AuthenticationType: AuthenticationTypeType,
        MessageAction: MessageActionType = ...,
        FirstName: str = ...,
        LastName: str = ...,
    ) -> Dict[str, Any]:
        """
        Creates a new user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_user)
        """

    async def delete_app_block(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_app_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_app_block)
        """

    async def delete_app_block_builder(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_app_block_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_app_block_builder)
        """

    async def delete_application(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_application)
        """

    async def delete_directory_config(self, *, DirectoryName: str) -> Dict[str, Any]:
        """
        Deletes the specified Directory Config object from AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_directory_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_directory_config)
        """

    async def delete_entitlement(self, *, Name: str, StackName: str) -> Dict[str, Any]:
        """
        Deletes the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_entitlement)
        """

    async def delete_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_fleet)
        """

    async def delete_image(self, *, Name: str) -> DeleteImageResultTypeDef:
        """
        Deletes the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image)
        """

    async def delete_image_builder(self, *, Name: str) -> DeleteImageBuilderResultTypeDef:
        """
        Deletes the specified image builder and releases the capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image_builder)
        """

    async def delete_image_permissions(self, *, Name: str, SharedAccountId: str) -> Dict[str, Any]:
        """
        Deletes permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_image_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image_permissions)
        """

    async def delete_stack(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_stack)
        """

    async def delete_theme_for_stack(self, *, StackName: str) -> Dict[str, Any]:
        """
        Deletes custom branding that customizes the appearance of the streaming
        application catalog
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_theme_for_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_theme_for_stack)
        """

    async def delete_usage_report_subscription(self) -> Dict[str, Any]:
        """
        Disables usage report generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_usage_report_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_usage_report_subscription)
        """

    async def delete_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Deletes a user from the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_user)
        """

    async def describe_app_block_builder_app_block_associations(
        self,
        *,
        AppBlockArn: str = ...,
        AppBlockBuilderName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef:
        """
        Retrieves a list that describes one or more app block builder associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_app_block_builder_app_block_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_block_builder_app_block_associations)
        """

    async def describe_app_block_builders(
        self, *, Names: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeAppBlockBuildersResultTypeDef:
        """
        Retrieves a list that describes one or more app block builders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_app_block_builders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_block_builders)
        """

    async def describe_app_blocks(
        self, *, Arns: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeAppBlocksResultTypeDef:
        """
        Retrieves a list that describes one or more app blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_app_blocks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_blocks)
        """

    async def describe_application_fleet_associations(
        self,
        *,
        FleetName: str = ...,
        ApplicationArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeApplicationFleetAssociationsResultTypeDef:
        """
        Retrieves a list that describes one or more application fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_application_fleet_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_application_fleet_associations)
        """

    async def describe_applications(
        self, *, Arns: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeApplicationsResultTypeDef:
        """
        Retrieves a list that describes one or more applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_applications)
        """

    async def describe_directory_configs(
        self, *, DirectoryNames: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDirectoryConfigsResultTypeDef:
        """
        Retrieves a list that describes one or more specified Directory Config objects
        for AppStream 2.0, if the names for these objects are
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_directory_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_directory_configs)
        """

    async def describe_entitlements(
        self, *, StackName: str, Name: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeEntitlementsResultTypeDef:
        """
        Retrieves a list that describes one of more entitlements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_entitlements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_entitlements)
        """

    async def describe_fleets(
        self, *, Names: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeFleetsResultTypeDef:
        """
        Retrieves a list that describes one or more specified fleets, if the fleet
        names are
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_fleets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_fleets)
        """

    async def describe_image_builders(
        self, *, Names: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeImageBuildersResultTypeDef:
        """
        Retrieves a list that describes one or more specified image builders, if the
        image builder names are
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_image_builders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_image_builders)
        """

    async def describe_image_permissions(
        self,
        *,
        Name: str,
        MaxResults: int = ...,
        SharedAwsAccountIds: Sequence[str] = ...,
        NextToken: str = ...,
    ) -> DescribeImagePermissionsResultTypeDef:
        """
        Retrieves a list that describes the permissions for shared AWS account IDs on a
        private image that you
        own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_image_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_image_permissions)
        """

    async def describe_images(
        self,
        *,
        Names: Sequence[str] = ...,
        Arns: Sequence[str] = ...,
        Type: VisibilityTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> DescribeImagesResultTypeDef:
        """
        Retrieves a list that describes one or more specified images, if the image
        names or image ARNs are
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_images)
        """

    async def describe_sessions(
        self,
        *,
        StackName: str,
        FleetName: str,
        UserId: str = ...,
        NextToken: str = ...,
        Limit: int = ...,
        AuthenticationType: AuthenticationTypeType = ...,
        InstanceId: str = ...,
    ) -> DescribeSessionsResultTypeDef:
        """
        Retrieves a list that describes the streaming sessions for a specified stack
        and
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_sessions)
        """

    async def describe_stacks(
        self, *, Names: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeStacksResultTypeDef:
        """
        Retrieves a list that describes one or more specified stacks, if the stack
        names are
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_stacks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_stacks)
        """

    async def describe_theme_for_stack(
        self, *, StackName: str
    ) -> DescribeThemeForStackResultTypeDef:
        """
        Retrieves a list that describes the theme for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_theme_for_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_theme_for_stack)
        """

    async def describe_usage_report_subscriptions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeUsageReportSubscriptionsResultTypeDef:
        """
        Retrieves a list that describes one or more usage report subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_usage_report_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_usage_report_subscriptions)
        """

    async def describe_user_stack_associations(
        self,
        *,
        StackName: str = ...,
        UserName: str = ...,
        AuthenticationType: AuthenticationTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeUserStackAssociationsResultTypeDef:
        """
        Retrieves a list that describes the UserStackAssociation objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_user_stack_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_user_stack_associations)
        """

    async def describe_users(
        self,
        *,
        AuthenticationType: AuthenticationTypeType,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeUsersResultTypeDef:
        """
        Retrieves a list that describes one or more specified users in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.describe_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_users)
        """

    async def disable_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Disables the specified user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disable_user)
        """

    async def disassociate_app_block_builder_app_block(
        self, *, AppBlockArn: str, AppBlockBuilderName: str
    ) -> Dict[str, Any]:
        """
        Disassociates a specified app block builder from a specified app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_app_block_builder_app_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_app_block_builder_app_block)
        """

    async def disassociate_application_fleet(
        self, *, FleetName: str, ApplicationArn: str
    ) -> Dict[str, Any]:
        """
        Disassociates the specified application from the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_application_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_application_fleet)
        """

    async def disassociate_application_from_entitlement(
        self, *, StackName: str, EntitlementName: str, ApplicationIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified application from the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_application_from_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_application_from_entitlement)
        """

    async def disassociate_fleet(self, *, FleetName: str, StackName: str) -> Dict[str, Any]:
        """
        Disassociates the specified fleet from the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.disassociate_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_fleet)
        """

    async def enable_user(
        self, *, UserName: str, AuthenticationType: AuthenticationTypeType
    ) -> Dict[str, Any]:
        """
        Enables a user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.enable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#enable_user)
        """

    async def expire_session(self, *, SessionId: str) -> Dict[str, Any]:
        """
        Immediately stops the specified streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.expire_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#expire_session)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#generate_presigned_url)
        """

    async def list_associated_fleets(
        self, *, StackName: str, NextToken: str = ...
    ) -> ListAssociatedFleetsResultTypeDef:
        """
        Retrieves the name of the fleet that is associated with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_associated_fleets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_associated_fleets)
        """

    async def list_associated_stacks(
        self, *, FleetName: str, NextToken: str = ...
    ) -> ListAssociatedStacksResultTypeDef:
        """
        Retrieves the name of the stack with which the specified fleet is associated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_associated_stacks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_associated_stacks)
        """

    async def list_entitled_applications(
        self, *, StackName: str, EntitlementName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEntitledApplicationsResultTypeDef:
        """
        Retrieves a list of entitled applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_entitled_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_entitled_applications)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of all tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_tags_for_resource)
        """

    async def start_app_block_builder(self, *, Name: str) -> StartAppBlockBuilderResultTypeDef:
        """
        Starts an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.start_app_block_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_app_block_builder)
        """

    async def start_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Starts the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.start_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_fleet)
        """

    async def start_image_builder(
        self, *, Name: str, AppstreamAgentVersion: str = ...
    ) -> StartImageBuilderResultTypeDef:
        """
        Starts the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.start_image_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_image_builder)
        """

    async def stop_app_block_builder(self, *, Name: str) -> StopAppBlockBuilderResultTypeDef:
        """
        Stops an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.stop_app_block_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_app_block_builder)
        """

    async def stop_fleet(self, *, Name: str) -> Dict[str, Any]:
        """
        Stops the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.stop_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_fleet)
        """

    async def stop_image_builder(self, *, Name: str) -> StopImageBuilderResultTypeDef:
        """
        Stops the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.stop_image_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_image_builder)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Disassociates one or more specified tags from the specified AppStream 2.0
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#untag_resource)
        """

    async def update_app_block_builder(
        self,
        *,
        Name: str,
        Description: str = ...,
        DisplayName: str = ...,
        Platform: PlatformTypeType = ...,
        InstanceType: str = ...,
        VpcConfig: VpcConfigUnionTypeDef = ...,
        EnableDefaultInternetAccess: bool = ...,
        IamRoleArn: str = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
        AttributesToDelete: Sequence[AppBlockBuilderAttributeType] = ...,
    ) -> UpdateAppBlockBuilderResultTypeDef:
        """
        Updates an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_app_block_builder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_app_block_builder)
        """

    async def update_application(
        self,
        *,
        Name: str,
        DisplayName: str = ...,
        Description: str = ...,
        IconS3Location: S3LocationTypeDef = ...,
        LaunchPath: str = ...,
        WorkingDirectory: str = ...,
        LaunchParameters: str = ...,
        AppBlockArn: str = ...,
        AttributesToDelete: Sequence[ApplicationAttributeType] = ...,
    ) -> UpdateApplicationResultTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_application)
        """

    async def update_directory_config(
        self,
        *,
        DirectoryName: str,
        OrganizationalUnitDistinguishedNames: Sequence[str] = ...,
        ServiceAccountCredentials: ServiceAccountCredentialsTypeDef = ...,
        CertificateBasedAuthProperties: CertificateBasedAuthPropertiesTypeDef = ...,
    ) -> UpdateDirectoryConfigResultTypeDef:
        """
        Updates the specified Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_directory_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_directory_config)
        """

    async def update_entitlement(
        self,
        *,
        Name: str,
        StackName: str,
        Description: str = ...,
        AppVisibility: AppVisibilityType = ...,
        Attributes: Sequence[EntitlementAttributeTypeDef] = ...,
    ) -> UpdateEntitlementResultTypeDef:
        """
        Updates the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_entitlement)
        """

    async def update_fleet(
        self,
        *,
        ImageName: str = ...,
        ImageArn: str = ...,
        Name: str = ...,
        InstanceType: str = ...,
        ComputeCapacity: ComputeCapacityTypeDef = ...,
        VpcConfig: VpcConfigUnionTypeDef = ...,
        MaxUserDurationInSeconds: int = ...,
        DisconnectTimeoutInSeconds: int = ...,
        DeleteVpcConfig: bool = ...,
        Description: str = ...,
        DisplayName: str = ...,
        EnableDefaultInternetAccess: bool = ...,
        DomainJoinInfo: DomainJoinInfoTypeDef = ...,
        IdleDisconnectTimeoutInSeconds: int = ...,
        AttributesToDelete: Sequence[FleetAttributeType] = ...,
        IamRoleArn: str = ...,
        StreamView: StreamViewType = ...,
        Platform: PlatformTypeType = ...,
        MaxConcurrentSessions: int = ...,
        UsbDeviceFilterStrings: Sequence[str] = ...,
        SessionScriptS3Location: S3LocationTypeDef = ...,
        MaxSessionsPerInstance: int = ...,
    ) -> UpdateFleetResultTypeDef:
        """
        Updates the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_fleet)
        """

    async def update_image_permissions(
        self, *, Name: str, SharedAccountId: str, ImagePermissions: ImagePermissionsTypeDef
    ) -> Dict[str, Any]:
        """
        Adds or updates permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_image_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_image_permissions)
        """

    async def update_stack(
        self,
        *,
        Name: str,
        DisplayName: str = ...,
        Description: str = ...,
        StorageConnectors: Sequence[StorageConnectorUnionTypeDef] = ...,
        DeleteStorageConnectors: bool = ...,
        RedirectURL: str = ...,
        FeedbackURL: str = ...,
        AttributesToDelete: Sequence[StackAttributeType] = ...,
        UserSettings: Sequence[UserSettingTypeDef] = ...,
        ApplicationSettings: ApplicationSettingsTypeDef = ...,
        AccessEndpoints: Sequence[AccessEndpointTypeDef] = ...,
        EmbedHostDomains: Sequence[str] = ...,
        StreamingExperienceSettings: StreamingExperienceSettingsTypeDef = ...,
    ) -> UpdateStackResultTypeDef:
        """
        Updates the specified fields for the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_stack)
        """

    async def update_theme_for_stack(
        self,
        *,
        StackName: str,
        FooterLinks: Sequence[ThemeFooterLinkTypeDef] = ...,
        TitleText: str = ...,
        ThemeStyling: ThemeStylingType = ...,
        OrganizationLogoS3Location: S3LocationTypeDef = ...,
        FaviconS3Location: S3LocationTypeDef = ...,
        State: ThemeStateType = ...,
        AttributesToDelete: Sequence[Literal["FOOTER_LINKS"]] = ...,
    ) -> UpdateThemeForStackResultTypeDef:
        """
        Updates custom branding that customizes the appearance of the streaming
        application catalog
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.update_theme_for_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_theme_for_stack)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_directory_configs"]
    ) -> DescribeDirectoryConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_fleets"]) -> DescribeFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_image_builders"]
    ) -> DescribeImageBuildersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_sessions"]
    ) -> DescribeSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stacks"]) -> DescribeStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_user_stack_associations"]
    ) -> DescribeUserStackAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_fleets"]
    ) -> ListAssociatedFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_stacks"]
    ) -> ListAssociatedStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_started"]) -> FleetStartedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_stopped"]) -> FleetStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_waiter)
        """

    async def __aenter__(self) -> "AppStreamClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
        """
