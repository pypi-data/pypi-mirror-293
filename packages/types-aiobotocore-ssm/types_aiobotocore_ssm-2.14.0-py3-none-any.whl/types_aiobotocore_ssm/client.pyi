"""
Type annotations for ssm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm.client import SSMClient

    session = get_session()
    async with session.create_client("ssm") as client:
        client: SSMClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AssociationComplianceSeverityType,
    AssociationSyncComplianceType,
    ComplianceUploadTypeType,
    DocumentFormatType,
    DocumentHashTypeType,
    DocumentTypeType,
    ExecutionModeType,
    InventorySchemaDeleteOptionType,
    MaintenanceWindowResourceTypeType,
    MaintenanceWindowTaskCutoffBehaviorType,
    MaintenanceWindowTaskTypeType,
    OperatingSystemType,
    OpsItemStatusType,
    ParameterTierType,
    ParameterTypeType,
    PatchActionType,
    PatchComplianceLevelType,
    PatchPropertyType,
    PatchSetType,
    ResourceTypeForTaggingType,
    SessionStateType,
    SignalTypeType,
    StopTypeType,
)
from .paginator import (
    DescribeActivationsPaginator,
    DescribeAssociationExecutionsPaginator,
    DescribeAssociationExecutionTargetsPaginator,
    DescribeAutomationExecutionsPaginator,
    DescribeAutomationStepExecutionsPaginator,
    DescribeAvailablePatchesPaginator,
    DescribeEffectiveInstanceAssociationsPaginator,
    DescribeEffectivePatchesForPatchBaselinePaginator,
    DescribeInstanceAssociationsStatusPaginator,
    DescribeInstanceInformationPaginator,
    DescribeInstancePatchesPaginator,
    DescribeInstancePatchStatesForPatchGroupPaginator,
    DescribeInstancePatchStatesPaginator,
    DescribeInstancePropertiesPaginator,
    DescribeInventoryDeletionsPaginator,
    DescribeMaintenanceWindowExecutionsPaginator,
    DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
    DescribeMaintenanceWindowExecutionTasksPaginator,
    DescribeMaintenanceWindowSchedulePaginator,
    DescribeMaintenanceWindowsForTargetPaginator,
    DescribeMaintenanceWindowsPaginator,
    DescribeMaintenanceWindowTargetsPaginator,
    DescribeMaintenanceWindowTasksPaginator,
    DescribeOpsItemsPaginator,
    DescribeParametersPaginator,
    DescribePatchBaselinesPaginator,
    DescribePatchGroupsPaginator,
    DescribePatchPropertiesPaginator,
    DescribeSessionsPaginator,
    GetInventoryPaginator,
    GetInventorySchemaPaginator,
    GetOpsSummaryPaginator,
    GetParameterHistoryPaginator,
    GetParametersByPathPaginator,
    GetResourcePoliciesPaginator,
    ListAssociationsPaginator,
    ListAssociationVersionsPaginator,
    ListCommandInvocationsPaginator,
    ListCommandsPaginator,
    ListComplianceItemsPaginator,
    ListComplianceSummariesPaginator,
    ListDocumentsPaginator,
    ListDocumentVersionsPaginator,
    ListOpsItemEventsPaginator,
    ListOpsItemRelatedItemsPaginator,
    ListOpsMetadataPaginator,
    ListResourceComplianceSummariesPaginator,
    ListResourceDataSyncPaginator,
)
from .type_defs import (
    AlarmConfigurationUnionTypeDef,
    AssociateOpsItemRelatedItemResponseTypeDef,
    AssociationExecutionFilterTypeDef,
    AssociationExecutionTargetsFilterTypeDef,
    AssociationFilterTypeDef,
    AssociationStatusUnionTypeDef,
    AttachmentsSourceTypeDef,
    AutomationExecutionFilterTypeDef,
    BaselineOverrideTypeDef,
    CancelMaintenanceWindowExecutionResultTypeDef,
    CloudWatchOutputConfigTypeDef,
    CommandFilterTypeDef,
    ComplianceExecutionSummaryUnionTypeDef,
    ComplianceItemEntryTypeDef,
    ComplianceStringFilterTypeDef,
    CreateActivationResultTypeDef,
    CreateAssociationBatchRequestEntryUnionTypeDef,
    CreateAssociationBatchResultTypeDef,
    CreateAssociationResultTypeDef,
    CreateDocumentResultTypeDef,
    CreateMaintenanceWindowResultTypeDef,
    CreateOpsItemResponseTypeDef,
    CreateOpsMetadataResultTypeDef,
    CreatePatchBaselineResultTypeDef,
    DeleteInventoryResultTypeDef,
    DeleteMaintenanceWindowResultTypeDef,
    DeleteParametersResultTypeDef,
    DeletePatchBaselineResultTypeDef,
    DeregisterPatchBaselineForPatchGroupResultTypeDef,
    DeregisterTargetFromMaintenanceWindowResultTypeDef,
    DeregisterTaskFromMaintenanceWindowResultTypeDef,
    DescribeActivationsFilterTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAssociationResultTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeDocumentPermissionResponseTypeDef,
    DescribeDocumentResultTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInstancePropertiesResultTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchGroupStateResultTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsResponseTypeDef,
    DocumentFilterTypeDef,
    DocumentKeyValuesFilterTypeDef,
    DocumentRequiresTypeDef,
    DocumentReviewsTypeDef,
    GetAutomationExecutionResultTypeDef,
    GetCalendarStateResponseTypeDef,
    GetCommandInvocationResultTypeDef,
    GetConnectionStatusResponseTypeDef,
    GetDefaultPatchBaselineResultTypeDef,
    GetDeployablePatchSnapshotForInstanceResultTypeDef,
    GetDocumentResultTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaResultTypeDef,
    GetMaintenanceWindowExecutionResultTypeDef,
    GetMaintenanceWindowExecutionTaskInvocationResultTypeDef,
    GetMaintenanceWindowExecutionTaskResultTypeDef,
    GetMaintenanceWindowResultTypeDef,
    GetMaintenanceWindowTaskResultTypeDef,
    GetOpsItemResponseTypeDef,
    GetOpsMetadataResultTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParameterResultTypeDef,
    GetParametersByPathResultTypeDef,
    GetParametersResultTypeDef,
    GetPatchBaselineForPatchGroupResultTypeDef,
    GetPatchBaselineResultTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetServiceSettingResultTypeDef,
    InstanceAssociationOutputLocationTypeDef,
    InstanceInformationFilterTypeDef,
    InstanceInformationStringFilterTypeDef,
    InstancePatchStateFilterTypeDef,
    InstancePropertyFilterTypeDef,
    InstancePropertyStringFilterTypeDef,
    InventoryAggregatorTypeDef,
    InventoryFilterTypeDef,
    InventoryItemTypeDef,
    LabelParameterVersionResultTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentMetadataHistoryResponseTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListInventoryEntriesResultTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncResultTypeDef,
    ListTagsForResourceResultTypeDef,
    LoggingInfoTypeDef,
    MaintenanceWindowFilterTypeDef,
    MaintenanceWindowTaskInvocationParametersUnionTypeDef,
    MaintenanceWindowTaskParameterValueExpressionUnionTypeDef,
    MetadataValueTypeDef,
    NotificationConfigUnionTypeDef,
    OpsAggregatorTypeDef,
    OpsFilterTypeDef,
    OpsItemDataValueTypeDef,
    OpsItemEventFilterTypeDef,
    OpsItemFilterTypeDef,
    OpsItemNotificationTypeDef,
    OpsItemRelatedItemsFilterTypeDef,
    OpsMetadataFilterTypeDef,
    OpsResultAttributeTypeDef,
    ParametersFilterTypeDef,
    ParameterStringFilterTypeDef,
    PatchFilterGroupUnionTypeDef,
    PatchOrchestratorFilterTypeDef,
    PatchRuleGroupUnionTypeDef,
    PatchSourceUnionTypeDef,
    PutInventoryResultTypeDef,
    PutParameterResultTypeDef,
    PutResourcePolicyResponseTypeDef,
    RegisterDefaultPatchBaselineResultTypeDef,
    RegisterPatchBaselineForPatchGroupResultTypeDef,
    RegisterTargetWithMaintenanceWindowResultTypeDef,
    RegisterTaskWithMaintenanceWindowResultTypeDef,
    RegistrationMetadataItemTypeDef,
    RelatedOpsItemTypeDef,
    ResetServiceSettingResultTypeDef,
    ResourceDataSyncS3DestinationTypeDef,
    ResourceDataSyncSourceTypeDef,
    ResultAttributeTypeDef,
    ResumeSessionResponseTypeDef,
    RunbookUnionTypeDef,
    SendCommandResultTypeDef,
    SessionFilterTypeDef,
    StartAutomationExecutionResultTypeDef,
    StartChangeRequestExecutionResultTypeDef,
    StartSessionResponseTypeDef,
    StepExecutionFilterTypeDef,
    TagTypeDef,
    TargetLocationUnionTypeDef,
    TargetUnionTypeDef,
    TerminateSessionResponseTypeDef,
    TimestampTypeDef,
    UnlabelParameterVersionResultTypeDef,
    UpdateAssociationResultTypeDef,
    UpdateAssociationStatusResultTypeDef,
    UpdateDocumentDefaultVersionResultTypeDef,
    UpdateDocumentResultTypeDef,
    UpdateMaintenanceWindowResultTypeDef,
    UpdateMaintenanceWindowTargetResultTypeDef,
    UpdateMaintenanceWindowTaskResultTypeDef,
    UpdateOpsMetadataResultTypeDef,
    UpdatePatchBaselineResultTypeDef,
)
from .waiter import CommandExecutedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SSMClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    AssociatedInstances: Type[BotocoreClientError]
    AssociationAlreadyExists: Type[BotocoreClientError]
    AssociationDoesNotExist: Type[BotocoreClientError]
    AssociationExecutionDoesNotExist: Type[BotocoreClientError]
    AssociationLimitExceeded: Type[BotocoreClientError]
    AssociationVersionLimitExceeded: Type[BotocoreClientError]
    AutomationDefinitionNotApprovedException: Type[BotocoreClientError]
    AutomationDefinitionNotFoundException: Type[BotocoreClientError]
    AutomationDefinitionVersionNotFoundException: Type[BotocoreClientError]
    AutomationExecutionLimitExceededException: Type[BotocoreClientError]
    AutomationExecutionNotFoundException: Type[BotocoreClientError]
    AutomationStepNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ComplianceTypeCountLimitExceededException: Type[BotocoreClientError]
    CustomSchemaCountLimitExceededException: Type[BotocoreClientError]
    DocumentAlreadyExists: Type[BotocoreClientError]
    DocumentLimitExceeded: Type[BotocoreClientError]
    DocumentPermissionLimit: Type[BotocoreClientError]
    DocumentVersionLimitExceeded: Type[BotocoreClientError]
    DoesNotExistException: Type[BotocoreClientError]
    DuplicateDocumentContent: Type[BotocoreClientError]
    DuplicateDocumentVersionName: Type[BotocoreClientError]
    DuplicateInstanceId: Type[BotocoreClientError]
    FeatureNotAvailableException: Type[BotocoreClientError]
    HierarchyLevelLimitExceededException: Type[BotocoreClientError]
    HierarchyTypeMismatchException: Type[BotocoreClientError]
    IdempotentParameterMismatch: Type[BotocoreClientError]
    IncompatiblePolicyException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidActivation: Type[BotocoreClientError]
    InvalidActivationId: Type[BotocoreClientError]
    InvalidAggregatorException: Type[BotocoreClientError]
    InvalidAllowedPatternException: Type[BotocoreClientError]
    InvalidAssociation: Type[BotocoreClientError]
    InvalidAssociationVersion: Type[BotocoreClientError]
    InvalidAutomationExecutionParametersException: Type[BotocoreClientError]
    InvalidAutomationSignalException: Type[BotocoreClientError]
    InvalidAutomationStatusUpdateException: Type[BotocoreClientError]
    InvalidCommandId: Type[BotocoreClientError]
    InvalidDeleteInventoryParametersException: Type[BotocoreClientError]
    InvalidDeletionIdException: Type[BotocoreClientError]
    InvalidDocument: Type[BotocoreClientError]
    InvalidDocumentContent: Type[BotocoreClientError]
    InvalidDocumentOperation: Type[BotocoreClientError]
    InvalidDocumentSchemaVersion: Type[BotocoreClientError]
    InvalidDocumentType: Type[BotocoreClientError]
    InvalidDocumentVersion: Type[BotocoreClientError]
    InvalidFilter: Type[BotocoreClientError]
    InvalidFilterKey: Type[BotocoreClientError]
    InvalidFilterOption: Type[BotocoreClientError]
    InvalidFilterValue: Type[BotocoreClientError]
    InvalidInstanceId: Type[BotocoreClientError]
    InvalidInstanceInformationFilterValue: Type[BotocoreClientError]
    InvalidInstancePropertyFilterValue: Type[BotocoreClientError]
    InvalidInventoryGroupException: Type[BotocoreClientError]
    InvalidInventoryItemContextException: Type[BotocoreClientError]
    InvalidInventoryRequestException: Type[BotocoreClientError]
    InvalidItemContentException: Type[BotocoreClientError]
    InvalidKeyId: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    InvalidNotificationConfig: Type[BotocoreClientError]
    InvalidOptionException: Type[BotocoreClientError]
    InvalidOutputFolder: Type[BotocoreClientError]
    InvalidOutputLocation: Type[BotocoreClientError]
    InvalidParameters: Type[BotocoreClientError]
    InvalidPermissionType: Type[BotocoreClientError]
    InvalidPluginName: Type[BotocoreClientError]
    InvalidPolicyAttributeException: Type[BotocoreClientError]
    InvalidPolicyTypeException: Type[BotocoreClientError]
    InvalidResourceId: Type[BotocoreClientError]
    InvalidResourceType: Type[BotocoreClientError]
    InvalidResultAttributeException: Type[BotocoreClientError]
    InvalidRole: Type[BotocoreClientError]
    InvalidSchedule: Type[BotocoreClientError]
    InvalidTag: Type[BotocoreClientError]
    InvalidTarget: Type[BotocoreClientError]
    InvalidTargetMaps: Type[BotocoreClientError]
    InvalidTypeNameException: Type[BotocoreClientError]
    InvalidUpdate: Type[BotocoreClientError]
    InvocationDoesNotExist: Type[BotocoreClientError]
    ItemContentMismatchException: Type[BotocoreClientError]
    ItemSizeLimitExceededException: Type[BotocoreClientError]
    MalformedResourcePolicyDocumentException: Type[BotocoreClientError]
    MaxDocumentSizeExceeded: Type[BotocoreClientError]
    OpsItemAccessDeniedException: Type[BotocoreClientError]
    OpsItemAlreadyExistsException: Type[BotocoreClientError]
    OpsItemConflictException: Type[BotocoreClientError]
    OpsItemInvalidParameterException: Type[BotocoreClientError]
    OpsItemLimitExceededException: Type[BotocoreClientError]
    OpsItemNotFoundException: Type[BotocoreClientError]
    OpsItemRelatedItemAlreadyExistsException: Type[BotocoreClientError]
    OpsItemRelatedItemAssociationNotFoundException: Type[BotocoreClientError]
    OpsMetadataAlreadyExistsException: Type[BotocoreClientError]
    OpsMetadataInvalidArgumentException: Type[BotocoreClientError]
    OpsMetadataKeyLimitExceededException: Type[BotocoreClientError]
    OpsMetadataLimitExceededException: Type[BotocoreClientError]
    OpsMetadataNotFoundException: Type[BotocoreClientError]
    OpsMetadataTooManyUpdatesException: Type[BotocoreClientError]
    ParameterAlreadyExists: Type[BotocoreClientError]
    ParameterLimitExceeded: Type[BotocoreClientError]
    ParameterMaxVersionLimitExceeded: Type[BotocoreClientError]
    ParameterNotFound: Type[BotocoreClientError]
    ParameterPatternMismatchException: Type[BotocoreClientError]
    ParameterVersionLabelLimitExceeded: Type[BotocoreClientError]
    ParameterVersionNotFound: Type[BotocoreClientError]
    PoliciesLimitExceededException: Type[BotocoreClientError]
    ResourceDataSyncAlreadyExistsException: Type[BotocoreClientError]
    ResourceDataSyncConflictException: Type[BotocoreClientError]
    ResourceDataSyncCountExceededException: Type[BotocoreClientError]
    ResourceDataSyncInvalidConfigurationException: Type[BotocoreClientError]
    ResourceDataSyncNotFoundException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourcePolicyConflictException: Type[BotocoreClientError]
    ResourcePolicyInvalidParameterException: Type[BotocoreClientError]
    ResourcePolicyLimitExceededException: Type[BotocoreClientError]
    ResourcePolicyNotFoundException: Type[BotocoreClientError]
    ServiceSettingNotFound: Type[BotocoreClientError]
    StatusUnchanged: Type[BotocoreClientError]
    SubTypeCountLimitExceededException: Type[BotocoreClientError]
    TargetInUseException: Type[BotocoreClientError]
    TargetNotConnected: Type[BotocoreClientError]
    TooManyTagsError: Type[BotocoreClientError]
    TooManyUpdates: Type[BotocoreClientError]
    TotalSizeLimitExceededException: Type[BotocoreClientError]
    UnsupportedCalendarException: Type[BotocoreClientError]
    UnsupportedFeatureRequiredException: Type[BotocoreClientError]
    UnsupportedInventoryItemContextException: Type[BotocoreClientError]
    UnsupportedInventorySchemaVersionException: Type[BotocoreClientError]
    UnsupportedOperatingSystem: Type[BotocoreClientError]
    UnsupportedParameterType: Type[BotocoreClientError]
    UnsupportedPlatformType: Type[BotocoreClientError]

class SSMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#exceptions)
        """

    async def add_tags_to_resource(
        self,
        *,
        ResourceType: ResourceTypeForTaggingType,
        ResourceId: str,
        Tags: Sequence[TagTypeDef],
    ) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.add_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#add_tags_to_resource)
        """

    async def associate_ops_item_related_item(
        self, *, OpsItemId: str, AssociationType: str, ResourceType: str, ResourceUri: str
    ) -> AssociateOpsItemRelatedItemResponseTypeDef:
        """
        Associates a related item to a Systems Manager OpsCenter OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.associate_ops_item_related_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#associate_ops_item_related_item)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#can_paginate)
        """

    async def cancel_command(
        self, *, CommandId: str, InstanceIds: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Attempts to cancel the command specified by the Command ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.cancel_command)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#cancel_command)
        """

    async def cancel_maintenance_window_execution(
        self, *, WindowExecutionId: str
    ) -> CancelMaintenanceWindowExecutionResultTypeDef:
        """
        Stops a maintenance window execution that is already in progress and cancels
        any tasks in the window that haven't already starting
        running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.cancel_maintenance_window_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#cancel_maintenance_window_execution)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#close)
        """

    async def create_activation(
        self,
        *,
        IamRole: str,
        Description: str = ...,
        DefaultInstanceName: str = ...,
        RegistrationLimit: int = ...,
        ExpirationDate: TimestampTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        RegistrationMetadata: Sequence[RegistrationMetadataItemTypeDef] = ...,
    ) -> CreateActivationResultTypeDef:
        """
        Generates an activation code and activation ID you can use to register your
        on-premises servers, edge devices, or virtual machine (VM) with Amazon Web
        Services Systems
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_activation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_activation)
        """

    async def create_association(
        self,
        *,
        Name: str,
        DocumentVersion: str = ...,
        InstanceId: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        ScheduleExpression: str = ...,
        OutputLocation: InstanceAssociationOutputLocationTypeDef = ...,
        AssociationName: str = ...,
        AutomationTargetParameterName: str = ...,
        MaxErrors: str = ...,
        MaxConcurrency: str = ...,
        ComplianceSeverity: AssociationComplianceSeverityType = ...,
        SyncCompliance: AssociationSyncComplianceType = ...,
        ApplyOnlyAtCronInterval: bool = ...,
        CalendarNames: Sequence[str] = ...,
        TargetLocations: Sequence[TargetLocationUnionTypeDef] = ...,
        ScheduleOffset: int = ...,
        Duration: int = ...,
        TargetMaps: Sequence[Mapping[str, Sequence[str]]] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> CreateAssociationResultTypeDef:
        """
        A State Manager association defines the state that you want to maintain on your
        managed
        nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_association)
        """

    async def create_association_batch(
        self, *, Entries: Sequence[CreateAssociationBatchRequestEntryUnionTypeDef]
    ) -> CreateAssociationBatchResultTypeDef:
        """
        Associates the specified Amazon Web Services Systems Manager document (SSM
        document) with the specified managed nodes or
        targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_association_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_association_batch)
        """

    async def create_document(
        self,
        *,
        Content: str,
        Name: str,
        Requires: Sequence[DocumentRequiresTypeDef] = ...,
        Attachments: Sequence[AttachmentsSourceTypeDef] = ...,
        DisplayName: str = ...,
        VersionName: str = ...,
        DocumentType: DocumentTypeType = ...,
        DocumentFormat: DocumentFormatType = ...,
        TargetType: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateDocumentResultTypeDef:
        """
        Creates a Amazon Web Services Systems Manager (SSM document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_document)
        """

    async def create_maintenance_window(
        self,
        *,
        Name: str,
        Schedule: str,
        Duration: int,
        Cutoff: int,
        AllowUnassociatedTargets: bool,
        Description: str = ...,
        StartDate: str = ...,
        EndDate: str = ...,
        ScheduleTimezone: str = ...,
        ScheduleOffset: int = ...,
        ClientToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateMaintenanceWindowResultTypeDef:
        """
        Creates a new maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_maintenance_window)
        """

    async def create_ops_item(
        self,
        *,
        Description: str,
        Source: str,
        Title: str,
        OpsItemType: str = ...,
        OperationalData: Mapping[str, OpsItemDataValueTypeDef] = ...,
        Notifications: Sequence[OpsItemNotificationTypeDef] = ...,
        Priority: int = ...,
        RelatedOpsItems: Sequence[RelatedOpsItemTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        Category: str = ...,
        Severity: str = ...,
        ActualStartTime: TimestampTypeDef = ...,
        ActualEndTime: TimestampTypeDef = ...,
        PlannedStartTime: TimestampTypeDef = ...,
        PlannedEndTime: TimestampTypeDef = ...,
        AccountId: str = ...,
    ) -> CreateOpsItemResponseTypeDef:
        """
        Creates a new OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_ops_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_ops_item)
        """

    async def create_ops_metadata(
        self,
        *,
        ResourceId: str,
        Metadata: Mapping[str, MetadataValueTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateOpsMetadataResultTypeDef:
        """
        If you create a new application in Application Manager, Amazon Web Services
        Systems Manager calls this API operation to specify information about the new
        application, including the application
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_ops_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_ops_metadata)
        """

    async def create_patch_baseline(
        self,
        *,
        Name: str,
        OperatingSystem: OperatingSystemType = ...,
        GlobalFilters: PatchFilterGroupUnionTypeDef = ...,
        ApprovalRules: PatchRuleGroupUnionTypeDef = ...,
        ApprovedPatches: Sequence[str] = ...,
        ApprovedPatchesComplianceLevel: PatchComplianceLevelType = ...,
        ApprovedPatchesEnableNonSecurity: bool = ...,
        RejectedPatches: Sequence[str] = ...,
        RejectedPatchesAction: PatchActionType = ...,
        Description: str = ...,
        Sources: Sequence[PatchSourceUnionTypeDef] = ...,
        ClientToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreatePatchBaselineResultTypeDef:
        """
        Creates a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_patch_baseline)
        """

    async def create_resource_data_sync(
        self,
        *,
        SyncName: str,
        S3Destination: ResourceDataSyncS3DestinationTypeDef = ...,
        SyncType: str = ...,
        SyncSource: ResourceDataSyncSourceTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        A resource data sync helps you view data from multiple sources in a single
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_resource_data_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#create_resource_data_sync)
        """

    async def delete_activation(self, *, ActivationId: str) -> Dict[str, Any]:
        """
        Deletes an activation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_activation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_activation)
        """

    async def delete_association(
        self, *, Name: str = ..., InstanceId: str = ..., AssociationId: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates the specified Amazon Web Services Systems Manager document (SSM
        document) from the specified managed
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_association)
        """

    async def delete_document(
        self, *, Name: str, DocumentVersion: str = ..., VersionName: str = ..., Force: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the Amazon Web Services Systems Manager document (SSM document) and all
        managed node associations to the
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_document)
        """

    async def delete_inventory(
        self,
        *,
        TypeName: str,
        SchemaDeleteOption: InventorySchemaDeleteOptionType = ...,
        DryRun: bool = ...,
        ClientToken: str = ...,
    ) -> DeleteInventoryResultTypeDef:
        """
        Delete a custom inventory type or the data associated with a custom Inventory
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_inventory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_inventory)
        """

    async def delete_maintenance_window(
        self, *, WindowId: str
    ) -> DeleteMaintenanceWindowResultTypeDef:
        """
        Deletes a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_maintenance_window)
        """

    async def delete_ops_item(self, *, OpsItemId: str) -> Dict[str, Any]:
        """
        Delete an OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_ops_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_ops_item)
        """

    async def delete_ops_metadata(self, *, OpsMetadataArn: str) -> Dict[str, Any]:
        """
        Delete OpsMetadata related to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_ops_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_ops_metadata)
        """

    async def delete_parameter(self, *, Name: str) -> Dict[str, Any]:
        """
        Delete a parameter from the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_parameter)
        """

    async def delete_parameters(self, *, Names: Sequence[str]) -> DeleteParametersResultTypeDef:
        """
        Delete a list of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_parameters)
        """

    async def delete_patch_baseline(self, *, BaselineId: str) -> DeletePatchBaselineResultTypeDef:
        """
        Deletes a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_patch_baseline)
        """

    async def delete_resource_data_sync(
        self, *, SyncName: str, SyncType: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a resource data sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_resource_data_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_resource_data_sync)
        """

    async def delete_resource_policy(
        self, *, ResourceArn: str, PolicyId: str, PolicyHash: str
    ) -> Dict[str, Any]:
        """
        Deletes a Systems Manager resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#delete_resource_policy)
        """

    async def deregister_managed_instance(self, *, InstanceId: str) -> Dict[str, Any]:
        """
        Removes the server or virtual machine from the list of registered servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.deregister_managed_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#deregister_managed_instance)
        """

    async def deregister_patch_baseline_for_patch_group(
        self, *, BaselineId: str, PatchGroup: str
    ) -> DeregisterPatchBaselineForPatchGroupResultTypeDef:
        """
        Removes a patch group from a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.deregister_patch_baseline_for_patch_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#deregister_patch_baseline_for_patch_group)
        """

    async def deregister_target_from_maintenance_window(
        self, *, WindowId: str, WindowTargetId: str, Safe: bool = ...
    ) -> DeregisterTargetFromMaintenanceWindowResultTypeDef:
        """
        Removes a target from a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.deregister_target_from_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#deregister_target_from_maintenance_window)
        """

    async def deregister_task_from_maintenance_window(
        self, *, WindowId: str, WindowTaskId: str
    ) -> DeregisterTaskFromMaintenanceWindowResultTypeDef:
        """
        Removes a task from a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.deregister_task_from_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#deregister_task_from_maintenance_window)
        """

    async def describe_activations(
        self,
        *,
        Filters: Sequence[DescribeActivationsFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeActivationsResultTypeDef:
        """
        Describes details about the activation, such as the date and time the
        activation was created, its expiration date, the Identity and Access Management
        (IAM) role assigned to the managed nodes in the activation, and the number of
        nodes registered by using this
        activation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_activations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_activations)
        """

    async def describe_association(
        self,
        *,
        Name: str = ...,
        InstanceId: str = ...,
        AssociationId: str = ...,
        AssociationVersion: str = ...,
    ) -> DescribeAssociationResultTypeDef:
        """
        Describes the association for the specified target or managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_association)
        """

    async def describe_association_execution_targets(
        self,
        *,
        AssociationId: str,
        ExecutionId: str,
        Filters: Sequence[AssociationExecutionTargetsFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAssociationExecutionTargetsResultTypeDef:
        """
        Views information about a specific execution of a specific association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_association_execution_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_association_execution_targets)
        """

    async def describe_association_executions(
        self,
        *,
        AssociationId: str,
        Filters: Sequence[AssociationExecutionFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAssociationExecutionsResultTypeDef:
        """
        Views all executions for a specific association ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_association_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_association_executions)
        """

    async def describe_automation_executions(
        self,
        *,
        Filters: Sequence[AutomationExecutionFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAutomationExecutionsResultTypeDef:
        """
        Provides details about all active and terminated Automation executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_automation_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_automation_executions)
        """

    async def describe_automation_step_executions(
        self,
        *,
        AutomationExecutionId: str,
        Filters: Sequence[StepExecutionFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ReverseOrder: bool = ...,
    ) -> DescribeAutomationStepExecutionsResultTypeDef:
        """
        Information about all active and terminated step executions in an Automation
        workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_automation_step_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_automation_step_executions)
        """

    async def describe_available_patches(
        self,
        *,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeAvailablePatchesResultTypeDef:
        """
        Lists all patches eligible to be included in a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_available_patches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_available_patches)
        """

    async def describe_document(
        self, *, Name: str, DocumentVersion: str = ..., VersionName: str = ...
    ) -> DescribeDocumentResultTypeDef:
        """
        Describes the specified Amazon Web Services Systems Manager document (SSM
        document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_document)
        """

    async def describe_document_permission(
        self,
        *,
        Name: str,
        PermissionType: Literal["Share"],
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeDocumentPermissionResponseTypeDef:
        """
        Describes the permissions for a Amazon Web Services Systems Manager document
        (SSM
        document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_document_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_document_permission)
        """

    async def describe_effective_instance_associations(
        self, *, InstanceId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeEffectiveInstanceAssociationsResultTypeDef:
        """
        All associations for the managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_effective_instance_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_effective_instance_associations)
        """

    async def describe_effective_patches_for_patch_baseline(
        self, *, BaselineId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeEffectivePatchesForPatchBaselineResultTypeDef:
        """
        Retrieves the current effective patches (the patch and the approval state) for
        the specified patch
        baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_effective_patches_for_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_effective_patches_for_patch_baseline)
        """

    async def describe_instance_associations_status(
        self, *, InstanceId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeInstanceAssociationsStatusResultTypeDef:
        """
        The status of the associations for the managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_associations_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_associations_status)
        """

    async def describe_instance_information(
        self,
        *,
        InstanceInformationFilterList: Sequence[InstanceInformationFilterTypeDef] = ...,
        Filters: Sequence[InstanceInformationStringFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeInstanceInformationResultTypeDef:
        """
        Provides information about one or more of your managed nodes, including the
        operating system platform, SSM Agent version, association status, and IP
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_information)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_information)
        """

    async def describe_instance_patch_states(
        self, *, InstanceIds: Sequence[str], NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeInstancePatchStatesResultTypeDef:
        """
        Retrieves the high-level patch state of one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_patch_states)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_patch_states)
        """

    async def describe_instance_patch_states_for_patch_group(
        self,
        *,
        PatchGroup: str,
        Filters: Sequence[InstancePatchStateFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> DescribeInstancePatchStatesForPatchGroupResultTypeDef:
        """
        Retrieves the high-level patch state for the managed nodes in the specified
        patch
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_patch_states_for_patch_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_patch_states_for_patch_group)
        """

    async def describe_instance_patches(
        self,
        *,
        InstanceId: str,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> DescribeInstancePatchesResultTypeDef:
        """
        Retrieves information about the patches on the specified managed node and their
        state relative to the patch baseline being used for the
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_patches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_patches)
        """

    async def describe_instance_properties(
        self,
        *,
        InstancePropertyFilterList: Sequence[InstancePropertyFilterTypeDef] = ...,
        FiltersWithOperator: Sequence[InstancePropertyStringFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeInstancePropertiesResultTypeDef:
        """
        An API operation used by the Systems Manager console to display information
        about Systems Manager managed
        nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_instance_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_instance_properties)
        """

    async def describe_inventory_deletions(
        self, *, DeletionId: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeInventoryDeletionsResultTypeDef:
        """
        Describes a specific delete inventory operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_inventory_deletions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_inventory_deletions)
        """

    async def describe_maintenance_window_execution_task_invocations(
        self,
        *,
        WindowExecutionId: str,
        TaskId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef:
        """
        Retrieves the individual task executions (one per target) for a particular task
        run as part of a maintenance window
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_execution_task_invocations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_execution_task_invocations)
        """

    async def describe_maintenance_window_execution_tasks(
        self,
        *,
        WindowExecutionId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowExecutionTasksResultTypeDef:
        """
        For a given maintenance window execution, lists the tasks that were run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_execution_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_execution_tasks)
        """

    async def describe_maintenance_window_executions(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowExecutionsResultTypeDef:
        """
        Lists the executions of a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_executions)
        """

    async def describe_maintenance_window_schedule(
        self,
        *,
        WindowId: str = ...,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        ResourceType: MaintenanceWindowResourceTypeType = ...,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowScheduleResultTypeDef:
        """
        Retrieves information about upcoming executions of a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_schedule)
        """

    async def describe_maintenance_window_targets(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowTargetsResultTypeDef:
        """
        Lists the targets registered with the maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_targets)
        """

    async def describe_maintenance_window_tasks(
        self,
        *,
        WindowId: str,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowTasksResultTypeDef:
        """
        Lists the tasks in a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_window_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_window_tasks)
        """

    async def describe_maintenance_windows(
        self,
        *,
        Filters: Sequence[MaintenanceWindowFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowsResultTypeDef:
        """
        Retrieves the maintenance windows in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_windows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_windows)
        """

    async def describe_maintenance_windows_for_target(
        self,
        *,
        Targets: Sequence[TargetUnionTypeDef],
        ResourceType: MaintenanceWindowResourceTypeType,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeMaintenanceWindowsForTargetResultTypeDef:
        """
        Retrieves information about the maintenance window targets or tasks that a
        managed node is associated
        with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_maintenance_windows_for_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_maintenance_windows_for_target)
        """

    async def describe_ops_items(
        self,
        *,
        OpsItemFilters: Sequence[OpsItemFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeOpsItemsResponseTypeDef:
        """
        Query a set of OpsItems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_ops_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_ops_items)
        """

    async def describe_parameters(
        self,
        *,
        Filters: Sequence[ParametersFilterTypeDef] = ...,
        ParameterFilters: Sequence[ParameterStringFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Shared: bool = ...,
    ) -> DescribeParametersResultTypeDef:
        """
        Lists the parameters in your Amazon Web Services account or the parameters
        shared with you when you enable the
        [Shared](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_DescribeParameters.html#systemsmanager-DescribeParameters-request-Shared)
        option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_parameters)
        """

    async def describe_patch_baselines(
        self,
        *,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribePatchBaselinesResultTypeDef:
        """
        Lists the patch baselines in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_patch_baselines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_patch_baselines)
        """

    async def describe_patch_group_state(
        self, *, PatchGroup: str
    ) -> DescribePatchGroupStateResultTypeDef:
        """
        Returns high-level aggregated patch compliance state information for a patch
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_patch_group_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_patch_group_state)
        """

    async def describe_patch_groups(
        self,
        *,
        MaxResults: int = ...,
        Filters: Sequence[PatchOrchestratorFilterTypeDef] = ...,
        NextToken: str = ...,
    ) -> DescribePatchGroupsResultTypeDef:
        """
        Lists all patch groups that have been registered with patch baselines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_patch_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_patch_groups)
        """

    async def describe_patch_properties(
        self,
        *,
        OperatingSystem: OperatingSystemType,
        Property: PatchPropertyType,
        PatchSet: PatchSetType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribePatchPropertiesResultTypeDef:
        """
        Lists the properties of available patches organized by product, product family,
        classification, severity, and other properties of available
        patches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_patch_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_patch_properties)
        """

    async def describe_sessions(
        self,
        *,
        State: SessionStateType,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[SessionFilterTypeDef] = ...,
    ) -> DescribeSessionsResponseTypeDef:
        """
        Retrieves a list of all active sessions (both connected and disconnected) or
        terminated sessions from the past 30
        days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#describe_sessions)
        """

    async def disassociate_ops_item_related_item(
        self, *, OpsItemId: str, AssociationId: str
    ) -> Dict[str, Any]:
        """
        Deletes the association between an OpsItem and a related item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.disassociate_ops_item_related_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#disassociate_ops_item_related_item)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#generate_presigned_url)
        """

    async def get_automation_execution(
        self, *, AutomationExecutionId: str
    ) -> GetAutomationExecutionResultTypeDef:
        """
        Get detailed information about a particular Automation execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_automation_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_automation_execution)
        """

    async def get_calendar_state(
        self, *, CalendarNames: Sequence[str], AtTime: str = ...
    ) -> GetCalendarStateResponseTypeDef:
        """
        Gets the state of a Amazon Web Services Systems Manager change calendar at the
        current time or a specified
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_calendar_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_calendar_state)
        """

    async def get_command_invocation(
        self, *, CommandId: str, InstanceId: str, PluginName: str = ...
    ) -> GetCommandInvocationResultTypeDef:
        """
        Returns detailed information about command execution for an invocation or
        plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_command_invocation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_command_invocation)
        """

    async def get_connection_status(self, *, Target: str) -> GetConnectionStatusResponseTypeDef:
        """
        Retrieves the Session Manager connection status for a managed node to determine
        whether it is running and ready to receive Session Manager
        connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_connection_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_connection_status)
        """

    async def get_default_patch_baseline(
        self, *, OperatingSystem: OperatingSystemType = ...
    ) -> GetDefaultPatchBaselineResultTypeDef:
        """
        Retrieves the default patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_default_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_default_patch_baseline)
        """

    async def get_deployable_patch_snapshot_for_instance(
        self, *, InstanceId: str, SnapshotId: str, BaselineOverride: BaselineOverrideTypeDef = ...
    ) -> GetDeployablePatchSnapshotForInstanceResultTypeDef:
        """
        Retrieves the current snapshot for the patch baseline the managed node uses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_deployable_patch_snapshot_for_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_deployable_patch_snapshot_for_instance)
        """

    async def get_document(
        self,
        *,
        Name: str,
        VersionName: str = ...,
        DocumentVersion: str = ...,
        DocumentFormat: DocumentFormatType = ...,
    ) -> GetDocumentResultTypeDef:
        """
        Gets the contents of the specified Amazon Web Services Systems Manager document
        (SSM
        document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_document)
        """

    async def get_inventory(
        self,
        *,
        Filters: Sequence[InventoryFilterTypeDef] = ...,
        Aggregators: Sequence["InventoryAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence[ResultAttributeTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> GetInventoryResultTypeDef:
        """
        Query inventory information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_inventory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_inventory)
        """

    async def get_inventory_schema(
        self,
        *,
        TypeName: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Aggregator: bool = ...,
        SubType: bool = ...,
    ) -> GetInventorySchemaResultTypeDef:
        """
        Return a list of inventory type names for the account, or return a list of
        attribute names for a specific Inventory item
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_inventory_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_inventory_schema)
        """

    async def get_maintenance_window(self, *, WindowId: str) -> GetMaintenanceWindowResultTypeDef:
        """
        Retrieves a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_maintenance_window)
        """

    async def get_maintenance_window_execution(
        self, *, WindowExecutionId: str
    ) -> GetMaintenanceWindowExecutionResultTypeDef:
        """
        Retrieves details about a specific a maintenance window execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_maintenance_window_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_maintenance_window_execution)
        """

    async def get_maintenance_window_execution_task(
        self, *, WindowExecutionId: str, TaskId: str
    ) -> GetMaintenanceWindowExecutionTaskResultTypeDef:
        """
        Retrieves the details about a specific task run as part of a maintenance window
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_maintenance_window_execution_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_maintenance_window_execution_task)
        """

    async def get_maintenance_window_execution_task_invocation(
        self, *, WindowExecutionId: str, TaskId: str, InvocationId: str
    ) -> GetMaintenanceWindowExecutionTaskInvocationResultTypeDef:
        """
        Retrieves information about a specific task running on a specific target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_maintenance_window_execution_task_invocation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_maintenance_window_execution_task_invocation)
        """

    async def get_maintenance_window_task(
        self, *, WindowId: str, WindowTaskId: str
    ) -> GetMaintenanceWindowTaskResultTypeDef:
        """
        Retrieves the details of a maintenance window task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_maintenance_window_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_maintenance_window_task)
        """

    async def get_ops_item(
        self, *, OpsItemId: str, OpsItemArn: str = ...
    ) -> GetOpsItemResponseTypeDef:
        """
        Get information about an OpsItem by using the ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_ops_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_ops_item)
        """

    async def get_ops_metadata(
        self, *, OpsMetadataArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetOpsMetadataResultTypeDef:
        """
        View operational metadata related to an application in Application Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_ops_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_ops_metadata)
        """

    async def get_ops_summary(
        self,
        *,
        SyncName: str = ...,
        Filters: Sequence[OpsFilterTypeDef] = ...,
        Aggregators: Sequence["OpsAggregatorTypeDef"] = ...,
        ResultAttributes: Sequence[OpsResultAttributeTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> GetOpsSummaryResultTypeDef:
        """
        View a summary of operations metadata (OpsData) based on specified filters and
        aggregators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_ops_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_ops_summary)
        """

    async def get_parameter(
        self, *, Name: str, WithDecryption: bool = ...
    ) -> GetParameterResultTypeDef:
        """
        Get information about a single parameter by specifying the parameter name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_parameter)
        """

    async def get_parameter_history(
        self, *, Name: str, WithDecryption: bool = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> GetParameterHistoryResultTypeDef:
        """
        Retrieves the history of all changes to a parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_parameter_history)
        """

    async def get_parameters(
        self, *, Names: Sequence[str], WithDecryption: bool = ...
    ) -> GetParametersResultTypeDef:
        """
        Get information about one or more parameters by specifying multiple parameter
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_parameters)
        """

    async def get_parameters_by_path(
        self,
        *,
        Path: str,
        Recursive: bool = ...,
        ParameterFilters: Sequence[ParameterStringFilterTypeDef] = ...,
        WithDecryption: bool = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> GetParametersByPathResultTypeDef:
        """
        Retrieve information about one or more parameters in a specific hierarchy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameters_by_path)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_parameters_by_path)
        """

    async def get_patch_baseline(self, *, BaselineId: str) -> GetPatchBaselineResultTypeDef:
        """
        Retrieves information about a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_patch_baseline)
        """

    async def get_patch_baseline_for_patch_group(
        self, *, PatchGroup: str, OperatingSystem: OperatingSystemType = ...
    ) -> GetPatchBaselineForPatchGroupResultTypeDef:
        """
        Retrieves the patch baseline that should be used for the specified patch group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_patch_baseline_for_patch_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_patch_baseline_for_patch_group)
        """

    async def get_resource_policies(
        self, *, ResourceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Returns an array of the `Policy` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_resource_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_resource_policies)
        """

    async def get_service_setting(self, *, SettingId: str) -> GetServiceSettingResultTypeDef:
        """
        `ServiceSetting` is an account-level setting for an Amazon Web Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_service_setting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_service_setting)
        """

    async def label_parameter_version(
        self, *, Name: str, Labels: Sequence[str], ParameterVersion: int = ...
    ) -> LabelParameterVersionResultTypeDef:
        """
        A parameter label is a user-defined alias to help you manage different versions
        of a
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.label_parameter_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#label_parameter_version)
        """

    async def list_association_versions(
        self, *, AssociationId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAssociationVersionsResultTypeDef:
        """
        Retrieves all versions of an association for a specific association ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_association_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_association_versions)
        """

    async def list_associations(
        self,
        *,
        AssociationFilterList: Sequence[AssociationFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListAssociationsResultTypeDef:
        """
        Returns all State Manager associations in the current Amazon Web Services
        account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_associations)
        """

    async def list_command_invocations(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[CommandFilterTypeDef] = ...,
        Details: bool = ...,
    ) -> ListCommandInvocationsResultTypeDef:
        """
        An invocation is copy of a command sent to a specific managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_command_invocations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_command_invocations)
        """

    async def list_commands(
        self,
        *,
        CommandId: str = ...,
        InstanceId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[CommandFilterTypeDef] = ...,
    ) -> ListCommandsResultTypeDef:
        """
        Lists the commands requested by users of the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_commands)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_commands)
        """

    async def list_compliance_items(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        ResourceIds: Sequence[str] = ...,
        ResourceTypes: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListComplianceItemsResultTypeDef:
        """
        For a specified resource ID, this API operation returns a list of compliance
        statuses for different resource
        types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_compliance_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_compliance_items)
        """

    async def list_compliance_summaries(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListComplianceSummariesResultTypeDef:
        """
        Returns a summary count of compliant and non-compliant resources for a
        compliance
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_compliance_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_compliance_summaries)
        """

    async def list_document_metadata_history(
        self,
        *,
        Name: str,
        Metadata: Literal["DocumentReviews"],
        DocumentVersion: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListDocumentMetadataHistoryResponseTypeDef:
        """
        Information about approval reviews for a version of a change template in Change
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_document_metadata_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_document_metadata_history)
        """

    async def list_document_versions(
        self, *, Name: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDocumentVersionsResultTypeDef:
        """
        List all versions for a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_document_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_document_versions)
        """

    async def list_documents(
        self,
        *,
        DocumentFilterList: Sequence[DocumentFilterTypeDef] = ...,
        Filters: Sequence[DocumentKeyValuesFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListDocumentsResultTypeDef:
        """
        Returns all Systems Manager (SSM) documents in the current Amazon Web Services
        account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_documents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_documents)
        """

    async def list_inventory_entries(
        self,
        *,
        InstanceId: str,
        TypeName: str,
        Filters: Sequence[InventoryFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListInventoryEntriesResultTypeDef:
        """
        A list of inventory items returned by the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_inventory_entries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_inventory_entries)
        """

    async def list_ops_item_events(
        self,
        *,
        Filters: Sequence[OpsItemEventFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListOpsItemEventsResponseTypeDef:
        """
        Returns a list of all OpsItem events in the current Amazon Web Services Region
        and Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_ops_item_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_ops_item_events)
        """

    async def list_ops_item_related_items(
        self,
        *,
        OpsItemId: str = ...,
        Filters: Sequence[OpsItemRelatedItemsFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListOpsItemRelatedItemsResponseTypeDef:
        """
        Lists all related-item resources associated with a Systems Manager OpsCenter
        OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_ops_item_related_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_ops_item_related_items)
        """

    async def list_ops_metadata(
        self,
        *,
        Filters: Sequence[OpsMetadataFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListOpsMetadataResultTypeDef:
        """
        Amazon Web Services Systems Manager calls this API operation when displaying
        all Application Manager OpsMetadata objects or
        blobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_ops_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_ops_metadata)
        """

    async def list_resource_compliance_summaries(
        self,
        *,
        Filters: Sequence[ComplianceStringFilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListResourceComplianceSummariesResultTypeDef:
        """
        Returns a resource-level summary count.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_resource_compliance_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_resource_compliance_summaries)
        """

    async def list_resource_data_sync(
        self, *, SyncType: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListResourceDataSyncResultTypeDef:
        """
        Lists your resource data sync configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_resource_data_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_resource_data_sync)
        """

    async def list_tags_for_resource(
        self, *, ResourceType: ResourceTypeForTaggingType, ResourceId: str
    ) -> ListTagsForResourceResultTypeDef:
        """
        Returns a list of the tags assigned to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#list_tags_for_resource)
        """

    async def modify_document_permission(
        self,
        *,
        Name: str,
        PermissionType: Literal["Share"],
        AccountIdsToAdd: Sequence[str] = ...,
        AccountIdsToRemove: Sequence[str] = ...,
        SharedDocumentVersion: str = ...,
    ) -> Dict[str, Any]:
        """
        Shares a Amazon Web Services Systems Manager document (SSM document)publicly or
        privately.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.modify_document_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#modify_document_permission)
        """

    async def put_compliance_items(
        self,
        *,
        ResourceId: str,
        ResourceType: str,
        ComplianceType: str,
        ExecutionSummary: ComplianceExecutionSummaryUnionTypeDef,
        Items: Sequence[ComplianceItemEntryTypeDef],
        ItemContentHash: str = ...,
        UploadType: ComplianceUploadTypeType = ...,
    ) -> Dict[str, Any]:
        """
        Registers a compliance type and other compliance details on a designated
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_compliance_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#put_compliance_items)
        """

    async def put_inventory(
        self, *, InstanceId: str, Items: Sequence[InventoryItemTypeDef]
    ) -> PutInventoryResultTypeDef:
        """
        Bulk update custom inventory items on one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_inventory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#put_inventory)
        """

    async def put_parameter(
        self,
        *,
        Name: str,
        Value: str,
        Description: str = ...,
        Type: ParameterTypeType = ...,
        KeyId: str = ...,
        Overwrite: bool = ...,
        AllowedPattern: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        Tier: ParameterTierType = ...,
        Policies: str = ...,
        DataType: str = ...,
    ) -> PutParameterResultTypeDef:
        """
        Add a parameter to the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#put_parameter)
        """

    async def put_resource_policy(
        self, *, ResourceArn: str, Policy: str, PolicyId: str = ..., PolicyHash: str = ...
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a Systems Manager resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#put_resource_policy)
        """

    async def register_default_patch_baseline(
        self, *, BaselineId: str
    ) -> RegisterDefaultPatchBaselineResultTypeDef:
        """
        Defines the default patch baseline for the relevant operating system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.register_default_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#register_default_patch_baseline)
        """

    async def register_patch_baseline_for_patch_group(
        self, *, BaselineId: str, PatchGroup: str
    ) -> RegisterPatchBaselineForPatchGroupResultTypeDef:
        """
        Registers a patch baseline for a patch group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.register_patch_baseline_for_patch_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#register_patch_baseline_for_patch_group)
        """

    async def register_target_with_maintenance_window(
        self,
        *,
        WindowId: str,
        ResourceType: MaintenanceWindowResourceTypeType,
        Targets: Sequence[TargetUnionTypeDef],
        OwnerInformation: str = ...,
        Name: str = ...,
        Description: str = ...,
        ClientToken: str = ...,
    ) -> RegisterTargetWithMaintenanceWindowResultTypeDef:
        """
        Registers a target with a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.register_target_with_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#register_target_with_maintenance_window)
        """

    async def register_task_with_maintenance_window(
        self,
        *,
        WindowId: str,
        TaskArn: str,
        TaskType: MaintenanceWindowTaskTypeType,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        ServiceRoleArn: str = ...,
        TaskParameters: Mapping[
            str, MaintenanceWindowTaskParameterValueExpressionUnionTypeDef
        ] = ...,
        TaskInvocationParameters: MaintenanceWindowTaskInvocationParametersUnionTypeDef = ...,
        Priority: int = ...,
        MaxConcurrency: str = ...,
        MaxErrors: str = ...,
        LoggingInfo: LoggingInfoTypeDef = ...,
        Name: str = ...,
        Description: str = ...,
        ClientToken: str = ...,
        CutoffBehavior: MaintenanceWindowTaskCutoffBehaviorType = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> RegisterTaskWithMaintenanceWindowResultTypeDef:
        """
        Adds a new task to a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.register_task_with_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#register_task_with_maintenance_window)
        """

    async def remove_tags_from_resource(
        self, *, ResourceType: ResourceTypeForTaggingType, ResourceId: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes tag keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.remove_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#remove_tags_from_resource)
        """

    async def reset_service_setting(self, *, SettingId: str) -> ResetServiceSettingResultTypeDef:
        """
        `ServiceSetting` is an account-level setting for an Amazon Web Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.reset_service_setting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#reset_service_setting)
        """

    async def resume_session(self, *, SessionId: str) -> ResumeSessionResponseTypeDef:
        """
        Reconnects a session to a managed node after it has been disconnected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.resume_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#resume_session)
        """

    async def send_automation_signal(
        self,
        *,
        AutomationExecutionId: str,
        SignalType: SignalTypeType,
        Payload: Mapping[str, Sequence[str]] = ...,
    ) -> Dict[str, Any]:
        """
        Sends a signal to an Automation execution to change the current behavior or
        status of the
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_automation_signal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#send_automation_signal)
        """

    async def send_command(
        self,
        *,
        DocumentName: str,
        InstanceIds: Sequence[str] = ...,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        DocumentVersion: str = ...,
        DocumentHash: str = ...,
        DocumentHashType: DocumentHashTypeType = ...,
        TimeoutSeconds: int = ...,
        Comment: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...,
        OutputS3Region: str = ...,
        OutputS3BucketName: str = ...,
        OutputS3KeyPrefix: str = ...,
        MaxConcurrency: str = ...,
        MaxErrors: str = ...,
        ServiceRoleArn: str = ...,
        NotificationConfig: NotificationConfigUnionTypeDef = ...,
        CloudWatchOutputConfig: CloudWatchOutputConfigTypeDef = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> SendCommandResultTypeDef:
        """
        Runs commands on one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#send_command)
        """

    async def start_associations_once(self, *, AssociationIds: Sequence[str]) -> Dict[str, Any]:
        """
        Runs an association immediately and only one time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.start_associations_once)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#start_associations_once)
        """

    async def start_automation_execution(
        self,
        *,
        DocumentName: str,
        DocumentVersion: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...,
        ClientToken: str = ...,
        Mode: ExecutionModeType = ...,
        TargetParameterName: str = ...,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        TargetMaps: Sequence[Mapping[str, Sequence[str]]] = ...,
        MaxConcurrency: str = ...,
        MaxErrors: str = ...,
        TargetLocations: Sequence[TargetLocationUnionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> StartAutomationExecutionResultTypeDef:
        """
        Initiates execution of an Automation runbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.start_automation_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#start_automation_execution)
        """

    async def start_change_request_execution(
        self,
        *,
        DocumentName: str,
        Runbooks: Sequence[RunbookUnionTypeDef],
        ScheduledTime: TimestampTypeDef = ...,
        DocumentVersion: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...,
        ChangeRequestName: str = ...,
        ClientToken: str = ...,
        AutoApprove: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ScheduledEndTime: TimestampTypeDef = ...,
        ChangeDetails: str = ...,
    ) -> StartChangeRequestExecutionResultTypeDef:
        """
        Creates a change request for Change Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.start_change_request_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#start_change_request_execution)
        """

    async def start_session(
        self,
        *,
        Target: str,
        DocumentName: str = ...,
        Reason: str = ...,
        Parameters: Mapping[str, Sequence[str]] = ...,
    ) -> StartSessionResponseTypeDef:
        """
        Initiates a connection to a target (for example, a managed node) for a Session
        Manager
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.start_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#start_session)
        """

    async def stop_automation_execution(
        self, *, AutomationExecutionId: str, Type: StopTypeType = ...
    ) -> Dict[str, Any]:
        """
        Stop an Automation that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.stop_automation_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#stop_automation_execution)
        """

    async def terminate_session(self, *, SessionId: str) -> TerminateSessionResponseTypeDef:
        """
        Permanently ends a session and closes the data connection between the Session
        Manager client and SSM Agent on the managed
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.terminate_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#terminate_session)
        """

    async def unlabel_parameter_version(
        self, *, Name: str, ParameterVersion: int, Labels: Sequence[str]
    ) -> UnlabelParameterVersionResultTypeDef:
        """
        Remove a label or labels from a parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.unlabel_parameter_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#unlabel_parameter_version)
        """

    async def update_association(
        self,
        *,
        AssociationId: str,
        Parameters: Mapping[str, Sequence[str]] = ...,
        DocumentVersion: str = ...,
        ScheduleExpression: str = ...,
        OutputLocation: InstanceAssociationOutputLocationTypeDef = ...,
        Name: str = ...,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        AssociationName: str = ...,
        AssociationVersion: str = ...,
        AutomationTargetParameterName: str = ...,
        MaxErrors: str = ...,
        MaxConcurrency: str = ...,
        ComplianceSeverity: AssociationComplianceSeverityType = ...,
        SyncCompliance: AssociationSyncComplianceType = ...,
        ApplyOnlyAtCronInterval: bool = ...,
        CalendarNames: Sequence[str] = ...,
        TargetLocations: Sequence[TargetLocationUnionTypeDef] = ...,
        ScheduleOffset: int = ...,
        Duration: int = ...,
        TargetMaps: Sequence[Mapping[str, Sequence[str]]] = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> UpdateAssociationResultTypeDef:
        """
        Updates an association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_association)
        """

    async def update_association_status(
        self, *, Name: str, InstanceId: str, AssociationStatus: AssociationStatusUnionTypeDef
    ) -> UpdateAssociationStatusResultTypeDef:
        """
        Updates the status of the Amazon Web Services Systems Manager document (SSM
        document) associated with the specified managed
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_association_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_association_status)
        """

    async def update_document(
        self,
        *,
        Content: str,
        Name: str,
        Attachments: Sequence[AttachmentsSourceTypeDef] = ...,
        DisplayName: str = ...,
        VersionName: str = ...,
        DocumentVersion: str = ...,
        DocumentFormat: DocumentFormatType = ...,
        TargetType: str = ...,
    ) -> UpdateDocumentResultTypeDef:
        """
        Updates one or more values for an SSM document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_document)
        """

    async def update_document_default_version(
        self, *, Name: str, DocumentVersion: str
    ) -> UpdateDocumentDefaultVersionResultTypeDef:
        """
        Set the default version of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_document_default_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_document_default_version)
        """

    async def update_document_metadata(
        self, *, Name: str, DocumentReviews: DocumentReviewsTypeDef, DocumentVersion: str = ...
    ) -> Dict[str, Any]:
        """
        Updates information related to approval reviews for a specific version of a
        change template in Change
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_document_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_document_metadata)
        """

    async def update_maintenance_window(
        self,
        *,
        WindowId: str,
        Name: str = ...,
        Description: str = ...,
        StartDate: str = ...,
        EndDate: str = ...,
        Schedule: str = ...,
        ScheduleTimezone: str = ...,
        ScheduleOffset: int = ...,
        Duration: int = ...,
        Cutoff: int = ...,
        AllowUnassociatedTargets: bool = ...,
        Enabled: bool = ...,
        Replace: bool = ...,
    ) -> UpdateMaintenanceWindowResultTypeDef:
        """
        Updates an existing maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_maintenance_window)
        """

    async def update_maintenance_window_target(
        self,
        *,
        WindowId: str,
        WindowTargetId: str,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        OwnerInformation: str = ...,
        Name: str = ...,
        Description: str = ...,
        Replace: bool = ...,
    ) -> UpdateMaintenanceWindowTargetResultTypeDef:
        """
        Modifies the target of an existing maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_maintenance_window_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_maintenance_window_target)
        """

    async def update_maintenance_window_task(
        self,
        *,
        WindowId: str,
        WindowTaskId: str,
        Targets: Sequence[TargetUnionTypeDef] = ...,
        TaskArn: str = ...,
        ServiceRoleArn: str = ...,
        TaskParameters: Mapping[
            str, MaintenanceWindowTaskParameterValueExpressionUnionTypeDef
        ] = ...,
        TaskInvocationParameters: MaintenanceWindowTaskInvocationParametersUnionTypeDef = ...,
        Priority: int = ...,
        MaxConcurrency: str = ...,
        MaxErrors: str = ...,
        LoggingInfo: LoggingInfoTypeDef = ...,
        Name: str = ...,
        Description: str = ...,
        Replace: bool = ...,
        CutoffBehavior: MaintenanceWindowTaskCutoffBehaviorType = ...,
        AlarmConfiguration: AlarmConfigurationUnionTypeDef = ...,
    ) -> UpdateMaintenanceWindowTaskResultTypeDef:
        """
        Modifies a task assigned to a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_maintenance_window_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_maintenance_window_task)
        """

    async def update_managed_instance_role(
        self, *, InstanceId: str, IamRole: str
    ) -> Dict[str, Any]:
        """
        Changes the Identity and Access Management (IAM) role that is assigned to the
        on-premises server, edge device, or virtual machines
        (VM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_managed_instance_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_managed_instance_role)
        """

    async def update_ops_item(
        self,
        *,
        OpsItemId: str,
        Description: str = ...,
        OperationalData: Mapping[str, OpsItemDataValueTypeDef] = ...,
        OperationalDataToDelete: Sequence[str] = ...,
        Notifications: Sequence[OpsItemNotificationTypeDef] = ...,
        Priority: int = ...,
        RelatedOpsItems: Sequence[RelatedOpsItemTypeDef] = ...,
        Status: OpsItemStatusType = ...,
        Title: str = ...,
        Category: str = ...,
        Severity: str = ...,
        ActualStartTime: TimestampTypeDef = ...,
        ActualEndTime: TimestampTypeDef = ...,
        PlannedStartTime: TimestampTypeDef = ...,
        PlannedEndTime: TimestampTypeDef = ...,
        OpsItemArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Edit or change an OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_ops_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_ops_item)
        """

    async def update_ops_metadata(
        self,
        *,
        OpsMetadataArn: str,
        MetadataToUpdate: Mapping[str, MetadataValueTypeDef] = ...,
        KeysToDelete: Sequence[str] = ...,
    ) -> UpdateOpsMetadataResultTypeDef:
        """
        Amazon Web Services Systems Manager calls this API operation when you edit
        OpsMetadata in Application
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_ops_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_ops_metadata)
        """

    async def update_patch_baseline(
        self,
        *,
        BaselineId: str,
        Name: str = ...,
        GlobalFilters: PatchFilterGroupUnionTypeDef = ...,
        ApprovalRules: PatchRuleGroupUnionTypeDef = ...,
        ApprovedPatches: Sequence[str] = ...,
        ApprovedPatchesComplianceLevel: PatchComplianceLevelType = ...,
        ApprovedPatchesEnableNonSecurity: bool = ...,
        RejectedPatches: Sequence[str] = ...,
        RejectedPatchesAction: PatchActionType = ...,
        Description: str = ...,
        Sources: Sequence[PatchSourceUnionTypeDef] = ...,
        Replace: bool = ...,
    ) -> UpdatePatchBaselineResultTypeDef:
        """
        Modifies an existing patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_patch_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_patch_baseline)
        """

    async def update_resource_data_sync(
        self, *, SyncName: str, SyncType: str, SyncSource: ResourceDataSyncSourceTypeDef
    ) -> Dict[str, Any]:
        """
        Update a resource data sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_resource_data_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_resource_data_sync)
        """

    async def update_service_setting(self, *, SettingId: str, SettingValue: str) -> Dict[str, Any]:
        """
        `ServiceSetting` is an account-level setting for an Amazon Web Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.update_service_setting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#update_service_setting)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_activations"]
    ) -> DescribeActivationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_association_execution_targets"]
    ) -> DescribeAssociationExecutionTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_association_executions"]
    ) -> DescribeAssociationExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_automation_executions"]
    ) -> DescribeAutomationExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_automation_step_executions"]
    ) -> DescribeAutomationStepExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_available_patches"]
    ) -> DescribeAvailablePatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_effective_instance_associations"]
    ) -> DescribeEffectiveInstanceAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_effective_patches_for_patch_baseline"]
    ) -> DescribeEffectivePatchesForPatchBaselinePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_associations_status"]
    ) -> DescribeInstanceAssociationsStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_information"]
    ) -> DescribeInstanceInformationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patch_states"]
    ) -> DescribeInstancePatchStatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patch_states_for_patch_group"]
    ) -> DescribeInstancePatchStatesForPatchGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patches"]
    ) -> DescribeInstancePatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_properties"]
    ) -> DescribeInstancePropertiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_inventory_deletions"]
    ) -> DescribeInventoryDeletionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_execution_task_invocations"]
    ) -> DescribeMaintenanceWindowExecutionTaskInvocationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_execution_tasks"]
    ) -> DescribeMaintenanceWindowExecutionTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_executions"]
    ) -> DescribeMaintenanceWindowExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_schedule"]
    ) -> DescribeMaintenanceWindowSchedulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_targets"]
    ) -> DescribeMaintenanceWindowTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_tasks"]
    ) -> DescribeMaintenanceWindowTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_windows"]
    ) -> DescribeMaintenanceWindowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_windows_for_target"]
    ) -> DescribeMaintenanceWindowsForTargetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ops_items"]
    ) -> DescribeOpsItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_parameters"]
    ) -> DescribeParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_baselines"]
    ) -> DescribePatchBaselinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_groups"]
    ) -> DescribePatchGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_properties"]
    ) -> DescribePatchPropertiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_sessions"]
    ) -> DescribeSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_inventory"]) -> GetInventoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_inventory_schema"]
    ) -> GetInventorySchemaPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_ops_summary"]) -> GetOpsSummaryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_parameter_history"]
    ) -> GetParameterHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_parameters_by_path"]
    ) -> GetParametersByPathPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_association_versions"]
    ) -> ListAssociationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associations"]
    ) -> ListAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_command_invocations"]
    ) -> ListCommandInvocationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_commands"]) -> ListCommandsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_items"]
    ) -> ListComplianceItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_summaries"]
    ) -> ListComplianceSummariesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_document_versions"]
    ) -> ListDocumentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_documents"]) -> ListDocumentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_item_events"]
    ) -> ListOpsItemEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_item_related_items"]
    ) -> ListOpsItemRelatedItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_metadata"]
    ) -> ListOpsMetadataPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_compliance_summaries"]
    ) -> ListResourceComplianceSummariesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_data_sync"]
    ) -> ListResourceDataSyncPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["command_executed"]) -> CommandExecutedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/#get_waiter)
        """

    async def __aenter__(self) -> "SSMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/client/)
        """
