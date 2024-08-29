"""
Type annotations for wellarchitected service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_wellarchitected.client import WellArchitectedClient

    session = get_session()
    async with session.create_client("wellarchitected") as client:
        client: WellArchitectedClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AnswerReasonType,
    DiscoveryIntegrationStatusType,
    LensStatusTypeType,
    LensTypeType,
    OrganizationSharingStatusType,
    PermissionTypeType,
    ProfileOwnerTypeType,
    QuestionPriorityType,
    ReportFormatType,
    ShareInvitationActionType,
    ShareResourceTypeType,
    ShareStatusType,
    WorkloadEnvironmentType,
    WorkloadImprovementStatusType,
)
from .type_defs import (
    AccountJiraConfigurationInputTypeDef,
    ChoiceUpdateTypeDef,
    CreateLensShareOutputTypeDef,
    CreateLensVersionOutputTypeDef,
    CreateMilestoneOutputTypeDef,
    CreateProfileOutputTypeDef,
    CreateProfileShareOutputTypeDef,
    CreateReviewTemplateOutputTypeDef,
    CreateTemplateShareOutputTypeDef,
    CreateWorkloadOutputTypeDef,
    CreateWorkloadShareOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportLensOutputTypeDef,
    GetAnswerOutputTypeDef,
    GetConsolidatedReportOutputTypeDef,
    GetGlobalSettingsOutputTypeDef,
    GetLensOutputTypeDef,
    GetLensReviewOutputTypeDef,
    GetLensReviewReportOutputTypeDef,
    GetLensVersionDifferenceOutputTypeDef,
    GetMilestoneOutputTypeDef,
    GetProfileOutputTypeDef,
    GetProfileTemplateOutputTypeDef,
    GetReviewTemplateAnswerOutputTypeDef,
    GetReviewTemplateLensReviewOutputTypeDef,
    GetReviewTemplateOutputTypeDef,
    GetWorkloadOutputTypeDef,
    ImportLensOutputTypeDef,
    JiraSelectedQuestionConfigurationUnionTypeDef,
    ListAnswersOutputTypeDef,
    ListCheckDetailsOutputTypeDef,
    ListCheckSummariesOutputTypeDef,
    ListLensesOutputTypeDef,
    ListLensReviewImprovementsOutputTypeDef,
    ListLensReviewsOutputTypeDef,
    ListLensSharesOutputTypeDef,
    ListMilestonesOutputTypeDef,
    ListNotificationsOutputTypeDef,
    ListProfileNotificationsOutputTypeDef,
    ListProfileSharesOutputTypeDef,
    ListProfilesOutputTypeDef,
    ListReviewTemplateAnswersOutputTypeDef,
    ListReviewTemplatesOutputTypeDef,
    ListShareInvitationsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTemplateSharesOutputTypeDef,
    ListWorkloadSharesOutputTypeDef,
    ListWorkloadsOutputTypeDef,
    ProfileQuestionUpdateTypeDef,
    UpdateAnswerOutputTypeDef,
    UpdateLensReviewOutputTypeDef,
    UpdateProfileOutputTypeDef,
    UpdateReviewTemplateAnswerOutputTypeDef,
    UpdateReviewTemplateLensReviewOutputTypeDef,
    UpdateReviewTemplateOutputTypeDef,
    UpdateShareInvitationOutputTypeDef,
    UpdateWorkloadOutputTypeDef,
    UpdateWorkloadShareOutputTypeDef,
    WorkloadDiscoveryConfigUnionTypeDef,
    WorkloadJiraConfigurationInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("WellArchitectedClient",)


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
    ValidationException: Type[BotocoreClientError]


class WellArchitectedClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WellArchitectedClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#exceptions)
        """

    async def associate_lenses(
        self, *, WorkloadId: str, LensAliases: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a lens to a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.associate_lenses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#associate_lenses)
        """

    async def associate_profiles(
        self, *, WorkloadId: str, ProfileArns: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a profile with a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.associate_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#associate_profiles)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#close)
        """

    async def create_lens_share(
        self, *, LensAlias: str, SharedWith: str, ClientRequestToken: str
    ) -> CreateLensShareOutputTypeDef:
        """
        Create a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_lens_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_lens_share)
        """

    async def create_lens_version(
        self,
        *,
        LensAlias: str,
        LensVersion: str,
        ClientRequestToken: str,
        IsMajorVersion: bool = ...,
    ) -> CreateLensVersionOutputTypeDef:
        """
        Create a new lens version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_lens_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_lens_version)
        """

    async def create_milestone(
        self, *, WorkloadId: str, MilestoneName: str, ClientRequestToken: str
    ) -> CreateMilestoneOutputTypeDef:
        """
        Create a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_milestone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_milestone)
        """

    async def create_profile(
        self,
        *,
        ProfileName: str,
        ProfileDescription: str,
        ProfileQuestions: Sequence[ProfileQuestionUpdateTypeDef],
        ClientRequestToken: str,
        Tags: Mapping[str, str] = ...,
    ) -> CreateProfileOutputTypeDef:
        """
        Create a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_profile)
        """

    async def create_profile_share(
        self, *, ProfileArn: str, SharedWith: str, ClientRequestToken: str
    ) -> CreateProfileShareOutputTypeDef:
        """
        Create a profile share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_profile_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_profile_share)
        """

    async def create_review_template(
        self,
        *,
        TemplateName: str,
        Description: str,
        Lenses: Sequence[str],
        ClientRequestToken: str,
        Notes: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateReviewTemplateOutputTypeDef:
        """
        Create a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_review_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_review_template)
        """

    async def create_template_share(
        self, *, TemplateArn: str, SharedWith: str, ClientRequestToken: str
    ) -> CreateTemplateShareOutputTypeDef:
        """
        Create a review template share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_template_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_template_share)
        """

    async def create_workload(
        self,
        *,
        WorkloadName: str,
        Description: str,
        Environment: WorkloadEnvironmentType,
        Lenses: Sequence[str],
        ClientRequestToken: str,
        AccountIds: Sequence[str] = ...,
        AwsRegions: Sequence[str] = ...,
        NonAwsRegions: Sequence[str] = ...,
        PillarPriorities: Sequence[str] = ...,
        ArchitecturalDesign: str = ...,
        ReviewOwner: str = ...,
        IndustryType: str = ...,
        Industry: str = ...,
        Notes: str = ...,
        Tags: Mapping[str, str] = ...,
        DiscoveryConfig: WorkloadDiscoveryConfigUnionTypeDef = ...,
        Applications: Sequence[str] = ...,
        ProfileArns: Sequence[str] = ...,
        ReviewTemplateArns: Sequence[str] = ...,
        JiraConfiguration: WorkloadJiraConfigurationInputTypeDef = ...,
    ) -> CreateWorkloadOutputTypeDef:
        """
        Create a new workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_workload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_workload)
        """

    async def create_workload_share(
        self,
        *,
        WorkloadId: str,
        SharedWith: str,
        PermissionType: PermissionTypeType,
        ClientRequestToken: str,
    ) -> CreateWorkloadShareOutputTypeDef:
        """
        Create a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.create_workload_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_workload_share)
        """

    async def delete_lens(
        self, *, LensAlias: str, ClientRequestToken: str, LensStatus: LensStatusTypeType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_lens)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_lens)
        """

    async def delete_lens_share(
        self, *, ShareId: str, LensAlias: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_lens_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_lens_share)
        """

    async def delete_profile(
        self, *, ProfileArn: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_profile)
        """

    async def delete_profile_share(
        self, *, ShareId: str, ProfileArn: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a profile share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_profile_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_profile_share)
        """

    async def delete_review_template(
        self, *, TemplateArn: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_review_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_review_template)
        """

    async def delete_template_share(
        self, *, ShareId: str, TemplateArn: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a review template share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_template_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_template_share)
        """

    async def delete_workload(
        self, *, WorkloadId: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_workload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_workload)
        """

    async def delete_workload_share(
        self, *, ShareId: str, WorkloadId: str, ClientRequestToken: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.delete_workload_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_workload_share)
        """

    async def disassociate_lenses(
        self, *, WorkloadId: str, LensAliases: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate a lens from a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.disassociate_lenses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#disassociate_lenses)
        """

    async def disassociate_profiles(
        self, *, WorkloadId: str, ProfileArns: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate a profile from a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.disassociate_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#disassociate_profiles)
        """

    async def export_lens(
        self, *, LensAlias: str, LensVersion: str = ...
    ) -> ExportLensOutputTypeDef:
        """
        Export an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.export_lens)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#export_lens)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#generate_presigned_url)
        """

    async def get_answer(
        self, *, WorkloadId: str, LensAlias: str, QuestionId: str, MilestoneNumber: int = ...
    ) -> GetAnswerOutputTypeDef:
        """
        Get the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_answer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_answer)
        """

    async def get_consolidated_report(
        self,
        *,
        Format: ReportFormatType,
        IncludeSharedResources: bool = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> GetConsolidatedReportOutputTypeDef:
        """
        Get a consolidated report of your workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_consolidated_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_consolidated_report)
        """

    async def get_global_settings(self) -> GetGlobalSettingsOutputTypeDef:
        """
        Global settings for all workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_global_settings)
        """

    async def get_lens(self, *, LensAlias: str, LensVersion: str = ...) -> GetLensOutputTypeDef:
        """
        Get an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens)
        """

    async def get_lens_review(
        self, *, WorkloadId: str, LensAlias: str, MilestoneNumber: int = ...
    ) -> GetLensReviewOutputTypeDef:
        """
        Get lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_review)
        """

    async def get_lens_review_report(
        self, *, WorkloadId: str, LensAlias: str, MilestoneNumber: int = ...
    ) -> GetLensReviewReportOutputTypeDef:
        """
        Get lens review report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_review_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_review_report)
        """

    async def get_lens_version_difference(
        self, *, LensAlias: str, BaseLensVersion: str = ..., TargetLensVersion: str = ...
    ) -> GetLensVersionDifferenceOutputTypeDef:
        """
        Get lens version differences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_lens_version_difference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_version_difference)
        """

    async def get_milestone(
        self, *, WorkloadId: str, MilestoneNumber: int
    ) -> GetMilestoneOutputTypeDef:
        """
        Get a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_milestone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_milestone)
        """

    async def get_profile(
        self, *, ProfileArn: str, ProfileVersion: str = ...
    ) -> GetProfileOutputTypeDef:
        """
        Get profile information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_profile)
        """

    async def get_profile_template(self) -> GetProfileTemplateOutputTypeDef:
        """
        Get profile template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_profile_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_profile_template)
        """

    async def get_review_template(self, *, TemplateArn: str) -> GetReviewTemplateOutputTypeDef:
        """
        Get review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_review_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template)
        """

    async def get_review_template_answer(
        self, *, TemplateArn: str, LensAlias: str, QuestionId: str
    ) -> GetReviewTemplateAnswerOutputTypeDef:
        """
        Get review template answer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_review_template_answer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template_answer)
        """

    async def get_review_template_lens_review(
        self, *, TemplateArn: str, LensAlias: str
    ) -> GetReviewTemplateLensReviewOutputTypeDef:
        """
        Get a lens review associated with a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_review_template_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template_lens_review)
        """

    async def get_workload(self, *, WorkloadId: str) -> GetWorkloadOutputTypeDef:
        """
        Get an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.get_workload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_workload)
        """

    async def import_lens(
        self,
        *,
        JSONString: str,
        ClientRequestToken: str,
        LensAlias: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> ImportLensOutputTypeDef:
        """
        Import a new custom lens or update an existing custom lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.import_lens)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#import_lens)
        """

    async def list_answers(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        PillarId: str = ...,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        QuestionPriority: QuestionPriorityType = ...,
    ) -> ListAnswersOutputTypeDef:
        """
        List of answers for a particular workload and lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_answers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_answers)
        """

    async def list_check_details(
        self,
        *,
        WorkloadId: str,
        LensArn: str,
        PillarId: str,
        QuestionId: str,
        ChoiceId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListCheckDetailsOutputTypeDef:
        """
        List of Trusted Advisor check details by account related to the workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_check_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_check_details)
        """

    async def list_check_summaries(
        self,
        *,
        WorkloadId: str,
        LensArn: str,
        PillarId: str,
        QuestionId: str,
        ChoiceId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListCheckSummariesOutputTypeDef:
        """
        List of Trusted Advisor checks summarized for all accounts related to the
        workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_check_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_check_summaries)
        """

    async def list_lens_review_improvements(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        PillarId: str = ...,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        QuestionPriority: QuestionPriorityType = ...,
    ) -> ListLensReviewImprovementsOutputTypeDef:
        """
        List the improvements of a particular lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_review_improvements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_review_improvements)
        """

    async def list_lens_reviews(
        self,
        *,
        WorkloadId: str,
        MilestoneNumber: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListLensReviewsOutputTypeDef:
        """
        List lens reviews for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_reviews)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_reviews)
        """

    async def list_lens_shares(
        self,
        *,
        LensAlias: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: ShareStatusType = ...,
    ) -> ListLensSharesOutputTypeDef:
        """
        List the lens shares associated with the lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lens_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_shares)
        """

    async def list_lenses(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        LensType: LensTypeType = ...,
        LensStatus: LensStatusTypeType = ...,
        LensName: str = ...,
    ) -> ListLensesOutputTypeDef:
        """
        List the available lenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_lenses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lenses)
        """

    async def list_milestones(
        self, *, WorkloadId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMilestonesOutputTypeDef:
        """
        List all milestones for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_milestones)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_milestones)
        """

    async def list_notifications(
        self,
        *,
        WorkloadId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ResourceArn: str = ...,
    ) -> ListNotificationsOutputTypeDef:
        """
        List lens notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_notifications)
        """

    async def list_profile_notifications(
        self, *, WorkloadId: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListProfileNotificationsOutputTypeDef:
        """
        List profile notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_profile_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profile_notifications)
        """

    async def list_profile_shares(
        self,
        *,
        ProfileArn: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: ShareStatusType = ...,
    ) -> ListProfileSharesOutputTypeDef:
        """
        List profile shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_profile_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profile_shares)
        """

    async def list_profiles(
        self,
        *,
        ProfileNamePrefix: str = ...,
        ProfileOwnerType: ProfileOwnerTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListProfilesOutputTypeDef:
        """
        List profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profiles)
        """

    async def list_review_template_answers(
        self,
        *,
        TemplateArn: str,
        LensAlias: str,
        PillarId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListReviewTemplateAnswersOutputTypeDef:
        """
        List the answers of a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_review_template_answers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_review_template_answers)
        """

    async def list_review_templates(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListReviewTemplatesOutputTypeDef:
        """
        List review templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_review_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_review_templates)
        """

    async def list_share_invitations(
        self,
        *,
        WorkloadNamePrefix: str = ...,
        LensNamePrefix: str = ...,
        ShareResourceType: ShareResourceTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ProfileNamePrefix: str = ...,
        TemplateNamePrefix: str = ...,
    ) -> ListShareInvitationsOutputTypeDef:
        """
        List the share invitations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_share_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_share_invitations)
        """

    async def list_tags_for_resource(self, *, WorkloadArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_tags_for_resource)
        """

    async def list_template_shares(
        self,
        *,
        TemplateArn: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: ShareStatusType = ...,
    ) -> ListTemplateSharesOutputTypeDef:
        """
        List review template shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_template_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_template_shares)
        """

    async def list_workload_shares(
        self,
        *,
        WorkloadId: str,
        SharedWithPrefix: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: ShareStatusType = ...,
    ) -> ListWorkloadSharesOutputTypeDef:
        """
        List the workload shares associated with the workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_workload_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_workload_shares)
        """

    async def list_workloads(
        self, *, WorkloadNamePrefix: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkloadsOutputTypeDef:
        """
        Paginated list of workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.list_workloads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_workloads)
        """

    async def tag_resource(self, *, WorkloadArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#tag_resource)
        """

    async def untag_resource(self, *, WorkloadArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#untag_resource)
        """

    async def update_answer(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        QuestionId: str,
        SelectedChoices: Sequence[str] = ...,
        ChoiceUpdates: Mapping[str, ChoiceUpdateTypeDef] = ...,
        Notes: str = ...,
        IsApplicable: bool = ...,
        Reason: AnswerReasonType = ...,
    ) -> UpdateAnswerOutputTypeDef:
        """
        Update the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_answer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_answer)
        """

    async def update_global_settings(
        self,
        *,
        OrganizationSharingStatus: OrganizationSharingStatusType = ...,
        DiscoveryIntegrationStatus: DiscoveryIntegrationStatusType = ...,
        JiraConfiguration: AccountJiraConfigurationInputTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update whether the Amazon Web Services account is opted into organization
        sharing and discovery integration
        features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_global_settings)
        """

    async def update_integration(
        self, *, WorkloadId: str, ClientRequestToken: str, IntegratingService: Literal["JIRA"]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update integration features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_integration)
        """

    async def update_lens_review(
        self,
        *,
        WorkloadId: str,
        LensAlias: str,
        LensNotes: str = ...,
        PillarNotes: Mapping[str, str] = ...,
        JiraConfiguration: JiraSelectedQuestionConfigurationUnionTypeDef = ...,
    ) -> UpdateLensReviewOutputTypeDef:
        """
        Update lens review for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_lens_review)
        """

    async def update_profile(
        self,
        *,
        ProfileArn: str,
        ProfileDescription: str = ...,
        ProfileQuestions: Sequence[ProfileQuestionUpdateTypeDef] = ...,
    ) -> UpdateProfileOutputTypeDef:
        """
        Update a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_profile)
        """

    async def update_review_template(
        self,
        *,
        TemplateArn: str,
        TemplateName: str = ...,
        Description: str = ...,
        Notes: str = ...,
        LensesToAssociate: Sequence[str] = ...,
        LensesToDisassociate: Sequence[str] = ...,
    ) -> UpdateReviewTemplateOutputTypeDef:
        """
        Update a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_review_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template)
        """

    async def update_review_template_answer(
        self,
        *,
        TemplateArn: str,
        LensAlias: str,
        QuestionId: str,
        SelectedChoices: Sequence[str] = ...,
        ChoiceUpdates: Mapping[str, ChoiceUpdateTypeDef] = ...,
        Notes: str = ...,
        IsApplicable: bool = ...,
        Reason: AnswerReasonType = ...,
    ) -> UpdateReviewTemplateAnswerOutputTypeDef:
        """
        Update a review template answer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_review_template_answer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template_answer)
        """

    async def update_review_template_lens_review(
        self,
        *,
        TemplateArn: str,
        LensAlias: str,
        LensNotes: str = ...,
        PillarNotes: Mapping[str, str] = ...,
    ) -> UpdateReviewTemplateLensReviewOutputTypeDef:
        """
        Update a lens review associated with a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_review_template_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template_lens_review)
        """

    async def update_share_invitation(
        self, *, ShareInvitationId: str, ShareInvitationAction: ShareInvitationActionType
    ) -> UpdateShareInvitationOutputTypeDef:
        """
        Update a workload or custom lens share invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_share_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_share_invitation)
        """

    async def update_workload(
        self,
        *,
        WorkloadId: str,
        WorkloadName: str = ...,
        Description: str = ...,
        Environment: WorkloadEnvironmentType = ...,
        AccountIds: Sequence[str] = ...,
        AwsRegions: Sequence[str] = ...,
        NonAwsRegions: Sequence[str] = ...,
        PillarPriorities: Sequence[str] = ...,
        ArchitecturalDesign: str = ...,
        ReviewOwner: str = ...,
        IsReviewOwnerUpdateAcknowledged: bool = ...,
        IndustryType: str = ...,
        Industry: str = ...,
        Notes: str = ...,
        ImprovementStatus: WorkloadImprovementStatusType = ...,
        DiscoveryConfig: WorkloadDiscoveryConfigUnionTypeDef = ...,
        Applications: Sequence[str] = ...,
        JiraConfiguration: WorkloadJiraConfigurationInputTypeDef = ...,
    ) -> UpdateWorkloadOutputTypeDef:
        """
        Update an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_workload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_workload)
        """

    async def update_workload_share(
        self, *, ShareId: str, WorkloadId: str, PermissionType: PermissionTypeType
    ) -> UpdateWorkloadShareOutputTypeDef:
        """
        Update a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.update_workload_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_workload_share)
        """

    async def upgrade_lens_review(
        self, *, WorkloadId: str, LensAlias: str, MilestoneName: str, ClientRequestToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade lens review for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.upgrade_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_lens_review)
        """

    async def upgrade_profile_version(
        self,
        *,
        WorkloadId: str,
        ProfileArn: str,
        MilestoneName: str = ...,
        ClientRequestToken: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.upgrade_profile_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_profile_version)
        """

    async def upgrade_review_template_lens_review(
        self, *, TemplateArn: str, LensAlias: str, ClientRequestToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade the lens review of a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client.upgrade_review_template_lens_review)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_review_template_lens_review)
        """

    async def __aenter__(self) -> "WellArchitectedClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
        """
