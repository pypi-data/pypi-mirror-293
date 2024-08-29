"""
Type annotations for cleanrooms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cleanrooms.client import CleanRoomsServiceClient

    session = get_session()
    async with session.create_client("cleanrooms") as client:
        client: CleanRoomsServiceClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AnalysisRuleTypeType,
    CollaborationQueryLogStatusType,
    ConfiguredTableAnalysisRuleTypeType,
    ConfiguredTableAssociationAnalysisRuleTypeType,
    FilterableMemberStatusType,
    MemberAbilityType,
    MembershipQueryLogStatusType,
    MembershipStatusType,
    PrivacyBudgetTemplateAutoRefreshType,
    ProtectedQueryStatusType,
    SchemaTypeType,
)
from .paginator import (
    ListAnalysisTemplatesPaginator,
    ListCollaborationAnalysisTemplatesPaginator,
    ListCollaborationConfiguredAudienceModelAssociationsPaginator,
    ListCollaborationIdNamespaceAssociationsPaginator,
    ListCollaborationPrivacyBudgetsPaginator,
    ListCollaborationPrivacyBudgetTemplatesPaginator,
    ListCollaborationsPaginator,
    ListConfiguredAudienceModelAssociationsPaginator,
    ListConfiguredTableAssociationsPaginator,
    ListConfiguredTablesPaginator,
    ListIdMappingTablesPaginator,
    ListIdNamespaceAssociationsPaginator,
    ListMembershipsPaginator,
    ListMembersPaginator,
    ListPrivacyBudgetsPaginator,
    ListPrivacyBudgetTemplatesPaginator,
    ListProtectedQueriesPaginator,
    ListSchemasPaginator,
)
from .type_defs import (
    AnalysisParameterTypeDef,
    AnalysisSourceTypeDef,
    BatchGetCollaborationAnalysisTemplateOutputTypeDef,
    BatchGetSchemaAnalysisRuleOutputTypeDef,
    BatchGetSchemaOutputTypeDef,
    ConfiguredTableAnalysisRulePolicyUnionTypeDef,
    ConfiguredTableAssociationAnalysisRulePolicyUnionTypeDef,
    CreateAnalysisTemplateOutputTypeDef,
    CreateCollaborationOutputTypeDef,
    CreateConfiguredAudienceModelAssociationOutputTypeDef,
    CreateConfiguredTableAnalysisRuleOutputTypeDef,
    CreateConfiguredTableAssociationAnalysisRuleOutputTypeDef,
    CreateConfiguredTableAssociationOutputTypeDef,
    CreateConfiguredTableOutputTypeDef,
    CreateIdMappingTableOutputTypeDef,
    CreateIdNamespaceAssociationOutputTypeDef,
    CreateMembershipOutputTypeDef,
    CreatePrivacyBudgetTemplateOutputTypeDef,
    DataEncryptionMetadataTypeDef,
    GetAnalysisTemplateOutputTypeDef,
    GetCollaborationAnalysisTemplateOutputTypeDef,
    GetCollaborationConfiguredAudienceModelAssociationOutputTypeDef,
    GetCollaborationIdNamespaceAssociationOutputTypeDef,
    GetCollaborationOutputTypeDef,
    GetCollaborationPrivacyBudgetTemplateOutputTypeDef,
    GetConfiguredAudienceModelAssociationOutputTypeDef,
    GetConfiguredTableAnalysisRuleOutputTypeDef,
    GetConfiguredTableAssociationAnalysisRuleOutputTypeDef,
    GetConfiguredTableAssociationOutputTypeDef,
    GetConfiguredTableOutputTypeDef,
    GetIdMappingTableOutputTypeDef,
    GetIdNamespaceAssociationOutputTypeDef,
    GetMembershipOutputTypeDef,
    GetPrivacyBudgetTemplateOutputTypeDef,
    GetProtectedQueryOutputTypeDef,
    GetSchemaAnalysisRuleOutputTypeDef,
    GetSchemaOutputTypeDef,
    IdMappingConfigTypeDef,
    IdMappingTableInputReferenceConfigTypeDef,
    IdNamespaceAssociationInputReferenceConfigTypeDef,
    ListAnalysisTemplatesOutputTypeDef,
    ListCollaborationAnalysisTemplatesOutputTypeDef,
    ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef,
    ListCollaborationIdNamespaceAssociationsOutputTypeDef,
    ListCollaborationPrivacyBudgetsOutputTypeDef,
    ListCollaborationPrivacyBudgetTemplatesOutputTypeDef,
    ListCollaborationsOutputTypeDef,
    ListConfiguredAudienceModelAssociationsOutputTypeDef,
    ListConfiguredTableAssociationsOutputTypeDef,
    ListConfiguredTablesOutputTypeDef,
    ListIdMappingTablesOutputTypeDef,
    ListIdNamespaceAssociationsOutputTypeDef,
    ListMembershipsOutputTypeDef,
    ListMembersOutputTypeDef,
    ListPrivacyBudgetsOutputTypeDef,
    ListPrivacyBudgetTemplatesOutputTypeDef,
    ListProtectedQueriesOutputTypeDef,
    ListSchemasOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    MembershipPaymentConfigurationTypeDef,
    MembershipProtectedQueryResultConfigurationTypeDef,
    MemberSpecificationTypeDef,
    PaymentConfigurationTypeDef,
    PopulateIdMappingTableOutputTypeDef,
    PreviewPrivacyImpactOutputTypeDef,
    PreviewPrivacyImpactParametersInputTypeDef,
    PrivacyBudgetTemplateParametersInputTypeDef,
    PrivacyBudgetTemplateUpdateParametersTypeDef,
    ProtectedQueryResultConfigurationTypeDef,
    ProtectedQuerySQLParametersUnionTypeDef,
    SchemaAnalysisRuleRequestTypeDef,
    StartProtectedQueryOutputTypeDef,
    TableReferenceTypeDef,
    UpdateAnalysisTemplateOutputTypeDef,
    UpdateCollaborationOutputTypeDef,
    UpdateConfiguredAudienceModelAssociationOutputTypeDef,
    UpdateConfiguredTableAnalysisRuleOutputTypeDef,
    UpdateConfiguredTableAssociationAnalysisRuleOutputTypeDef,
    UpdateConfiguredTableAssociationOutputTypeDef,
    UpdateConfiguredTableOutputTypeDef,
    UpdateIdMappingTableOutputTypeDef,
    UpdateIdNamespaceAssociationOutputTypeDef,
    UpdateMembershipOutputTypeDef,
    UpdatePrivacyBudgetTemplateOutputTypeDef,
    UpdateProtectedQueryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CleanRoomsServiceClient",)

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

class CleanRoomsServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CleanRoomsServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#exceptions)
        """

    async def batch_get_collaboration_analysis_template(
        self, *, collaborationIdentifier: str, analysisTemplateArns: Sequence[str]
    ) -> BatchGetCollaborationAnalysisTemplateOutputTypeDef:
        """
        Retrieves multiple analysis templates within a collaboration by their Amazon
        Resource Names
        (ARNs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.batch_get_collaboration_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#batch_get_collaboration_analysis_template)
        """

    async def batch_get_schema(
        self, *, collaborationIdentifier: str, names: Sequence[str]
    ) -> BatchGetSchemaOutputTypeDef:
        """
        Retrieves multiple schemas by their identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.batch_get_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#batch_get_schema)
        """

    async def batch_get_schema_analysis_rule(
        self,
        *,
        collaborationIdentifier: str,
        schemaAnalysisRuleRequests: Sequence[SchemaAnalysisRuleRequestTypeDef],
    ) -> BatchGetSchemaAnalysisRuleOutputTypeDef:
        """
        Retrieves multiple analysis rule schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.batch_get_schema_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#batch_get_schema_analysis_rule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#close)
        """

    async def create_analysis_template(
        self,
        *,
        membershipIdentifier: str,
        name: str,
        format: Literal["SQL"],
        source: AnalysisSourceTypeDef,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        analysisParameters: Sequence[AnalysisParameterTypeDef] = ...,
    ) -> CreateAnalysisTemplateOutputTypeDef:
        """
        Creates a new analysis template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_analysis_template)
        """

    async def create_collaboration(
        self,
        *,
        members: Sequence[MemberSpecificationTypeDef],
        name: str,
        description: str,
        creatorMemberAbilities: Sequence[MemberAbilityType],
        creatorDisplayName: str,
        queryLogStatus: CollaborationQueryLogStatusType,
        dataEncryptionMetadata: DataEncryptionMetadataTypeDef = ...,
        tags: Mapping[str, str] = ...,
        creatorPaymentConfiguration: PaymentConfigurationTypeDef = ...,
    ) -> CreateCollaborationOutputTypeDef:
        """
        Creates a new collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_collaboration)
        """

    async def create_configured_audience_model_association(
        self,
        *,
        membershipIdentifier: str,
        configuredAudienceModelArn: str,
        configuredAudienceModelAssociationName: str,
        manageResourcePolicies: bool,
        tags: Mapping[str, str] = ...,
        description: str = ...,
    ) -> CreateConfiguredAudienceModelAssociationOutputTypeDef:
        """
        Provides the details necessary to create a configured audience model
        association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_audience_model_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_audience_model_association)
        """

    async def create_configured_table(
        self,
        *,
        name: str,
        tableReference: TableReferenceTypeDef,
        allowedColumns: Sequence[str],
        analysisMethod: Literal["DIRECT_QUERY"],
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateConfiguredTableOutputTypeDef:
        """
        Creates a new configured table resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table)
        """

    async def create_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAnalysisRulePolicyUnionTypeDef,
    ) -> CreateConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Creates a new analysis rule for a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table_analysis_rule)
        """

    async def create_configured_table_association(
        self,
        *,
        name: str,
        membershipIdentifier: str,
        configuredTableIdentifier: str,
        roleArn: str,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateConfiguredTableAssociationOutputTypeDef:
        """
        Creates a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table_association)
        """

    async def create_configured_table_association_analysis_rule(
        self,
        *,
        membershipIdentifier: str,
        configuredTableAssociationIdentifier: str,
        analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAssociationAnalysisRulePolicyUnionTypeDef,
    ) -> CreateConfiguredTableAssociationAnalysisRuleOutputTypeDef:
        """
        Creates a new analysis rule for an associated configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table_association_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table_association_analysis_rule)
        """

    async def create_id_mapping_table(
        self,
        *,
        membershipIdentifier: str,
        name: str,
        inputReferenceConfig: IdMappingTableInputReferenceConfigTypeDef,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        kmsKeyArn: str = ...,
    ) -> CreateIdMappingTableOutputTypeDef:
        """
        Creates an ID mapping table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_id_mapping_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_id_mapping_table)
        """

    async def create_id_namespace_association(
        self,
        *,
        membershipIdentifier: str,
        inputReferenceConfig: IdNamespaceAssociationInputReferenceConfigTypeDef,
        name: str,
        tags: Mapping[str, str] = ...,
        description: str = ...,
        idMappingConfig: IdMappingConfigTypeDef = ...,
    ) -> CreateIdNamespaceAssociationOutputTypeDef:
        """
        Creates an ID namespace association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_id_namespace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_id_namespace_association)
        """

    async def create_membership(
        self,
        *,
        collaborationIdentifier: str,
        queryLogStatus: MembershipQueryLogStatusType,
        tags: Mapping[str, str] = ...,
        defaultResultConfiguration: MembershipProtectedQueryResultConfigurationTypeDef = ...,
        paymentConfiguration: MembershipPaymentConfigurationTypeDef = ...,
    ) -> CreateMembershipOutputTypeDef:
        """
        Creates a membership for a specific collaboration identifier and joins the
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_membership)
        """

    async def create_privacy_budget_template(
        self,
        *,
        membershipIdentifier: str,
        autoRefresh: PrivacyBudgetTemplateAutoRefreshType,
        privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"],
        parameters: PrivacyBudgetTemplateParametersInputTypeDef,
        tags: Mapping[str, str] = ...,
    ) -> CreatePrivacyBudgetTemplateOutputTypeDef:
        """
        Creates a privacy budget template for a specified membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_privacy_budget_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_privacy_budget_template)
        """

    async def delete_analysis_template(
        self, *, membershipIdentifier: str, analysisTemplateIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes an analysis template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_analysis_template)
        """

    async def delete_collaboration(self, *, collaborationIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_collaboration)
        """

    async def delete_configured_audience_model_association(
        self, *, configuredAudienceModelAssociationIdentifier: str, membershipIdentifier: str
    ) -> Dict[str, Any]:
        """
        Provides the information necessary to delete a configured audience model
        association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_audience_model_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_audience_model_association)
        """

    async def delete_configured_table(self, *, configuredTableIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table)
        """

    async def delete_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
    ) -> Dict[str, Any]:
        """
        Deletes a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table_analysis_rule)
        """

    async def delete_configured_table_association(
        self, *, configuredTableAssociationIdentifier: str, membershipIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table_association)
        """

    async def delete_configured_table_association_analysis_rule(
        self,
        *,
        membershipIdentifier: str,
        configuredTableAssociationIdentifier: str,
        analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType,
    ) -> Dict[str, Any]:
        """
        Deletes an analysis rule for a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table_association_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table_association_analysis_rule)
        """

    async def delete_id_mapping_table(
        self, *, idMappingTableIdentifier: str, membershipIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes an ID mapping table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_id_mapping_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_id_mapping_table)
        """

    async def delete_id_namespace_association(
        self, *, idNamespaceAssociationIdentifier: str, membershipIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes an ID namespace association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_id_namespace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_id_namespace_association)
        """

    async def delete_member(
        self, *, collaborationIdentifier: str, accountId: str
    ) -> Dict[str, Any]:
        """
        Removes the specified member from a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_member)
        """

    async def delete_membership(self, *, membershipIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a specified membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_membership)
        """

    async def delete_privacy_budget_template(
        self, *, membershipIdentifier: str, privacyBudgetTemplateIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes a privacy budget template for a specified membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_privacy_budget_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_privacy_budget_template)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#generate_presigned_url)
        """

    async def get_analysis_template(
        self, *, membershipIdentifier: str, analysisTemplateIdentifier: str
    ) -> GetAnalysisTemplateOutputTypeDef:
        """
        Retrieves an analysis template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_analysis_template)
        """

    async def get_collaboration(
        self, *, collaborationIdentifier: str
    ) -> GetCollaborationOutputTypeDef:
        """
        Returns metadata about a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration)
        """

    async def get_collaboration_analysis_template(
        self, *, collaborationIdentifier: str, analysisTemplateArn: str
    ) -> GetCollaborationAnalysisTemplateOutputTypeDef:
        """
        Retrieves an analysis template within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration_analysis_template)
        """

    async def get_collaboration_configured_audience_model_association(
        self, *, collaborationIdentifier: str, configuredAudienceModelAssociationIdentifier: str
    ) -> GetCollaborationConfiguredAudienceModelAssociationOutputTypeDef:
        """
        Retrieves a configured audience model association within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration_configured_audience_model_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration_configured_audience_model_association)
        """

    async def get_collaboration_id_namespace_association(
        self, *, collaborationIdentifier: str, idNamespaceAssociationIdentifier: str
    ) -> GetCollaborationIdNamespaceAssociationOutputTypeDef:
        """
        Retrieves an ID namespace association from a specific collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration_id_namespace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration_id_namespace_association)
        """

    async def get_collaboration_privacy_budget_template(
        self, *, collaborationIdentifier: str, privacyBudgetTemplateIdentifier: str
    ) -> GetCollaborationPrivacyBudgetTemplateOutputTypeDef:
        """
        Returns details about a specified privacy budget template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration_privacy_budget_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration_privacy_budget_template)
        """

    async def get_configured_audience_model_association(
        self, *, configuredAudienceModelAssociationIdentifier: str, membershipIdentifier: str
    ) -> GetConfiguredAudienceModelAssociationOutputTypeDef:
        """
        Returns information about a configured audience model association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_audience_model_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_audience_model_association)
        """

    async def get_configured_table(
        self, *, configuredTableIdentifier: str
    ) -> GetConfiguredTableOutputTypeDef:
        """
        Retrieves a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table)
        """

    async def get_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
    ) -> GetConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Retrieves a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table_analysis_rule)
        """

    async def get_configured_table_association(
        self, *, configuredTableAssociationIdentifier: str, membershipIdentifier: str
    ) -> GetConfiguredTableAssociationOutputTypeDef:
        """
        Retrieves a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table_association)
        """

    async def get_configured_table_association_analysis_rule(
        self,
        *,
        membershipIdentifier: str,
        configuredTableAssociationIdentifier: str,
        analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType,
    ) -> GetConfiguredTableAssociationAnalysisRuleOutputTypeDef:
        """
        Retrieves the analysis rule for a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table_association_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table_association_analysis_rule)
        """

    async def get_id_mapping_table(
        self, *, idMappingTableIdentifier: str, membershipIdentifier: str
    ) -> GetIdMappingTableOutputTypeDef:
        """
        Retrieves an ID mapping table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_id_mapping_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_id_mapping_table)
        """

    async def get_id_namespace_association(
        self, *, idNamespaceAssociationIdentifier: str, membershipIdentifier: str
    ) -> GetIdNamespaceAssociationOutputTypeDef:
        """
        Retrieves an ID namespace association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_id_namespace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_id_namespace_association)
        """

    async def get_membership(self, *, membershipIdentifier: str) -> GetMembershipOutputTypeDef:
        """
        Retrieves a specified membership for an identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_membership)
        """

    async def get_privacy_budget_template(
        self, *, membershipIdentifier: str, privacyBudgetTemplateIdentifier: str
    ) -> GetPrivacyBudgetTemplateOutputTypeDef:
        """
        Returns details for a specified privacy budget template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_privacy_budget_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_privacy_budget_template)
        """

    async def get_protected_query(
        self, *, membershipIdentifier: str, protectedQueryIdentifier: str
    ) -> GetProtectedQueryOutputTypeDef:
        """
        Returns query processing metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_protected_query)
        """

    async def get_schema(
        self, *, collaborationIdentifier: str, name: str
    ) -> GetSchemaOutputTypeDef:
        """
        Retrieves the schema for a relation within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_schema)
        """

    async def get_schema_analysis_rule(
        self, *, collaborationIdentifier: str, name: str, type: AnalysisRuleTypeType
    ) -> GetSchemaAnalysisRuleOutputTypeDef:
        """
        Retrieves a schema analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_schema_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_schema_analysis_rule)
        """

    async def list_analysis_templates(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListAnalysisTemplatesOutputTypeDef:
        """
        Lists analysis templates that the caller owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_analysis_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_analysis_templates)
        """

    async def list_collaboration_analysis_templates(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListCollaborationAnalysisTemplatesOutputTypeDef:
        """
        Lists analysis templates within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaboration_analysis_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaboration_analysis_templates)
        """

    async def list_collaboration_configured_audience_model_associations(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListCollaborationConfiguredAudienceModelAssociationsOutputTypeDef:
        """
        Lists configured audience model associations within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaboration_configured_audience_model_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaboration_configured_audience_model_associations)
        """

    async def list_collaboration_id_namespace_associations(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListCollaborationIdNamespaceAssociationsOutputTypeDef:
        """
        Returns a list of the ID namespace associations in a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaboration_id_namespace_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaboration_id_namespace_associations)
        """

    async def list_collaboration_privacy_budget_templates(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListCollaborationPrivacyBudgetTemplatesOutputTypeDef:
        """
        Returns an array that summarizes each privacy budget template in a specified
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaboration_privacy_budget_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaboration_privacy_budget_templates)
        """

    async def list_collaboration_privacy_budgets(
        self,
        *,
        collaborationIdentifier: str,
        privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"],
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListCollaborationPrivacyBudgetsOutputTypeDef:
        """
        Returns an array that summarizes each privacy budget in a specified
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaboration_privacy_budgets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaboration_privacy_budgets)
        """

    async def list_collaborations(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        memberStatus: FilterableMemberStatusType = ...,
    ) -> ListCollaborationsOutputTypeDef:
        """
        Lists collaborations the caller owns, is active in, or has been invited to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaborations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaborations)
        """

    async def list_configured_audience_model_associations(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredAudienceModelAssociationsOutputTypeDef:
        """
        Lists information about requested configured audience model associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_configured_audience_model_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_configured_audience_model_associations)
        """

    async def list_configured_table_associations(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredTableAssociationsOutputTypeDef:
        """
        Lists configured table associations for a membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_configured_table_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_configured_table_associations)
        """

    async def list_configured_tables(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredTablesOutputTypeDef:
        """
        Lists configured tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_configured_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_configured_tables)
        """

    async def list_id_mapping_tables(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListIdMappingTablesOutputTypeDef:
        """
        Returns a list of ID mapping tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_id_mapping_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_id_mapping_tables)
        """

    async def list_id_namespace_associations(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListIdNamespaceAssociationsOutputTypeDef:
        """
        Returns a list of ID namespace associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_id_namespace_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_id_namespace_associations)
        """

    async def list_members(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListMembersOutputTypeDef:
        """
        Lists all members within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_members)
        """

    async def list_memberships(
        self, *, nextToken: str = ..., maxResults: int = ..., status: MembershipStatusType = ...
    ) -> ListMembershipsOutputTypeDef:
        """
        Lists all memberships resources within the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_memberships)
        """

    async def list_privacy_budget_templates(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListPrivacyBudgetTemplatesOutputTypeDef:
        """
        Returns detailed information about the privacy budget templates in a specified
        membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_privacy_budget_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_privacy_budget_templates)
        """

    async def list_privacy_budgets(
        self,
        *,
        membershipIdentifier: str,
        privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"],
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListPrivacyBudgetsOutputTypeDef:
        """
        Returns detailed information about the privacy budgets in a specified
        membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_privacy_budgets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_privacy_budgets)
        """

    async def list_protected_queries(
        self,
        *,
        membershipIdentifier: str,
        status: ProtectedQueryStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListProtectedQueriesOutputTypeDef:
        """
        Lists protected queries, sorted by the most recent query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_protected_queries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_protected_queries)
        """

    async def list_schemas(
        self,
        *,
        collaborationIdentifier: str,
        schemaType: SchemaTypeType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListSchemasOutputTypeDef:
        """
        Lists the schemas for relations within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_schemas)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_schemas)
        """

    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Lists all of the tags that have been added to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_tags_for_resource)
        """

    async def populate_id_mapping_table(
        self, *, idMappingTableIdentifier: str, membershipIdentifier: str
    ) -> PopulateIdMappingTableOutputTypeDef:
        """
        Defines the information that's necessary to populate an ID mapping table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.populate_id_mapping_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#populate_id_mapping_table)
        """

    async def preview_privacy_impact(
        self, *, membershipIdentifier: str, parameters: PreviewPrivacyImpactParametersInputTypeDef
    ) -> PreviewPrivacyImpactOutputTypeDef:
        """
        An estimate of the number of aggregation functions that the member who can
        query can run given epsilon and noise
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.preview_privacy_impact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#preview_privacy_impact)
        """

    async def start_protected_query(
        self,
        *,
        type: Literal["SQL"],
        membershipIdentifier: str,
        sqlParameters: ProtectedQuerySQLParametersUnionTypeDef,
        resultConfiguration: ProtectedQueryResultConfigurationTypeDef = ...,
    ) -> StartProtectedQueryOutputTypeDef:
        """
        Creates a protected query that is started by Clean Rooms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.start_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#start_protected_query)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag or list of tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#untag_resource)
        """

    async def update_analysis_template(
        self, *, membershipIdentifier: str, analysisTemplateIdentifier: str, description: str = ...
    ) -> UpdateAnalysisTemplateOutputTypeDef:
        """
        Updates the analysis template metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_analysis_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_analysis_template)
        """

    async def update_collaboration(
        self, *, collaborationIdentifier: str, name: str = ..., description: str = ...
    ) -> UpdateCollaborationOutputTypeDef:
        """
        Updates collaboration metadata and can only be called by the collaboration
        owner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_collaboration)
        """

    async def update_configured_audience_model_association(
        self,
        *,
        configuredAudienceModelAssociationIdentifier: str,
        membershipIdentifier: str,
        description: str = ...,
        name: str = ...,
    ) -> UpdateConfiguredAudienceModelAssociationOutputTypeDef:
        """
        Provides the details necessary to update a configured audience model
        association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_audience_model_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_audience_model_association)
        """

    async def update_configured_table(
        self, *, configuredTableIdentifier: str, name: str = ..., description: str = ...
    ) -> UpdateConfiguredTableOutputTypeDef:
        """
        Updates a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table)
        """

    async def update_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAnalysisRulePolicyUnionTypeDef,
    ) -> UpdateConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Updates a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table_analysis_rule)
        """

    async def update_configured_table_association(
        self,
        *,
        configuredTableAssociationIdentifier: str,
        membershipIdentifier: str,
        description: str = ...,
        roleArn: str = ...,
    ) -> UpdateConfiguredTableAssociationOutputTypeDef:
        """
        Updates a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table_association)
        """

    async def update_configured_table_association_analysis_rule(
        self,
        *,
        membershipIdentifier: str,
        configuredTableAssociationIdentifier: str,
        analysisRuleType: ConfiguredTableAssociationAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAssociationAnalysisRulePolicyUnionTypeDef,
    ) -> UpdateConfiguredTableAssociationAnalysisRuleOutputTypeDef:
        """
        Updates the analysis rule for a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table_association_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table_association_analysis_rule)
        """

    async def update_id_mapping_table(
        self,
        *,
        idMappingTableIdentifier: str,
        membershipIdentifier: str,
        description: str = ...,
        kmsKeyArn: str = ...,
    ) -> UpdateIdMappingTableOutputTypeDef:
        """
        Provides the details that are necessary to update an ID mapping table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_id_mapping_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_id_mapping_table)
        """

    async def update_id_namespace_association(
        self,
        *,
        idNamespaceAssociationIdentifier: str,
        membershipIdentifier: str,
        name: str = ...,
        description: str = ...,
        idMappingConfig: IdMappingConfigTypeDef = ...,
    ) -> UpdateIdNamespaceAssociationOutputTypeDef:
        """
        Provides the details that are necessary to update an ID namespace association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_id_namespace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_id_namespace_association)
        """

    async def update_membership(
        self,
        *,
        membershipIdentifier: str,
        queryLogStatus: MembershipQueryLogStatusType = ...,
        defaultResultConfiguration: MembershipProtectedQueryResultConfigurationTypeDef = ...,
    ) -> UpdateMembershipOutputTypeDef:
        """
        Updates a membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_membership)
        """

    async def update_privacy_budget_template(
        self,
        *,
        membershipIdentifier: str,
        privacyBudgetTemplateIdentifier: str,
        privacyBudgetType: Literal["DIFFERENTIAL_PRIVACY"],
        parameters: PrivacyBudgetTemplateUpdateParametersTypeDef = ...,
    ) -> UpdatePrivacyBudgetTemplateOutputTypeDef:
        """
        Updates the privacy budget template for the specified membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_privacy_budget_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_privacy_budget_template)
        """

    async def update_protected_query(
        self,
        *,
        membershipIdentifier: str,
        protectedQueryIdentifier: str,
        targetStatus: Literal["CANCELLED"],
    ) -> UpdateProtectedQueryOutputTypeDef:
        """
        Updates the processing of a currently running query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_protected_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_analysis_templates"]
    ) -> ListAnalysisTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_analysis_templates"]
    ) -> ListCollaborationAnalysisTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_configured_audience_model_associations"]
    ) -> ListCollaborationConfiguredAudienceModelAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_id_namespace_associations"]
    ) -> ListCollaborationIdNamespaceAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_privacy_budget_templates"]
    ) -> ListCollaborationPrivacyBudgetTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaboration_privacy_budgets"]
    ) -> ListCollaborationPrivacyBudgetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaborations"]
    ) -> ListCollaborationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_audience_model_associations"]
    ) -> ListConfiguredAudienceModelAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_table_associations"]
    ) -> ListConfiguredTableAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_tables"]
    ) -> ListConfiguredTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_id_mapping_tables"]
    ) -> ListIdMappingTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_id_namespace_associations"]
    ) -> ListIdNamespaceAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_memberships"]
    ) -> ListMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_privacy_budget_templates"]
    ) -> ListPrivacyBudgetTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_privacy_budgets"]
    ) -> ListPrivacyBudgetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protected_queries"]
    ) -> ListProtectedQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """

    async def __aenter__(self) -> "CleanRoomsServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
        """
