"""
Type annotations for datazone service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_datazone.client import DataZoneClient

    session = get_session()
    async with session.create_client("datazone") as client:
        client: DataZoneClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ChangeActionType,
    DataAssetActivityStatusType,
    DataSourceRunStatusType,
    DataSourceStatusType,
    DomainStatusType,
    EdgeDirectionType,
    EnableSettingType,
    EntityTypeType,
    EnvironmentStatusType,
    FilterStatusType,
    FormTypeStatusType,
    GlossaryStatusType,
    GlossaryTermStatusType,
    GroupProfileStatusType,
    GroupSearchTypeType,
    InventorySearchScopeType,
    MetadataGenerationRunStatusType,
    NotificationTypeType,
    SearchOutputAdditionalAttributeType,
    SortKeyType,
    SortOrderType,
    SubscriptionGrantStatusType,
    SubscriptionRequestStatusType,
    SubscriptionStatusType,
    TaskStatusType,
    TimeSeriesEntityTypeType,
    TypesSearchScopeType,
    UserDesignationType,
    UserProfileStatusType,
    UserProfileTypeType,
    UserSearchTypeType,
    UserTypeType,
)
from .paginator import (
    ListAssetFiltersPaginator,
    ListAssetRevisionsPaginator,
    ListDataProductRevisionsPaginator,
    ListDataSourceRunActivitiesPaginator,
    ListDataSourceRunsPaginator,
    ListDataSourcesPaginator,
    ListDomainsPaginator,
    ListEnvironmentActionsPaginator,
    ListEnvironmentBlueprintConfigurationsPaginator,
    ListEnvironmentBlueprintsPaginator,
    ListEnvironmentProfilesPaginator,
    ListEnvironmentsPaginator,
    ListLineageNodeHistoryPaginator,
    ListMetadataGenerationRunsPaginator,
    ListNotificationsPaginator,
    ListProjectMembershipsPaginator,
    ListProjectsPaginator,
    ListSubscriptionGrantsPaginator,
    ListSubscriptionRequestsPaginator,
    ListSubscriptionsPaginator,
    ListSubscriptionTargetsPaginator,
    ListTimeSeriesDataPointsPaginator,
    SearchGroupProfilesPaginator,
    SearchListingsPaginator,
    SearchPaginator,
    SearchTypesPaginator,
    SearchUserProfilesPaginator,
)
from .type_defs import (
    AcceptChoiceTypeDef,
    AcceptPredictionsOutputTypeDef,
    AcceptRuleTypeDef,
    AcceptSubscriptionRequestOutputTypeDef,
    ActionParametersTypeDef,
    AssetFilterConfigurationUnionTypeDef,
    AssetTargetNameMapTypeDef,
    BlobTypeDef,
    CancelSubscriptionOutputTypeDef,
    CreateAssetFilterOutputTypeDef,
    CreateAssetOutputTypeDef,
    CreateAssetRevisionOutputTypeDef,
    CreateAssetTypeOutputTypeDef,
    CreateDataProductOutputTypeDef,
    CreateDataProductRevisionOutputTypeDef,
    CreateDataSourceOutputTypeDef,
    CreateDomainOutputTypeDef,
    CreateEnvironmentActionOutputTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateEnvironmentProfileOutputTypeDef,
    CreateFormTypeOutputTypeDef,
    CreateGlossaryOutputTypeDef,
    CreateGlossaryTermOutputTypeDef,
    CreateGroupProfileOutputTypeDef,
    CreateListingChangeSetOutputTypeDef,
    CreateProjectOutputTypeDef,
    CreateSubscriptionGrantOutputTypeDef,
    CreateSubscriptionRequestOutputTypeDef,
    CreateSubscriptionTargetOutputTypeDef,
    CreateUserProfileOutputTypeDef,
    DataProductItemUnionTypeDef,
    DataSourceConfigurationInputTypeDef,
    DeleteDataSourceOutputTypeDef,
    DeleteDomainOutputTypeDef,
    DeleteSubscriptionGrantOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EnvironmentParameterTypeDef,
    FailureCauseTypeDef,
    FilterClauseTypeDef,
    FormEntryInputTypeDef,
    FormInputTypeDef,
    GetAssetFilterOutputTypeDef,
    GetAssetOutputTypeDef,
    GetAssetTypeOutputTypeDef,
    GetDataProductOutputTypeDef,
    GetDataSourceOutputTypeDef,
    GetDataSourceRunOutputTypeDef,
    GetDomainOutputTypeDef,
    GetEnvironmentActionOutputTypeDef,
    GetEnvironmentBlueprintConfigurationOutputTypeDef,
    GetEnvironmentBlueprintOutputTypeDef,
    GetEnvironmentCredentialsOutputTypeDef,
    GetEnvironmentOutputTypeDef,
    GetEnvironmentProfileOutputTypeDef,
    GetFormTypeOutputTypeDef,
    GetGlossaryOutputTypeDef,
    GetGlossaryTermOutputTypeDef,
    GetGroupProfileOutputTypeDef,
    GetIamPortalLoginUrlOutputTypeDef,
    GetLineageNodeOutputTypeDef,
    GetListingOutputTypeDef,
    GetMetadataGenerationRunOutputTypeDef,
    GetProjectOutputTypeDef,
    GetSubscriptionGrantOutputTypeDef,
    GetSubscriptionOutputTypeDef,
    GetSubscriptionRequestDetailsOutputTypeDef,
    GetSubscriptionTargetOutputTypeDef,
    GetTimeSeriesDataPointOutputTypeDef,
    GetUserProfileOutputTypeDef,
    GrantedEntityInputTypeDef,
    ListAssetFiltersOutputTypeDef,
    ListAssetRevisionsOutputTypeDef,
    ListDataProductRevisionsOutputTypeDef,
    ListDataSourceRunActivitiesOutputTypeDef,
    ListDataSourceRunsOutputTypeDef,
    ListDataSourcesOutputTypeDef,
    ListDomainsOutputTypeDef,
    ListEnvironmentActionsOutputTypeDef,
    ListEnvironmentBlueprintConfigurationsOutputTypeDef,
    ListEnvironmentBlueprintsOutputTypeDef,
    ListEnvironmentProfilesOutputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListLineageNodeHistoryOutputTypeDef,
    ListMetadataGenerationRunsOutputTypeDef,
    ListNotificationsOutputTypeDef,
    ListProjectMembershipsOutputTypeDef,
    ListProjectsOutputTypeDef,
    ListSubscriptionGrantsOutputTypeDef,
    ListSubscriptionRequestsOutputTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListSubscriptionTargetsOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimeSeriesDataPointsOutputTypeDef,
    MemberTypeDef,
    MetadataGenerationRunTargetTypeDef,
    ModelTypeDef,
    PostTimeSeriesDataPointsOutputTypeDef,
    PredictionConfigurationTypeDef,
    ProvisioningConfigurationUnionTypeDef,
    PutEnvironmentBlueprintConfigurationOutputTypeDef,
    RecommendationConfigurationTypeDef,
    RejectChoiceTypeDef,
    RejectPredictionsOutputTypeDef,
    RejectRuleTypeDef,
    RejectSubscriptionRequestOutputTypeDef,
    RevokeSubscriptionOutputTypeDef,
    ScheduleConfigurationTypeDef,
    SearchGroupProfilesOutputTypeDef,
    SearchInItemTypeDef,
    SearchListingsOutputTypeDef,
    SearchOutputTypeDef,
    SearchSortTypeDef,
    SearchTypesOutputTypeDef,
    SearchUserProfilesOutputTypeDef,
    SingleSignOnTypeDef,
    StartDataSourceRunOutputTypeDef,
    StartMetadataGenerationRunOutputTypeDef,
    SubscribedListingInputTypeDef,
    SubscribedPrincipalInputTypeDef,
    SubscriptionTargetFormTypeDef,
    TermRelationsUnionTypeDef,
    TimeSeriesDataPointFormInputTypeDef,
    TimestampTypeDef,
    UpdateAssetFilterOutputTypeDef,
    UpdateDataSourceOutputTypeDef,
    UpdateDomainOutputTypeDef,
    UpdateEnvironmentActionOutputTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateEnvironmentProfileOutputTypeDef,
    UpdateGlossaryOutputTypeDef,
    UpdateGlossaryTermOutputTypeDef,
    UpdateGroupProfileOutputTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateSubscriptionGrantStatusOutputTypeDef,
    UpdateSubscriptionRequestOutputTypeDef,
    UpdateSubscriptionTargetOutputTypeDef,
    UpdateUserProfileOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DataZoneClient",)

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
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DataZoneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataZoneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#exceptions)
        """

    async def accept_predictions(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        acceptChoices: Sequence[AcceptChoiceTypeDef] = ...,
        acceptRule: AcceptRuleTypeDef = ...,
        clientToken: str = ...,
        revision: str = ...,
    ) -> AcceptPredictionsOutputTypeDef:
        """
        Accepts automatically generated business-friendly metadata for your Amazon
        DataZone
        assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.accept_predictions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#accept_predictions)
        """

    async def accept_subscription_request(
        self, *, domainIdentifier: str, identifier: str, decisionComment: str = ...
    ) -> AcceptSubscriptionRequestOutputTypeDef:
        """
        Accepts a subscription request to a specific asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.accept_subscription_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#accept_subscription_request)
        """

    async def associate_environment_role(
        self, *, domainIdentifier: str, environmentIdentifier: str, environmentRoleArn: str
    ) -> Dict[str, Any]:
        """
        Associates the environment role in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.associate_environment_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#associate_environment_role)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#can_paginate)
        """

    async def cancel_metadata_generation_run(
        self, *, domainIdentifier: str, identifier: str
    ) -> Dict[str, Any]:
        """
        Cancels the metadata generation run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.cancel_metadata_generation_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#cancel_metadata_generation_run)
        """

    async def cancel_subscription(
        self, *, domainIdentifier: str, identifier: str
    ) -> CancelSubscriptionOutputTypeDef:
        """
        Cancels the subscription to the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.cancel_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#cancel_subscription)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#close)
        """

    async def create_asset(
        self,
        *,
        domainIdentifier: str,
        name: str,
        owningProjectIdentifier: str,
        typeIdentifier: str,
        clientToken: str = ...,
        description: str = ...,
        externalIdentifier: str = ...,
        formsInput: Sequence[FormInputTypeDef] = ...,
        glossaryTerms: Sequence[str] = ...,
        predictionConfiguration: PredictionConfigurationTypeDef = ...,
        typeRevision: str = ...,
    ) -> CreateAssetOutputTypeDef:
        """
        Creates an asset in Amazon DataZone catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_asset)
        """

    async def create_asset_filter(
        self,
        *,
        assetIdentifier: str,
        configuration: AssetFilterConfigurationUnionTypeDef,
        domainIdentifier: str,
        name: str,
        clientToken: str = ...,
        description: str = ...,
    ) -> CreateAssetFilterOutputTypeDef:
        """
        Creates a data asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_asset_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_asset_filter)
        """

    async def create_asset_revision(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        formsInput: Sequence[FormInputTypeDef] = ...,
        glossaryTerms: Sequence[str] = ...,
        predictionConfiguration: PredictionConfigurationTypeDef = ...,
        typeRevision: str = ...,
    ) -> CreateAssetRevisionOutputTypeDef:
        """
        Creates a revision of the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_asset_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_asset_revision)
        """

    async def create_asset_type(
        self,
        *,
        domainIdentifier: str,
        formsInput: Mapping[str, FormEntryInputTypeDef],
        name: str,
        owningProjectIdentifier: str,
        description: str = ...,
    ) -> CreateAssetTypeOutputTypeDef:
        """
        Creates a custom asset type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_asset_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_asset_type)
        """

    async def create_data_product(
        self,
        *,
        domainIdentifier: str,
        name: str,
        owningProjectIdentifier: str,
        clientToken: str = ...,
        description: str = ...,
        formsInput: Sequence[FormInputTypeDef] = ...,
        glossaryTerms: Sequence[str] = ...,
        items: Sequence[DataProductItemUnionTypeDef] = ...,
    ) -> CreateDataProductOutputTypeDef:
        """
        Creates a data product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_data_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_data_product)
        """

    async def create_data_product_revision(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        formsInput: Sequence[FormInputTypeDef] = ...,
        glossaryTerms: Sequence[str] = ...,
        items: Sequence[DataProductItemUnionTypeDef] = ...,
    ) -> CreateDataProductRevisionOutputTypeDef:
        """
        Creates a data product revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_data_product_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_data_product_revision)
        """

    async def create_data_source(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        name: str,
        projectIdentifier: str,
        type: str,
        assetFormsInput: Sequence[FormInputTypeDef] = ...,
        clientToken: str = ...,
        configuration: DataSourceConfigurationInputTypeDef = ...,
        description: str = ...,
        enableSetting: EnableSettingType = ...,
        publishOnImport: bool = ...,
        recommendation: RecommendationConfigurationTypeDef = ...,
        schedule: ScheduleConfigurationTypeDef = ...,
    ) -> CreateDataSourceOutputTypeDef:
        """
        Creates an Amazon DataZone data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_data_source)
        """

    async def create_domain(
        self,
        *,
        domainExecutionRole: str,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        kmsKeyIdentifier: str = ...,
        singleSignOn: SingleSignOnTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateDomainOutputTypeDef:
        """
        Creates an Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_domain)
        """

    async def create_environment(
        self,
        *,
        domainIdentifier: str,
        environmentProfileIdentifier: str,
        name: str,
        projectIdentifier: str,
        description: str = ...,
        environmentAccountIdentifier: str = ...,
        environmentAccountRegion: str = ...,
        environmentBlueprintIdentifier: str = ...,
        glossaryTerms: Sequence[str] = ...,
        userParameters: Sequence[EnvironmentParameterTypeDef] = ...,
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Create an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_environment)
        """

    async def create_environment_action(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        name: str,
        parameters: ActionParametersTypeDef,
        description: str = ...,
    ) -> CreateEnvironmentActionOutputTypeDef:
        """
        Creates an action for the environment, for example, creates a console link for
        an analytics tool that is available in this
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_environment_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_environment_action)
        """

    async def create_environment_profile(
        self,
        *,
        domainIdentifier: str,
        environmentBlueprintIdentifier: str,
        name: str,
        projectIdentifier: str,
        awsAccountId: str = ...,
        awsAccountRegion: str = ...,
        description: str = ...,
        userParameters: Sequence[EnvironmentParameterTypeDef] = ...,
    ) -> CreateEnvironmentProfileOutputTypeDef:
        """
        Creates an Amazon DataZone environment profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_environment_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_environment_profile)
        """

    async def create_form_type(
        self,
        *,
        domainIdentifier: str,
        model: ModelTypeDef,
        name: str,
        owningProjectIdentifier: str,
        description: str = ...,
        status: FormTypeStatusType = ...,
    ) -> CreateFormTypeOutputTypeDef:
        """
        Creates a metadata form type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_form_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_form_type)
        """

    async def create_glossary(
        self,
        *,
        domainIdentifier: str,
        name: str,
        owningProjectIdentifier: str,
        clientToken: str = ...,
        description: str = ...,
        status: GlossaryStatusType = ...,
    ) -> CreateGlossaryOutputTypeDef:
        """
        Creates an Amazon DataZone business glossary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_glossary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_glossary)
        """

    async def create_glossary_term(
        self,
        *,
        domainIdentifier: str,
        glossaryIdentifier: str,
        name: str,
        clientToken: str = ...,
        longDescription: str = ...,
        shortDescription: str = ...,
        status: GlossaryTermStatusType = ...,
        termRelations: TermRelationsUnionTypeDef = ...,
    ) -> CreateGlossaryTermOutputTypeDef:
        """
        Creates a business glossary term.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_glossary_term)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_glossary_term)
        """

    async def create_group_profile(
        self, *, domainIdentifier: str, groupIdentifier: str, clientToken: str = ...
    ) -> CreateGroupProfileOutputTypeDef:
        """
        Creates a group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_group_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_group_profile)
        """

    async def create_listing_change_set(
        self,
        *,
        action: ChangeActionType,
        domainIdentifier: str,
        entityIdentifier: str,
        entityType: EntityTypeType,
        clientToken: str = ...,
        entityRevision: str = ...,
    ) -> CreateListingChangeSetOutputTypeDef:
        """
        Publishes a listing (a record of an asset at a given time) or removes a listing
        from the
        catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_listing_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_listing_change_set)
        """

    async def create_project(
        self,
        *,
        domainIdentifier: str,
        name: str,
        description: str = ...,
        glossaryTerms: Sequence[str] = ...,
    ) -> CreateProjectOutputTypeDef:
        """
        Creates an Amazon DataZone project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_project)
        """

    async def create_project_membership(
        self,
        *,
        designation: UserDesignationType,
        domainIdentifier: str,
        member: MemberTypeDef,
        projectIdentifier: str,
    ) -> Dict[str, Any]:
        """
        Creates a project membership in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_project_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_project_membership)
        """

    async def create_subscription_grant(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        grantedEntity: GrantedEntityInputTypeDef,
        subscriptionTargetIdentifier: str,
        assetTargetNames: Sequence[AssetTargetNameMapTypeDef] = ...,
        clientToken: str = ...,
    ) -> CreateSubscriptionGrantOutputTypeDef:
        """
        Creates a subsscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_subscription_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_subscription_grant)
        """

    async def create_subscription_request(
        self,
        *,
        domainIdentifier: str,
        requestReason: str,
        subscribedListings: Sequence[SubscribedListingInputTypeDef],
        subscribedPrincipals: Sequence[SubscribedPrincipalInputTypeDef],
        clientToken: str = ...,
    ) -> CreateSubscriptionRequestOutputTypeDef:
        """
        Creates a subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_subscription_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_subscription_request)
        """

    async def create_subscription_target(
        self,
        *,
        applicableAssetTypes: Sequence[str],
        authorizedPrincipals: Sequence[str],
        domainIdentifier: str,
        environmentIdentifier: str,
        manageAccessRole: str,
        name: str,
        subscriptionTargetConfig: Sequence[SubscriptionTargetFormTypeDef],
        type: str,
        clientToken: str = ...,
        provider: str = ...,
    ) -> CreateSubscriptionTargetOutputTypeDef:
        """
        Creates a subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_subscription_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_subscription_target)
        """

    async def create_user_profile(
        self,
        *,
        domainIdentifier: str,
        userIdentifier: str,
        clientToken: str = ...,
        userType: UserTypeType = ...,
    ) -> CreateUserProfileOutputTypeDef:
        """
        Creates a user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.create_user_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#create_user_profile)
        """

    async def delete_asset(self, *, domainIdentifier: str, identifier: str) -> Dict[str, Any]:
        """
        Deletes an asset in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_asset)
        """

    async def delete_asset_filter(
        self, *, assetIdentifier: str, domainIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_asset_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_asset_filter)
        """

    async def delete_asset_type(self, *, domainIdentifier: str, identifier: str) -> Dict[str, Any]:
        """
        Deletes an asset type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_asset_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_asset_type)
        """

    async def delete_data_product(
        self, *, domainIdentifier: str, identifier: str
    ) -> Dict[str, Any]:
        """
        Deletes an data product in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_data_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_data_product)
        """

    async def delete_data_source(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        clientToken: str = ...,
        retainPermissionsOnRevokeFailure: bool = ...,
    ) -> DeleteDataSourceOutputTypeDef:
        """
        Deletes a data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_data_source)
        """

    async def delete_domain(
        self, *, identifier: str, clientToken: str = ..., skipDeletionCheck: bool = ...
    ) -> DeleteDomainOutputTypeDef:
        """
        Deletes a Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_domain)
        """

    async def delete_environment(
        self, *, domainIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_environment)
        """

    async def delete_environment_action(
        self, *, domainIdentifier: str, environmentIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an action for the environment, for example, deletes a console link for
        an analytics tool that is available in this
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_environment_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_environment_action)
        """

    async def delete_environment_blueprint_configuration(
        self, *, domainIdentifier: str, environmentBlueprintIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes the blueprint configuration in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_environment_blueprint_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_environment_blueprint_configuration)
        """

    async def delete_environment_profile(
        self, *, domainIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_environment_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_environment_profile)
        """

    async def delete_form_type(
        self, *, domainIdentifier: str, formTypeIdentifier: str
    ) -> Dict[str, Any]:
        """
        Delets and metadata form type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_form_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_form_type)
        """

    async def delete_glossary(self, *, domainIdentifier: str, identifier: str) -> Dict[str, Any]:
        """
        Deletes a business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_glossary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_glossary)
        """

    async def delete_glossary_term(
        self, *, domainIdentifier: str, identifier: str
    ) -> Dict[str, Any]:
        """
        Deletes a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_glossary_term)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_glossary_term)
        """

    async def delete_listing(self, *, domainIdentifier: str, identifier: str) -> Dict[str, Any]:
        """
        Deletes a listing (a record of an asset at a given time).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_listing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_listing)
        """

    async def delete_project(
        self, *, domainIdentifier: str, identifier: str, skipDeletionCheck: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes a project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_project)
        """

    async def delete_project_membership(
        self, *, domainIdentifier: str, member: MemberTypeDef, projectIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes project membership in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_project_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_project_membership)
        """

    async def delete_subscription_grant(
        self, *, domainIdentifier: str, identifier: str
    ) -> DeleteSubscriptionGrantOutputTypeDef:
        """
        Deletes and subscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_subscription_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_subscription_grant)
        """

    async def delete_subscription_request(
        self, *, domainIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_subscription_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_subscription_request)
        """

    async def delete_subscription_target(
        self, *, domainIdentifier: str, environmentIdentifier: str, identifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_subscription_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_subscription_target)
        """

    async def delete_time_series_data_points(
        self,
        *,
        domainIdentifier: str,
        entityIdentifier: str,
        entityType: TimeSeriesEntityTypeType,
        formName: str,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Deletes the specified time series form for the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.delete_time_series_data_points)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#delete_time_series_data_points)
        """

    async def disassociate_environment_role(
        self, *, domainIdentifier: str, environmentIdentifier: str, environmentRoleArn: str
    ) -> Dict[str, Any]:
        """
        Disassociates the environment role in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.disassociate_environment_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#disassociate_environment_role)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#generate_presigned_url)
        """

    async def get_asset(
        self, *, domainIdentifier: str, identifier: str, revision: str = ...
    ) -> GetAssetOutputTypeDef:
        """
        Gets an Amazon DataZone asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_asset)
        """

    async def get_asset_filter(
        self, *, assetIdentifier: str, domainIdentifier: str, identifier: str
    ) -> GetAssetFilterOutputTypeDef:
        """
        Gets an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_asset_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_asset_filter)
        """

    async def get_asset_type(
        self, *, domainIdentifier: str, identifier: str, revision: str = ...
    ) -> GetAssetTypeOutputTypeDef:
        """
        Gets an Amazon DataZone asset type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_asset_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_asset_type)
        """

    async def get_data_product(
        self, *, domainIdentifier: str, identifier: str, revision: str = ...
    ) -> GetDataProductOutputTypeDef:
        """
        Gets the data product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_data_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_data_product)
        """

    async def get_data_source(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetDataSourceOutputTypeDef:
        """
        Gets an Amazon DataZone data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_data_source)
        """

    async def get_data_source_run(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetDataSourceRunOutputTypeDef:
        """
        Gets an Amazon DataZone data source run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_data_source_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_data_source_run)
        """

    async def get_domain(self, *, identifier: str) -> GetDomainOutputTypeDef:
        """
        Gets an Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_domain)
        """

    async def get_environment(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetEnvironmentOutputTypeDef:
        """
        Gets an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment)
        """

    async def get_environment_action(
        self, *, domainIdentifier: str, environmentIdentifier: str, identifier: str
    ) -> GetEnvironmentActionOutputTypeDef:
        """
        Gets the specified environment action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment_action)
        """

    async def get_environment_blueprint(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetEnvironmentBlueprintOutputTypeDef:
        """
        Gets an Amazon DataZone blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment_blueprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment_blueprint)
        """

    async def get_environment_blueprint_configuration(
        self, *, domainIdentifier: str, environmentBlueprintIdentifier: str
    ) -> GetEnvironmentBlueprintConfigurationOutputTypeDef:
        """
        Gets the blueprint configuration in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment_blueprint_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment_blueprint_configuration)
        """

    async def get_environment_credentials(
        self, *, domainIdentifier: str, environmentIdentifier: str
    ) -> GetEnvironmentCredentialsOutputTypeDef:
        """
        Gets the credentials of an environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment_credentials)
        """

    async def get_environment_profile(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetEnvironmentProfileOutputTypeDef:
        """
        Gets an evinronment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_environment_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_environment_profile)
        """

    async def get_form_type(
        self, *, domainIdentifier: str, formTypeIdentifier: str, revision: str = ...
    ) -> GetFormTypeOutputTypeDef:
        """
        Gets a metadata form type in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_form_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_form_type)
        """

    async def get_glossary(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetGlossaryOutputTypeDef:
        """
        Gets a business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_glossary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_glossary)
        """

    async def get_glossary_term(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetGlossaryTermOutputTypeDef:
        """
        Gets a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_glossary_term)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_glossary_term)
        """

    async def get_group_profile(
        self, *, domainIdentifier: str, groupIdentifier: str
    ) -> GetGroupProfileOutputTypeDef:
        """
        Gets a group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_group_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_group_profile)
        """

    async def get_iam_portal_login_url(
        self, *, domainIdentifier: str
    ) -> GetIamPortalLoginUrlOutputTypeDef:
        """
        Gets the data portal URL for the specified Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_iam_portal_login_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_iam_portal_login_url)
        """

    async def get_lineage_node(
        self, *, domainIdentifier: str, identifier: str, eventTimestamp: TimestampTypeDef = ...
    ) -> GetLineageNodeOutputTypeDef:
        """
        Gets the data lineage node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_lineage_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_lineage_node)
        """

    async def get_listing(
        self, *, domainIdentifier: str, identifier: str, listingRevision: str = ...
    ) -> GetListingOutputTypeDef:
        """
        Gets a listing (a record of an asset at a given time).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_listing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_listing)
        """

    async def get_metadata_generation_run(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetMetadataGenerationRunOutputTypeDef:
        """
        Gets a metadata generation run in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_metadata_generation_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_metadata_generation_run)
        """

    async def get_project(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetProjectOutputTypeDef:
        """
        Gets a project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_project)
        """

    async def get_subscription(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetSubscriptionOutputTypeDef:
        """
        Gets a subscription in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_subscription)
        """

    async def get_subscription_grant(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetSubscriptionGrantOutputTypeDef:
        """
        Gets the subscription grant in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_subscription_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_subscription_grant)
        """

    async def get_subscription_request_details(
        self, *, domainIdentifier: str, identifier: str
    ) -> GetSubscriptionRequestDetailsOutputTypeDef:
        """
        Gets the details of the specified subscription request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_subscription_request_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_subscription_request_details)
        """

    async def get_subscription_target(
        self, *, domainIdentifier: str, environmentIdentifier: str, identifier: str
    ) -> GetSubscriptionTargetOutputTypeDef:
        """
        Gets the subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_subscription_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_subscription_target)
        """

    async def get_time_series_data_point(
        self,
        *,
        domainIdentifier: str,
        entityIdentifier: str,
        entityType: TimeSeriesEntityTypeType,
        formName: str,
        identifier: str,
    ) -> GetTimeSeriesDataPointOutputTypeDef:
        """
        Gets the existing data point for the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_time_series_data_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_time_series_data_point)
        """

    async def get_user_profile(
        self, *, domainIdentifier: str, userIdentifier: str, type: UserProfileTypeType = ...
    ) -> GetUserProfileOutputTypeDef:
        """
        Gets a user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_user_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_user_profile)
        """

    async def list_asset_filters(
        self,
        *,
        assetIdentifier: str,
        domainIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: FilterStatusType = ...,
    ) -> ListAssetFiltersOutputTypeDef:
        """
        Lists asset filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_asset_filters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_asset_filters)
        """

    async def list_asset_revisions(
        self, *, domainIdentifier: str, identifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAssetRevisionsOutputTypeDef:
        """
        Lists the revisions for the asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_asset_revisions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_asset_revisions)
        """

    async def list_data_product_revisions(
        self, *, domainIdentifier: str, identifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListDataProductRevisionsOutputTypeDef:
        """
        Lists data product revisions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_data_product_revisions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_data_product_revisions)
        """

    async def list_data_source_run_activities(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: DataAssetActivityStatusType = ...,
    ) -> ListDataSourceRunActivitiesOutputTypeDef:
        """
        Lists data source run activities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_data_source_run_activities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_data_source_run_activities)
        """

    async def list_data_source_runs(
        self,
        *,
        dataSourceIdentifier: str,
        domainIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: DataSourceRunStatusType = ...,
    ) -> ListDataSourceRunsOutputTypeDef:
        """
        Lists data source runs in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_data_source_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_data_source_runs)
        """

    async def list_data_sources(
        self,
        *,
        domainIdentifier: str,
        projectIdentifier: str,
        environmentIdentifier: str = ...,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
        status: DataSourceStatusType = ...,
        type: str = ...,
    ) -> ListDataSourcesOutputTypeDef:
        """
        Lists data sources in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_data_sources)
        """

    async def list_domains(
        self, *, maxResults: int = ..., nextToken: str = ..., status: DomainStatusType = ...
    ) -> ListDomainsOutputTypeDef:
        """
        Lists Amazon DataZone domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_domains)
        """

    async def list_environment_actions(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListEnvironmentActionsOutputTypeDef:
        """
        Lists existing environment actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_environment_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_environment_actions)
        """

    async def list_environment_blueprint_configurations(
        self, *, domainIdentifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListEnvironmentBlueprintConfigurationsOutputTypeDef:
        """
        Lists blueprint configurations for a Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_environment_blueprint_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_environment_blueprint_configurations)
        """

    async def list_environment_blueprints(
        self,
        *,
        domainIdentifier: str,
        managed: bool = ...,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
    ) -> ListEnvironmentBlueprintsOutputTypeDef:
        """
        Lists blueprints in an Amazon DataZone environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_environment_blueprints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_environment_blueprints)
        """

    async def list_environment_profiles(
        self,
        *,
        domainIdentifier: str,
        awsAccountId: str = ...,
        awsAccountRegion: str = ...,
        environmentBlueprintIdentifier: str = ...,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
        projectIdentifier: str = ...,
    ) -> ListEnvironmentProfilesOutputTypeDef:
        """
        Lists Amazon DataZone environment profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_environment_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_environment_profiles)
        """

    async def list_environments(
        self,
        *,
        domainIdentifier: str,
        projectIdentifier: str,
        awsAccountId: str = ...,
        awsAccountRegion: str = ...,
        environmentBlueprintIdentifier: str = ...,
        environmentProfileIdentifier: str = ...,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
        provider: str = ...,
        status: EnvironmentStatusType = ...,
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists Amazon DataZone environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_environments)
        """

    async def list_lineage_node_history(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        direction: EdgeDirectionType = ...,
        eventTimestampGTE: TimestampTypeDef = ...,
        eventTimestampLTE: TimestampTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortOrder: SortOrderType = ...,
    ) -> ListLineageNodeHistoryOutputTypeDef:
        """
        Lists the history of the specified data lineage node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_lineage_node_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_lineage_node_history)
        """

    async def list_metadata_generation_runs(
        self,
        *,
        domainIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: MetadataGenerationRunStatusType = ...,
        type: Literal["BUSINESS_DESCRIPTIONS"] = ...,
    ) -> ListMetadataGenerationRunsOutputTypeDef:
        """
        Lists all metadata generation runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_metadata_generation_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_metadata_generation_runs)
        """

    async def list_notifications(
        self,
        *,
        domainIdentifier: str,
        type: NotificationTypeType,
        afterTimestamp: TimestampTypeDef = ...,
        beforeTimestamp: TimestampTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        subjects: Sequence[str] = ...,
        taskStatus: TaskStatusType = ...,
    ) -> ListNotificationsOutputTypeDef:
        """
        Lists all Amazon DataZone notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_notifications)
        """

    async def list_project_memberships(
        self,
        *,
        domainIdentifier: str,
        projectIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: Literal["NAME"] = ...,
        sortOrder: SortOrderType = ...,
    ) -> ListProjectMembershipsOutputTypeDef:
        """
        Lists all members of the specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_project_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_project_memberships)
        """

    async def list_projects(
        self,
        *,
        domainIdentifier: str,
        groupIdentifier: str = ...,
        maxResults: int = ...,
        name: str = ...,
        nextToken: str = ...,
        userIdentifier: str = ...,
    ) -> ListProjectsOutputTypeDef:
        """
        Lists Amazon DataZone projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_projects)
        """

    async def list_subscription_grants(
        self,
        *,
        domainIdentifier: str,
        environmentId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        owningProjectId: str = ...,
        sortBy: SortKeyType = ...,
        sortOrder: SortOrderType = ...,
        subscribedListingId: str = ...,
        subscriptionId: str = ...,
        subscriptionTargetId: str = ...,
    ) -> ListSubscriptionGrantsOutputTypeDef:
        """
        Lists subscription grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_subscription_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_subscription_grants)
        """

    async def list_subscription_requests(
        self,
        *,
        domainIdentifier: str,
        approverProjectId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        owningProjectId: str = ...,
        sortBy: SortKeyType = ...,
        sortOrder: SortOrderType = ...,
        status: SubscriptionRequestStatusType = ...,
        subscribedListingId: str = ...,
    ) -> ListSubscriptionRequestsOutputTypeDef:
        """
        Lists Amazon DataZone subscription requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_subscription_requests)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_subscription_requests)
        """

    async def list_subscription_targets(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: SortKeyType = ...,
        sortOrder: SortOrderType = ...,
    ) -> ListSubscriptionTargetsOutputTypeDef:
        """
        Lists subscription targets in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_subscription_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_subscription_targets)
        """

    async def list_subscriptions(
        self,
        *,
        domainIdentifier: str,
        approverProjectId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        owningProjectId: str = ...,
        sortBy: SortKeyType = ...,
        sortOrder: SortOrderType = ...,
        status: SubscriptionStatusType = ...,
        subscribedListingId: str = ...,
        subscriptionRequestIdentifier: str = ...,
    ) -> ListSubscriptionsOutputTypeDef:
        """
        Lists subscriptions in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_subscriptions)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for the specified resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_tags_for_resource)
        """

    async def list_time_series_data_points(
        self,
        *,
        domainIdentifier: str,
        entityIdentifier: str,
        entityType: TimeSeriesEntityTypeType,
        formName: str,
        endedAt: TimestampTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        startedAt: TimestampTypeDef = ...,
    ) -> ListTimeSeriesDataPointsOutputTypeDef:
        """
        Lists time series data points.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.list_time_series_data_points)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#list_time_series_data_points)
        """

    async def post_lineage_event(
        self, *, domainIdentifier: str, event: BlobTypeDef, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Posts a data lineage event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.post_lineage_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#post_lineage_event)
        """

    async def post_time_series_data_points(
        self,
        *,
        domainIdentifier: str,
        entityIdentifier: str,
        entityType: TimeSeriesEntityTypeType,
        forms: Sequence[TimeSeriesDataPointFormInputTypeDef],
        clientToken: str = ...,
    ) -> PostTimeSeriesDataPointsOutputTypeDef:
        """
        Posts time series data points to Amazon DataZone for the specified asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.post_time_series_data_points)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#post_time_series_data_points)
        """

    async def put_environment_blueprint_configuration(
        self,
        *,
        domainIdentifier: str,
        enabledRegions: Sequence[str],
        environmentBlueprintIdentifier: str,
        manageAccessRoleArn: str = ...,
        provisioningConfigurations: Sequence[ProvisioningConfigurationUnionTypeDef] = ...,
        provisioningRoleArn: str = ...,
        regionalParameters: Mapping[str, Mapping[str, str]] = ...,
    ) -> PutEnvironmentBlueprintConfigurationOutputTypeDef:
        """
        Writes the configuration for the specified environment blueprint in Amazon
        DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.put_environment_blueprint_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#put_environment_blueprint_configuration)
        """

    async def reject_predictions(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        clientToken: str = ...,
        rejectChoices: Sequence[RejectChoiceTypeDef] = ...,
        rejectRule: RejectRuleTypeDef = ...,
        revision: str = ...,
    ) -> RejectPredictionsOutputTypeDef:
        """
        Rejects automatically generated business-friendly metadata for your Amazon
        DataZone
        assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.reject_predictions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#reject_predictions)
        """

    async def reject_subscription_request(
        self, *, domainIdentifier: str, identifier: str, decisionComment: str = ...
    ) -> RejectSubscriptionRequestOutputTypeDef:
        """
        Rejects the specified subscription request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.reject_subscription_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#reject_subscription_request)
        """

    async def revoke_subscription(
        self, *, domainIdentifier: str, identifier: str, retainPermissions: bool = ...
    ) -> RevokeSubscriptionOutputTypeDef:
        """
        Revokes a specified subscription in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.revoke_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#revoke_subscription)
        """

    async def search(
        self,
        *,
        domainIdentifier: str,
        searchScope: InventorySearchScopeType,
        additionalAttributes: Sequence[SearchOutputAdditionalAttributeType] = ...,
        filters: "FilterClauseTypeDef" = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        owningProjectIdentifier: str = ...,
        searchIn: Sequence[SearchInItemTypeDef] = ...,
        searchText: str = ...,
        sort: SearchSortTypeDef = ...,
    ) -> SearchOutputTypeDef:
        """
        Searches for assets in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.search)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#search)
        """

    async def search_group_profiles(
        self,
        *,
        domainIdentifier: str,
        groupType: GroupSearchTypeType,
        maxResults: int = ...,
        nextToken: str = ...,
        searchText: str = ...,
    ) -> SearchGroupProfilesOutputTypeDef:
        """
        Searches group profiles in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.search_group_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#search_group_profiles)
        """

    async def search_listings(
        self,
        *,
        domainIdentifier: str,
        additionalAttributes: Sequence[SearchOutputAdditionalAttributeType] = ...,
        filters: "FilterClauseTypeDef" = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        searchIn: Sequence[SearchInItemTypeDef] = ...,
        searchText: str = ...,
        sort: SearchSortTypeDef = ...,
    ) -> SearchListingsOutputTypeDef:
        """
        Searches listings (records of an asset at a given time) in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.search_listings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#search_listings)
        """

    async def search_types(
        self,
        *,
        domainIdentifier: str,
        managed: bool,
        searchScope: TypesSearchScopeType,
        filters: "FilterClauseTypeDef" = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        searchIn: Sequence[SearchInItemTypeDef] = ...,
        searchText: str = ...,
        sort: SearchSortTypeDef = ...,
    ) -> SearchTypesOutputTypeDef:
        """
        Searches for types in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.search_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#search_types)
        """

    async def search_user_profiles(
        self,
        *,
        domainIdentifier: str,
        userType: UserSearchTypeType,
        maxResults: int = ...,
        nextToken: str = ...,
        searchText: str = ...,
    ) -> SearchUserProfilesOutputTypeDef:
        """
        Searches user profiles in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.search_user_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#search_user_profiles)
        """

    async def start_data_source_run(
        self, *, dataSourceIdentifier: str, domainIdentifier: str, clientToken: str = ...
    ) -> StartDataSourceRunOutputTypeDef:
        """
        Start the run of the specified data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.start_data_source_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#start_data_source_run)
        """

    async def start_metadata_generation_run(
        self,
        *,
        domainIdentifier: str,
        owningProjectIdentifier: str,
        target: MetadataGenerationRunTargetTypeDef,
        type: Literal["BUSINESS_DESCRIPTIONS"],
        clientToken: str = ...,
    ) -> StartMetadataGenerationRunOutputTypeDef:
        """
        Starts the metadata generation run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.start_metadata_generation_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#start_metadata_generation_run)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags a resource in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#untag_resource)
        """

    async def update_asset_filter(
        self,
        *,
        assetIdentifier: str,
        domainIdentifier: str,
        identifier: str,
        configuration: AssetFilterConfigurationUnionTypeDef = ...,
        description: str = ...,
        name: str = ...,
    ) -> UpdateAssetFilterOutputTypeDef:
        """
        Updates an asset filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_asset_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_asset_filter)
        """

    async def update_data_source(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        assetFormsInput: Sequence[FormInputTypeDef] = ...,
        configuration: DataSourceConfigurationInputTypeDef = ...,
        description: str = ...,
        enableSetting: EnableSettingType = ...,
        name: str = ...,
        publishOnImport: bool = ...,
        recommendation: RecommendationConfigurationTypeDef = ...,
        retainPermissionsOnRevokeFailure: bool = ...,
        schedule: ScheduleConfigurationTypeDef = ...,
    ) -> UpdateDataSourceOutputTypeDef:
        """
        Updates the specified data source in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_data_source)
        """

    async def update_domain(
        self,
        *,
        identifier: str,
        clientToken: str = ...,
        description: str = ...,
        domainExecutionRole: str = ...,
        name: str = ...,
        singleSignOn: SingleSignOnTypeDef = ...,
    ) -> UpdateDomainOutputTypeDef:
        """
        Updates a Amazon DataZone domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_domain)
        """

    async def update_environment(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        description: str = ...,
        glossaryTerms: Sequence[str] = ...,
        name: str = ...,
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates the specified environment in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_environment)
        """

    async def update_environment_action(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        identifier: str,
        description: str = ...,
        name: str = ...,
        parameters: ActionParametersTypeDef = ...,
    ) -> UpdateEnvironmentActionOutputTypeDef:
        """
        Updates an environment action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_environment_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_environment_action)
        """

    async def update_environment_profile(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        awsAccountId: str = ...,
        awsAccountRegion: str = ...,
        description: str = ...,
        name: str = ...,
        userParameters: Sequence[EnvironmentParameterTypeDef] = ...,
    ) -> UpdateEnvironmentProfileOutputTypeDef:
        """
        Updates the specified environment profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_environment_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_environment_profile)
        """

    async def update_glossary(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        clientToken: str = ...,
        description: str = ...,
        name: str = ...,
        status: GlossaryStatusType = ...,
    ) -> UpdateGlossaryOutputTypeDef:
        """
        Updates the business glossary in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_glossary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_glossary)
        """

    async def update_glossary_term(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        glossaryIdentifier: str = ...,
        longDescription: str = ...,
        name: str = ...,
        shortDescription: str = ...,
        status: GlossaryTermStatusType = ...,
        termRelations: TermRelationsUnionTypeDef = ...,
    ) -> UpdateGlossaryTermOutputTypeDef:
        """
        Updates a business glossary term in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_glossary_term)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_glossary_term)
        """

    async def update_group_profile(
        self, *, domainIdentifier: str, groupIdentifier: str, status: GroupProfileStatusType
    ) -> UpdateGroupProfileOutputTypeDef:
        """
        Updates the specified group profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_group_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_group_profile)
        """

    async def update_project(
        self,
        *,
        domainIdentifier: str,
        identifier: str,
        description: str = ...,
        glossaryTerms: Sequence[str] = ...,
        name: str = ...,
    ) -> UpdateProjectOutputTypeDef:
        """
        Updates the specified project in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_project)
        """

    async def update_subscription_grant_status(
        self,
        *,
        assetIdentifier: str,
        domainIdentifier: str,
        identifier: str,
        status: SubscriptionGrantStatusType,
        failureCause: FailureCauseTypeDef = ...,
        targetName: str = ...,
    ) -> UpdateSubscriptionGrantStatusOutputTypeDef:
        """
        Updates the status of the specified subscription grant status in Amazon
        DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_subscription_grant_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_subscription_grant_status)
        """

    async def update_subscription_request(
        self, *, domainIdentifier: str, identifier: str, requestReason: str
    ) -> UpdateSubscriptionRequestOutputTypeDef:
        """
        Updates a specified subscription request in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_subscription_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_subscription_request)
        """

    async def update_subscription_target(
        self,
        *,
        domainIdentifier: str,
        environmentIdentifier: str,
        identifier: str,
        applicableAssetTypes: Sequence[str] = ...,
        authorizedPrincipals: Sequence[str] = ...,
        manageAccessRole: str = ...,
        name: str = ...,
        provider: str = ...,
        subscriptionTargetConfig: Sequence[SubscriptionTargetFormTypeDef] = ...,
    ) -> UpdateSubscriptionTargetOutputTypeDef:
        """
        Updates the specified subscription target in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_subscription_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_subscription_target)
        """

    async def update_user_profile(
        self,
        *,
        domainIdentifier: str,
        status: UserProfileStatusType,
        userIdentifier: str,
        type: UserProfileTypeType = ...,
    ) -> UpdateUserProfileOutputTypeDef:
        """
        Updates the specified user profile in Amazon DataZone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.update_user_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#update_user_profile)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_filters"]
    ) -> ListAssetFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_revisions"]
    ) -> ListAssetRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_product_revisions"]
    ) -> ListDataProductRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_run_activities"]
    ) -> ListDataSourceRunActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_runs"]
    ) -> ListDataSourceRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_actions"]
    ) -> ListEnvironmentActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_blueprint_configurations"]
    ) -> ListEnvironmentBlueprintConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_blueprints"]
    ) -> ListEnvironmentBlueprintsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_profiles"]
    ) -> ListEnvironmentProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_lineage_node_history"]
    ) -> ListLineageNodeHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metadata_generation_runs"]
    ) -> ListMetadataGenerationRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notifications"]
    ) -> ListNotificationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_project_memberships"]
    ) -> ListProjectMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_grants"]
    ) -> ListSubscriptionGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_requests"]
    ) -> ListSubscriptionRequestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscription_targets"]
    ) -> ListSubscriptionTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscriptions"]
    ) -> ListSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_time_series_data_points"]
    ) -> ListTimeSeriesDataPointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search"]) -> SearchPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_group_profiles"]
    ) -> SearchGroupProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_listings"]) -> SearchListingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_types"]) -> SearchTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_user_profiles"]
    ) -> SearchUserProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/#get_paginator)
        """

    async def __aenter__(self) -> "DataZoneClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone.html#DataZone.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/client/)
        """
