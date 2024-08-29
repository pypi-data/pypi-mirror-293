"""
Type annotations for cloudformation service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudformation.client import CloudFormationClient

    session = get_session()
    async with session.create_client("cloudformation") as client:
        client: CloudFormationClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CallAsType,
    CapabilityType,
    ChangeSetTypeType,
    DeletionModeType,
    DeprecatedStatusType,
    HandlerErrorCodeType,
    OnFailureType,
    OnStackFailureType,
    OperationStatusType,
    PermissionModelsType,
    ProvisioningTypeType,
    RegistrationStatusType,
    RegistryTypeType,
    ResourceSignalStatusType,
    StackResourceDriftStatusType,
    StackSetStatusType,
    StackStatusType,
    TemplateFormatType,
    TemplateStageType,
    ThirdPartyTypeType,
    VersionBumpType,
    VisibilityType,
)
from .paginator import (
    DescribeAccountLimitsPaginator,
    DescribeChangeSetPaginator,
    DescribeStackEventsPaginator,
    DescribeStacksPaginator,
    ListChangeSetsPaginator,
    ListExportsPaginator,
    ListGeneratedTemplatesPaginator,
    ListImportsPaginator,
    ListResourceScanRelatedResourcesPaginator,
    ListResourceScanResourcesPaginator,
    ListResourceScansPaginator,
    ListStackInstancesPaginator,
    ListStackResourcesPaginator,
    ListStackSetOperationResultsPaginator,
    ListStackSetOperationsPaginator,
    ListStackSetsPaginator,
    ListStacksPaginator,
    ListTypesPaginator,
)
from .type_defs import (
    ActivateTypeOutputTypeDef,
    AutoDeploymentTypeDef,
    BatchDescribeTypeConfigurationsOutputTypeDef,
    CreateChangeSetOutputTypeDef,
    CreateGeneratedTemplateOutputTypeDef,
    CreateStackInstancesOutputTypeDef,
    CreateStackOutputTypeDef,
    CreateStackSetOutputTypeDef,
    DeleteStackInstancesOutputTypeDef,
    DeploymentTargetsUnionTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeChangeSetHooksOutputTypeDef,
    DescribeChangeSetOutputTypeDef,
    DescribeGeneratedTemplateOutputTypeDef,
    DescribeOrganizationsAccessOutputTypeDef,
    DescribePublisherOutputTypeDef,
    DescribeResourceScanOutputTypeDef,
    DescribeStackDriftDetectionStatusOutputTypeDef,
    DescribeStackEventsOutputTypeDef,
    DescribeStackInstanceOutputTypeDef,
    DescribeStackResourceDriftsOutputTypeDef,
    DescribeStackResourceOutputTypeDef,
    DescribeStackResourcesOutputTypeDef,
    DescribeStackSetOperationOutputTypeDef,
    DescribeStackSetOutputTypeDef,
    DescribeStacksOutputTypeDef,
    DescribeTypeOutputTypeDef,
    DescribeTypeRegistrationOutputTypeDef,
    DetectStackDriftOutputTypeDef,
    DetectStackResourceDriftOutputTypeDef,
    DetectStackSetDriftOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EstimateTemplateCostOutputTypeDef,
    GetGeneratedTemplateOutputTypeDef,
    GetStackPolicyOutputTypeDef,
    GetTemplateOutputTypeDef,
    GetTemplateSummaryOutputTypeDef,
    ImportStacksToStackSetOutputTypeDef,
    ListChangeSetsOutputTypeDef,
    ListExportsOutputTypeDef,
    ListGeneratedTemplatesOutputTypeDef,
    ListImportsOutputTypeDef,
    ListResourceScanRelatedResourcesOutputTypeDef,
    ListResourceScanResourcesOutputTypeDef,
    ListResourceScansOutputTypeDef,
    ListStackInstanceResourceDriftsOutputTypeDef,
    ListStackInstancesOutputTypeDef,
    ListStackResourcesOutputTypeDef,
    ListStackSetAutoDeploymentTargetsOutputTypeDef,
    ListStackSetOperationResultsOutputTypeDef,
    ListStackSetOperationsOutputTypeDef,
    ListStackSetsOutputTypeDef,
    ListStacksOutputTypeDef,
    ListTypeRegistrationsOutputTypeDef,
    ListTypesOutputTypeDef,
    ListTypeVersionsOutputTypeDef,
    LoggingConfigTypeDef,
    ManagedExecutionTypeDef,
    OperationResultFilterTypeDef,
    ParameterTypeDef,
    PublishTypeOutputTypeDef,
    RegisterPublisherOutputTypeDef,
    RegisterTypeOutputTypeDef,
    ResourceDefinitionTypeDef,
    ResourceToImportTypeDef,
    RollbackConfigurationUnionTypeDef,
    RollbackStackOutputTypeDef,
    ScannedResourceIdentifierTypeDef,
    SetTypeConfigurationOutputTypeDef,
    StackInstanceFilterTypeDef,
    StackSetOperationPreferencesUnionTypeDef,
    StartResourceScanOutputTypeDef,
    TagTypeDef,
    TemplateConfigurationTypeDef,
    TemplateSummaryConfigTypeDef,
    TestTypeOutputTypeDef,
    TypeConfigurationIdentifierTypeDef,
    TypeFiltersTypeDef,
    UpdateGeneratedTemplateOutputTypeDef,
    UpdateStackInstancesOutputTypeDef,
    UpdateStackOutputTypeDef,
    UpdateStackSetOutputTypeDef,
    UpdateTerminationProtectionOutputTypeDef,
    ValidateTemplateOutputTypeDef,
)
from .waiter import (
    ChangeSetCreateCompleteWaiter,
    StackCreateCompleteWaiter,
    StackDeleteCompleteWaiter,
    StackExistsWaiter,
    StackImportCompleteWaiter,
    StackRollbackCompleteWaiter,
    StackUpdateCompleteWaiter,
    TypeRegistrationCompleteWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CloudFormationClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    CFNRegistryException: Type[BotocoreClientError]
    ChangeSetNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentResourcesLimitExceededException: Type[BotocoreClientError]
    CreatedButModifiedException: Type[BotocoreClientError]
    GeneratedTemplateNotFoundException: Type[BotocoreClientError]
    InsufficientCapabilitiesException: Type[BotocoreClientError]
    InvalidChangeSetStatusException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NameAlreadyExistsException: Type[BotocoreClientError]
    OperationIdAlreadyExistsException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    OperationNotFoundException: Type[BotocoreClientError]
    OperationStatusCheckFailedException: Type[BotocoreClientError]
    ResourceScanInProgressException: Type[BotocoreClientError]
    ResourceScanLimitExceededException: Type[BotocoreClientError]
    ResourceScanNotFoundException: Type[BotocoreClientError]
    StackInstanceNotFoundException: Type[BotocoreClientError]
    StackNotFoundException: Type[BotocoreClientError]
    StackSetNotEmptyException: Type[BotocoreClientError]
    StackSetNotFoundException: Type[BotocoreClientError]
    StaleRequestException: Type[BotocoreClientError]
    TokenAlreadyExistsException: Type[BotocoreClientError]
    TypeConfigurationNotFoundException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]

class CloudFormationClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudFormationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#exceptions)
        """

    async def activate_organizations_access(self) -> Dict[str, Any]:
        """
        Activate trusted access with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.activate_organizations_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#activate_organizations_access)
        """

    async def activate_type(
        self,
        *,
        Type: ThirdPartyTypeType = ...,
        PublicTypeArn: str = ...,
        PublisherId: str = ...,
        TypeName: str = ...,
        TypeNameAlias: str = ...,
        AutoUpdate: bool = ...,
        LoggingConfig: LoggingConfigTypeDef = ...,
        ExecutionRoleArn: str = ...,
        VersionBump: VersionBumpType = ...,
        MajorVersion: int = ...,
    ) -> ActivateTypeOutputTypeDef:
        """
        Activates a public third-party extension, making it available for use in stack
        templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.activate_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#activate_type)
        """

    async def batch_describe_type_configurations(
        self, *, TypeConfigurationIdentifiers: Sequence[TypeConfigurationIdentifierTypeDef]
    ) -> BatchDescribeTypeConfigurationsOutputTypeDef:
        """
        Returns configuration data for the specified CloudFormation extensions, from
        the CloudFormation registry for the account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.batch_describe_type_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#batch_describe_type_configurations)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#can_paginate)
        """

    async def cancel_update_stack(
        self, *, StackName: str, ClientRequestToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels an update on the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.cancel_update_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#cancel_update_stack)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#close)
        """

    async def continue_update_rollback(
        self,
        *,
        StackName: str,
        RoleARN: str = ...,
        ResourcesToSkip: Sequence[str] = ...,
        ClientRequestToken: str = ...,
    ) -> Dict[str, Any]:
        """
        For a specified stack that's in the `UPDATE_ROLLBACK_FAILED` state, continues
        rolling it back to the `UPDATE_ROLLBACK_COMPLETE`
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.continue_update_rollback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#continue_update_rollback)
        """

    async def create_change_set(
        self,
        *,
        StackName: str,
        ChangeSetName: str,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        UsePreviousTemplate: bool = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
        Capabilities: Sequence[CapabilityType] = ...,
        ResourceTypes: Sequence[str] = ...,
        RoleARN: str = ...,
        RollbackConfiguration: RollbackConfigurationUnionTypeDef = ...,
        NotificationARNs: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientToken: str = ...,
        Description: str = ...,
        ChangeSetType: ChangeSetTypeType = ...,
        ResourcesToImport: Sequence[ResourceToImportTypeDef] = ...,
        IncludeNestedStacks: bool = ...,
        OnStackFailure: OnStackFailureType = ...,
        ImportExistingResources: bool = ...,
    ) -> CreateChangeSetOutputTypeDef:
        """
        Creates a list of changes that will be applied to a stack so that you can
        review the changes before executing
        them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#create_change_set)
        """

    async def create_generated_template(
        self,
        *,
        GeneratedTemplateName: str,
        Resources: Sequence[ResourceDefinitionTypeDef] = ...,
        StackName: str = ...,
        TemplateConfiguration: TemplateConfigurationTypeDef = ...,
    ) -> CreateGeneratedTemplateOutputTypeDef:
        """
        Creates a template from existing resources that are not already managed with
        CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_generated_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#create_generated_template)
        """

    async def create_stack(
        self,
        *,
        StackName: str,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
        DisableRollback: bool = ...,
        RollbackConfiguration: RollbackConfigurationUnionTypeDef = ...,
        TimeoutInMinutes: int = ...,
        NotificationARNs: Sequence[str] = ...,
        Capabilities: Sequence[CapabilityType] = ...,
        ResourceTypes: Sequence[str] = ...,
        RoleARN: str = ...,
        OnFailure: OnFailureType = ...,
        StackPolicyBody: str = ...,
        StackPolicyURL: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ClientRequestToken: str = ...,
        EnableTerminationProtection: bool = ...,
        RetainExceptOnCreate: bool = ...,
    ) -> CreateStackOutputTypeDef:
        """
        Creates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#create_stack)
        """

    async def create_stack_instances(
        self,
        *,
        StackSetName: str,
        Regions: Sequence[str],
        Accounts: Sequence[str] = ...,
        DeploymentTargets: DeploymentTargetsUnionTypeDef = ...,
        ParameterOverrides: Sequence[ParameterTypeDef] = ...,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        OperationId: str = ...,
        CallAs: CallAsType = ...,
    ) -> CreateStackInstancesOutputTypeDef:
        """
        Creates stack instances for the specified accounts, within the specified Amazon
        Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#create_stack_instances)
        """

    async def create_stack_set(
        self,
        *,
        StackSetName: str,
        Description: str = ...,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        StackId: str = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
        Capabilities: Sequence[CapabilityType] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        AdministrationRoleARN: str = ...,
        ExecutionRoleName: str = ...,
        PermissionModel: PermissionModelsType = ...,
        AutoDeployment: AutoDeploymentTypeDef = ...,
        CallAs: CallAsType = ...,
        ClientRequestToken: str = ...,
        ManagedExecution: ManagedExecutionTypeDef = ...,
    ) -> CreateStackSetOutputTypeDef:
        """
        Creates a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#create_stack_set)
        """

    async def deactivate_organizations_access(self) -> Dict[str, Any]:
        """
        Deactivates trusted access with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deactivate_organizations_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#deactivate_organizations_access)
        """

    async def deactivate_type(
        self, *, TypeName: str = ..., Type: ThirdPartyTypeType = ..., Arn: str = ...
    ) -> Dict[str, Any]:
        """
        Deactivates a public extension that was previously activated in this account
        and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deactivate_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#deactivate_type)
        """

    async def delete_change_set(
        self, *, ChangeSetName: str, StackName: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified change set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#delete_change_set)
        """

    async def delete_generated_template(
        self, *, GeneratedTemplateName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deleted a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_generated_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#delete_generated_template)
        """

    async def delete_stack(
        self,
        *,
        StackName: str,
        RetainResources: Sequence[str] = ...,
        RoleARN: str = ...,
        ClientRequestToken: str = ...,
        DeletionMode: DeletionModeType = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#delete_stack)
        """

    async def delete_stack_instances(
        self,
        *,
        StackSetName: str,
        Regions: Sequence[str],
        RetainStacks: bool,
        Accounts: Sequence[str] = ...,
        DeploymentTargets: DeploymentTargetsUnionTypeDef = ...,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        OperationId: str = ...,
        CallAs: CallAsType = ...,
    ) -> DeleteStackInstancesOutputTypeDef:
        """
        Deletes stack instances for the specified accounts, in the specified Amazon Web
        Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#delete_stack_instances)
        """

    async def delete_stack_set(
        self, *, StackSetName: str, CallAs: CallAsType = ...
    ) -> Dict[str, Any]:
        """
        Deletes a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.delete_stack_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#delete_stack_set)
        """

    async def deregister_type(
        self,
        *,
        Arn: str = ...,
        Type: RegistryTypeType = ...,
        TypeName: str = ...,
        VersionId: str = ...,
    ) -> Dict[str, Any]:
        """
        Marks an extension or extension version as `DEPRECATED` in the CloudFormation
        registry, removing it from active
        use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.deregister_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#deregister_type)
        """

    async def describe_account_limits(
        self, *, NextToken: str = ...
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Retrieves your account's CloudFormation limits, such as the maximum number of
        stacks that you can create in your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_account_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_account_limits)
        """

    async def describe_change_set(
        self,
        *,
        ChangeSetName: str,
        StackName: str = ...,
        NextToken: str = ...,
        IncludePropertyValues: bool = ...,
    ) -> DescribeChangeSetOutputTypeDef:
        """
        Returns the inputs for the change set and a list of changes that CloudFormation
        will make if you execute the change
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_change_set)
        """

    async def describe_change_set_hooks(
        self,
        *,
        ChangeSetName: str,
        StackName: str = ...,
        NextToken: str = ...,
        LogicalResourceId: str = ...,
    ) -> DescribeChangeSetHooksOutputTypeDef:
        """
        Returns hook-related information for the change set and a list of changes that
        CloudFormation makes when you run the change
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_change_set_hooks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_change_set_hooks)
        """

    async def describe_generated_template(
        self, *, GeneratedTemplateName: str
    ) -> DescribeGeneratedTemplateOutputTypeDef:
        """
        Describes a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_generated_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_generated_template)
        """

    async def describe_organizations_access(
        self, *, CallAs: CallAsType = ...
    ) -> DescribeOrganizationsAccessOutputTypeDef:
        """
        Retrieves information about the account's `OrganizationAccess` status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_organizations_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_organizations_access)
        """

    async def describe_publisher(self, *, PublisherId: str = ...) -> DescribePublisherOutputTypeDef:
        """
        Returns information about a CloudFormation extension publisher.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_publisher)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_publisher)
        """

    async def describe_resource_scan(
        self, *, ResourceScanId: str
    ) -> DescribeResourceScanOutputTypeDef:
        """
        Describes details of a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_resource_scan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_resource_scan)
        """

    async def describe_stack_drift_detection_status(
        self, *, StackDriftDetectionId: str
    ) -> DescribeStackDriftDetectionStatusOutputTypeDef:
        """
        Returns information about a stack drift detection operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_drift_detection_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_drift_detection_status)
        """

    async def describe_stack_events(
        self, *, StackName: str = ..., NextToken: str = ...
    ) -> DescribeStackEventsOutputTypeDef:
        """
        Returns all stack related events for a specified stack in reverse chronological
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_events)
        """

    async def describe_stack_instance(
        self,
        *,
        StackSetName: str,
        StackInstanceAccount: str,
        StackInstanceRegion: str,
        CallAs: CallAsType = ...,
    ) -> DescribeStackInstanceOutputTypeDef:
        """
        Returns the stack instance that's associated with the specified StackSet,
        Amazon Web Services account, and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_instance)
        """

    async def describe_stack_resource(
        self, *, StackName: str, LogicalResourceId: str
    ) -> DescribeStackResourceOutputTypeDef:
        """
        Returns a description of the specified resource in the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_resource)
        """

    async def describe_stack_resource_drifts(
        self,
        *,
        StackName: str,
        StackResourceDriftStatusFilters: Sequence[StackResourceDriftStatusType] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> DescribeStackResourceDriftsOutputTypeDef:
        """
        Returns drift information for the resources that have been checked for drift in
        the specified
        stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resource_drifts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_resource_drifts)
        """

    async def describe_stack_resources(
        self, *, StackName: str = ..., LogicalResourceId: str = ..., PhysicalResourceId: str = ...
    ) -> DescribeStackResourcesOutputTypeDef:
        """
        Returns Amazon Web Services resource descriptions for running and deleted
        stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_resources)
        """

    async def describe_stack_set(
        self, *, StackSetName: str, CallAs: CallAsType = ...
    ) -> DescribeStackSetOutputTypeDef:
        """
        Returns the description of the specified StackSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_set)
        """

    async def describe_stack_set_operation(
        self, *, StackSetName: str, OperationId: str, CallAs: CallAsType = ...
    ) -> DescribeStackSetOperationOutputTypeDef:
        """
        Returns the description of the specified StackSet operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stack_set_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stack_set_operation)
        """

    async def describe_stacks(
        self, *, StackName: str = ..., NextToken: str = ...
    ) -> DescribeStacksOutputTypeDef:
        """
        Returns the description for the specified stack; if no stack name was
        specified, then it returns the description for all the stacks
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_stacks)
        """

    async def describe_type(
        self,
        *,
        Type: RegistryTypeType = ...,
        TypeName: str = ...,
        Arn: str = ...,
        VersionId: str = ...,
        PublisherId: str = ...,
        PublicVersionNumber: str = ...,
    ) -> DescribeTypeOutputTypeDef:
        """
        Returns detailed information about an extension that has been registered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_type)
        """

    async def describe_type_registration(
        self, *, RegistrationToken: str
    ) -> DescribeTypeRegistrationOutputTypeDef:
        """
        Returns information about an extension's registration, including its current
        status and type and version
        identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_type_registration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#describe_type_registration)
        """

    async def detect_stack_drift(
        self, *, StackName: str, LogicalResourceIds: Sequence[str] = ...
    ) -> DetectStackDriftOutputTypeDef:
        """
        Detects whether a stack's actual configuration differs, or has *drifted*, from
        its expected configuration, as defined in the stack template and any values
        specified as template
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_drift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#detect_stack_drift)
        """

    async def detect_stack_resource_drift(
        self, *, StackName: str, LogicalResourceId: str
    ) -> DetectStackResourceDriftOutputTypeDef:
        """
        Returns information about whether a resource's actual configuration differs, or
        has *drifted*, from its expected configuration, as defined in the stack
        template and any values specified as template
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_resource_drift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#detect_stack_resource_drift)
        """

    async def detect_stack_set_drift(
        self,
        *,
        StackSetName: str,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        OperationId: str = ...,
        CallAs: CallAsType = ...,
    ) -> DetectStackSetDriftOutputTypeDef:
        """
        Detect drift on a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.detect_stack_set_drift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#detect_stack_set_drift)
        """

    async def estimate_template_cost(
        self,
        *,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
    ) -> EstimateTemplateCostOutputTypeDef:
        """
        Returns the estimated monthly cost of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.estimate_template_cost)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#estimate_template_cost)
        """

    async def execute_change_set(
        self,
        *,
        ChangeSetName: str,
        StackName: str = ...,
        ClientRequestToken: str = ...,
        DisableRollback: bool = ...,
        RetainExceptOnCreate: bool = ...,
    ) -> Dict[str, Any]:
        """
        Updates a stack using the input information that was provided when the
        specified change set was
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.execute_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#execute_change_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#generate_presigned_url)
        """

    async def get_generated_template(
        self, *, GeneratedTemplateName: str, Format: TemplateFormatType = ...
    ) -> GetGeneratedTemplateOutputTypeDef:
        """
        Retrieves a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_generated_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_generated_template)
        """

    async def get_stack_policy(self, *, StackName: str) -> GetStackPolicyOutputTypeDef:
        """
        Returns the stack policy for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_stack_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_stack_policy)
        """

    async def get_template(
        self,
        *,
        StackName: str = ...,
        ChangeSetName: str = ...,
        TemplateStage: TemplateStageType = ...,
    ) -> GetTemplateOutputTypeDef:
        """
        Returns the template body for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_template)
        """

    async def get_template_summary(
        self,
        *,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        StackName: str = ...,
        StackSetName: str = ...,
        CallAs: CallAsType = ...,
        TemplateSummaryConfig: TemplateSummaryConfigTypeDef = ...,
    ) -> GetTemplateSummaryOutputTypeDef:
        """
        Returns information about a new or existing template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_template_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_template_summary)
        """

    async def import_stacks_to_stack_set(
        self,
        *,
        StackSetName: str,
        StackIds: Sequence[str] = ...,
        StackIdsUrl: str = ...,
        OrganizationalUnitIds: Sequence[str] = ...,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        OperationId: str = ...,
        CallAs: CallAsType = ...,
    ) -> ImportStacksToStackSetOutputTypeDef:
        """
        Import existing stacks into a new stack sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.import_stacks_to_stack_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#import_stacks_to_stack_set)
        """

    async def list_change_sets(
        self, *, StackName: str, NextToken: str = ...
    ) -> ListChangeSetsOutputTypeDef:
        """
        Returns the ID and status of each active change set for a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_change_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_change_sets)
        """

    async def list_exports(self, *, NextToken: str = ...) -> ListExportsOutputTypeDef:
        """
        Lists all exported output values in the account and Region in which you call
        this
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_exports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_exports)
        """

    async def list_generated_templates(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGeneratedTemplatesOutputTypeDef:
        """
        Lists your generated templates in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_generated_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_generated_templates)
        """

    async def list_imports(
        self, *, ExportName: str, NextToken: str = ...
    ) -> ListImportsOutputTypeDef:
        """
        Lists all stacks that are importing an exported output value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_imports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_imports)
        """

    async def list_resource_scan_related_resources(
        self,
        *,
        ResourceScanId: str,
        Resources: Sequence[ScannedResourceIdentifierTypeDef],
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListResourceScanRelatedResourcesOutputTypeDef:
        """
        Lists the related resources for a list of resources from a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scan_related_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_resource_scan_related_resources)
        """

    async def list_resource_scan_resources(
        self,
        *,
        ResourceScanId: str,
        ResourceIdentifier: str = ...,
        ResourceTypePrefix: str = ...,
        TagKey: str = ...,
        TagValue: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListResourceScanResourcesOutputTypeDef:
        """
        Lists the resources from a resource scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scan_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_resource_scan_resources)
        """

    async def list_resource_scans(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListResourceScansOutputTypeDef:
        """
        List the resource scans from newest to oldest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_resource_scans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_resource_scans)
        """

    async def list_stack_instance_resource_drifts(
        self,
        *,
        StackSetName: str,
        StackInstanceAccount: str,
        StackInstanceRegion: str,
        OperationId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        StackInstanceResourceDriftStatuses: Sequence[StackResourceDriftStatusType] = ...,
        CallAs: CallAsType = ...,
    ) -> ListStackInstanceResourceDriftsOutputTypeDef:
        """
        Returns drift information for resources in a stack instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_instance_resource_drifts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_instance_resource_drifts)
        """

    async def list_stack_instances(
        self,
        *,
        StackSetName: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[StackInstanceFilterTypeDef] = ...,
        StackInstanceAccount: str = ...,
        StackInstanceRegion: str = ...,
        CallAs: CallAsType = ...,
    ) -> ListStackInstancesOutputTypeDef:
        """
        Returns summary information about stack instances that are associated with the
        specified stack
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_instances)
        """

    async def list_stack_resources(
        self, *, StackName: str, NextToken: str = ...
    ) -> ListStackResourcesOutputTypeDef:
        """
        Returns descriptions of all resources of the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_resources)
        """

    async def list_stack_set_auto_deployment_targets(
        self,
        *,
        StackSetName: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        CallAs: CallAsType = ...,
    ) -> ListStackSetAutoDeploymentTargetsOutputTypeDef:
        """
        Returns summary information about deployment targets for a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_auto_deployment_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_set_auto_deployment_targets)
        """

    async def list_stack_set_operation_results(
        self,
        *,
        StackSetName: str,
        OperationId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        CallAs: CallAsType = ...,
        Filters: Sequence[OperationResultFilterTypeDef] = ...,
    ) -> ListStackSetOperationResultsOutputTypeDef:
        """
        Returns summary information about the results of a stack set operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_operation_results)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_set_operation_results)
        """

    async def list_stack_set_operations(
        self,
        *,
        StackSetName: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        CallAs: CallAsType = ...,
    ) -> ListStackSetOperationsOutputTypeDef:
        """
        Returns summary information about operations performed on a stack set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_set_operations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_set_operations)
        """

    async def list_stack_sets(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: StackSetStatusType = ...,
        CallAs: CallAsType = ...,
    ) -> ListStackSetsOutputTypeDef:
        """
        Returns summary information about stack sets that are associated with the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stack_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stack_sets)
        """

    async def list_stacks(
        self, *, NextToken: str = ..., StackStatusFilter: Sequence[StackStatusType] = ...
    ) -> ListStacksOutputTypeDef:
        """
        Returns the summary information for stacks whose status matches the specified
        StackStatusFilter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stacks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_stacks)
        """

    async def list_type_registrations(
        self,
        *,
        Type: RegistryTypeType = ...,
        TypeName: str = ...,
        TypeArn: str = ...,
        RegistrationStatusFilter: RegistrationStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListTypeRegistrationsOutputTypeDef:
        """
        Returns a list of registration tokens for the specified extension(s).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_type_registrations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_type_registrations)
        """

    async def list_type_versions(
        self,
        *,
        Type: RegistryTypeType = ...,
        TypeName: str = ...,
        Arn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        DeprecatedStatus: DeprecatedStatusType = ...,
        PublisherId: str = ...,
    ) -> ListTypeVersionsOutputTypeDef:
        """
        Returns summary information about the versions of an extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_type_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_type_versions)
        """

    async def list_types(
        self,
        *,
        Visibility: VisibilityType = ...,
        ProvisioningType: ProvisioningTypeType = ...,
        DeprecatedStatus: DeprecatedStatusType = ...,
        Type: RegistryTypeType = ...,
        Filters: TypeFiltersTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListTypesOutputTypeDef:
        """
        Returns summary information about extension that have been registered with
        CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#list_types)
        """

    async def publish_type(
        self,
        *,
        Type: ThirdPartyTypeType = ...,
        Arn: str = ...,
        TypeName: str = ...,
        PublicVersionNumber: str = ...,
    ) -> PublishTypeOutputTypeDef:
        """
        Publishes the specified extension to the CloudFormation registry as a public
        extension in this
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.publish_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#publish_type)
        """

    async def record_handler_progress(
        self,
        *,
        BearerToken: str,
        OperationStatus: OperationStatusType,
        CurrentOperationStatus: OperationStatusType = ...,
        StatusMessage: str = ...,
        ErrorCode: HandlerErrorCodeType = ...,
        ResourceModel: str = ...,
        ClientRequestToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Reports progress of a resource handler to CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.record_handler_progress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#record_handler_progress)
        """

    async def register_publisher(
        self, *, AcceptTermsAndConditions: bool = ..., ConnectionArn: str = ...
    ) -> RegisterPublisherOutputTypeDef:
        """
        Registers your account as a publisher of public extensions in the
        CloudFormation
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.register_publisher)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#register_publisher)
        """

    async def register_type(
        self,
        *,
        TypeName: str,
        SchemaHandlerPackage: str,
        Type: RegistryTypeType = ...,
        LoggingConfig: LoggingConfigTypeDef = ...,
        ExecutionRoleArn: str = ...,
        ClientRequestToken: str = ...,
    ) -> RegisterTypeOutputTypeDef:
        """
        Registers an extension with the CloudFormation service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.register_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#register_type)
        """

    async def rollback_stack(
        self,
        *,
        StackName: str,
        RoleARN: str = ...,
        ClientRequestToken: str = ...,
        RetainExceptOnCreate: bool = ...,
    ) -> RollbackStackOutputTypeDef:
        """
        When specifying `RollbackStack`, you preserve the state of previously
        provisioned resources when an operation
        fails.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.rollback_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#rollback_stack)
        """

    async def set_stack_policy(
        self, *, StackName: str, StackPolicyBody: str = ..., StackPolicyURL: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a stack policy for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_stack_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#set_stack_policy)
        """

    async def set_type_configuration(
        self,
        *,
        Configuration: str,
        TypeArn: str = ...,
        ConfigurationAlias: str = ...,
        TypeName: str = ...,
        Type: ThirdPartyTypeType = ...,
    ) -> SetTypeConfigurationOutputTypeDef:
        """
        Specifies the configuration data for a registered CloudFormation extension, in
        the given account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_type_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#set_type_configuration)
        """

    async def set_type_default_version(
        self,
        *,
        Arn: str = ...,
        Type: RegistryTypeType = ...,
        TypeName: str = ...,
        VersionId: str = ...,
    ) -> Dict[str, Any]:
        """
        Specify the default version of an extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.set_type_default_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#set_type_default_version)
        """

    async def signal_resource(
        self,
        *,
        StackName: str,
        LogicalResourceId: str,
        UniqueId: str,
        Status: ResourceSignalStatusType,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a signal to the specified resource with a success or failure status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.signal_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#signal_resource)
        """

    async def start_resource_scan(
        self, *, ClientRequestToken: str = ...
    ) -> StartResourceScanOutputTypeDef:
        """
        Starts a scan of the resources in this account in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.start_resource_scan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#start_resource_scan)
        """

    async def stop_stack_set_operation(
        self, *, StackSetName: str, OperationId: str, CallAs: CallAsType = ...
    ) -> Dict[str, Any]:
        """
        Stops an in-progress operation on a stack set and its associated stack
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.stop_stack_set_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#stop_stack_set_operation)
        """

    async def test_type(
        self,
        *,
        Arn: str = ...,
        Type: ThirdPartyTypeType = ...,
        TypeName: str = ...,
        VersionId: str = ...,
        LogDeliveryBucket: str = ...,
    ) -> TestTypeOutputTypeDef:
        """
        Tests a registered extension to make sure it meets all necessary requirements
        for being published in the CloudFormation
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.test_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#test_type)
        """

    async def update_generated_template(
        self,
        *,
        GeneratedTemplateName: str,
        NewGeneratedTemplateName: str = ...,
        AddResources: Sequence[ResourceDefinitionTypeDef] = ...,
        RemoveResources: Sequence[str] = ...,
        RefreshAllResources: bool = ...,
        TemplateConfiguration: TemplateConfigurationTypeDef = ...,
    ) -> UpdateGeneratedTemplateOutputTypeDef:
        """
        Updates a generated template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_generated_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#update_generated_template)
        """

    async def update_stack(
        self,
        *,
        StackName: str,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        UsePreviousTemplate: bool = ...,
        StackPolicyDuringUpdateBody: str = ...,
        StackPolicyDuringUpdateURL: str = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
        Capabilities: Sequence[CapabilityType] = ...,
        ResourceTypes: Sequence[str] = ...,
        RoleARN: str = ...,
        RollbackConfiguration: RollbackConfigurationUnionTypeDef = ...,
        StackPolicyBody: str = ...,
        StackPolicyURL: str = ...,
        NotificationARNs: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        DisableRollback: bool = ...,
        ClientRequestToken: str = ...,
        RetainExceptOnCreate: bool = ...,
    ) -> UpdateStackOutputTypeDef:
        """
        Updates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#update_stack)
        """

    async def update_stack_instances(
        self,
        *,
        StackSetName: str,
        Regions: Sequence[str],
        Accounts: Sequence[str] = ...,
        DeploymentTargets: DeploymentTargetsUnionTypeDef = ...,
        ParameterOverrides: Sequence[ParameterTypeDef] = ...,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        OperationId: str = ...,
        CallAs: CallAsType = ...,
    ) -> UpdateStackInstancesOutputTypeDef:
        """
        Updates the parameter values for stack instances for the specified accounts,
        within the specified Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#update_stack_instances)
        """

    async def update_stack_set(
        self,
        *,
        StackSetName: str,
        Description: str = ...,
        TemplateBody: str = ...,
        TemplateURL: str = ...,
        UsePreviousTemplate: bool = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
        Capabilities: Sequence[CapabilityType] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        OperationPreferences: StackSetOperationPreferencesUnionTypeDef = ...,
        AdministrationRoleARN: str = ...,
        ExecutionRoleName: str = ...,
        DeploymentTargets: DeploymentTargetsUnionTypeDef = ...,
        PermissionModel: PermissionModelsType = ...,
        AutoDeployment: AutoDeploymentTypeDef = ...,
        OperationId: str = ...,
        Accounts: Sequence[str] = ...,
        Regions: Sequence[str] = ...,
        CallAs: CallAsType = ...,
        ManagedExecution: ManagedExecutionTypeDef = ...,
    ) -> UpdateStackSetOutputTypeDef:
        """
        Updates the stack set, and associated stack instances in the specified accounts
        and Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#update_stack_set)
        """

    async def update_termination_protection(
        self, *, EnableTerminationProtection: bool, StackName: str
    ) -> UpdateTerminationProtectionOutputTypeDef:
        """
        Updates termination protection for the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.update_termination_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#update_termination_protection)
        """

    async def validate_template(
        self, *, TemplateBody: str = ..., TemplateURL: str = ...
    ) -> ValidateTemplateOutputTypeDef:
        """
        Validates a specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.validate_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#validate_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_change_set"]
    ) -> DescribeChangeSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_stack_events"]
    ) -> DescribeStackEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stacks"]) -> DescribeStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_change_sets"]) -> ListChangeSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exports"]) -> ListExportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_generated_templates"]
    ) -> ListGeneratedTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_imports"]) -> ListImportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scan_related_resources"]
    ) -> ListResourceScanRelatedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scan_resources"]
    ) -> ListResourceScanResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_scans"]
    ) -> ListResourceScansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_instances"]
    ) -> ListStackInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_resources"]
    ) -> ListStackResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_set_operation_results"]
    ) -> ListStackSetOperationResultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stack_set_operations"]
    ) -> ListStackSetOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stack_sets"]) -> ListStackSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stacks"]) -> ListStacksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_types"]) -> ListTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["change_set_create_complete"]
    ) -> ChangeSetCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_create_complete"]
    ) -> StackCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_delete_complete"]
    ) -> StackDeleteCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stack_exists"]) -> StackExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_import_complete"]
    ) -> StackImportCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_rollback_complete"]
    ) -> StackRollbackCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["stack_update_complete"]
    ) -> StackUpdateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["type_registration_complete"]
    ) -> TypeRegistrationCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/#get_waiter)
        """

    async def __aenter__(self) -> "CloudFormationClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/client/)
        """
