"""
Type annotations for codepipeline service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codepipeline.client import CodePipelineClient

    session = get_session()
    async with session.create_client("codepipeline") as client:
        client: CodePipelineClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionCategoryType,
    ActionOwnerType,
    ConditionTypeType,
    StageRetryModeType,
    StageTransitionTypeType,
)
from .paginator import (
    ListActionExecutionsPaginator,
    ListActionTypesPaginator,
    ListPipelineExecutionsPaginator,
    ListPipelinesPaginator,
    ListRuleExecutionsPaginator,
    ListTagsForResourcePaginator,
    ListWebhooksPaginator,
)
from .type_defs import (
    AcknowledgeJobOutputTypeDef,
    AcknowledgeThirdPartyJobOutputTypeDef,
    ActionConfigurationPropertyTypeDef,
    ActionExecutionFilterTypeDef,
    ActionRevisionUnionTypeDef,
    ActionTypeDeclarationUnionTypeDef,
    ActionTypeIdTypeDef,
    ActionTypeSettingsTypeDef,
    ApprovalResultTypeDef,
    ArtifactDetailsTypeDef,
    CreateCustomActionTypeOutputTypeDef,
    CreatePipelineOutputTypeDef,
    CurrentRevisionTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecutionDetailsTypeDef,
    FailureDetailsTypeDef,
    GetActionTypeOutputTypeDef,
    GetJobDetailsOutputTypeDef,
    GetPipelineExecutionOutputTypeDef,
    GetPipelineOutputTypeDef,
    GetPipelineStateOutputTypeDef,
    GetThirdPartyJobDetailsOutputTypeDef,
    ListActionExecutionsOutputTypeDef,
    ListActionTypesOutputTypeDef,
    ListPipelineExecutionsOutputTypeDef,
    ListPipelinesOutputTypeDef,
    ListRuleExecutionsOutputTypeDef,
    ListRuleTypesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWebhooksOutputTypeDef,
    PipelineDeclarationUnionTypeDef,
    PipelineExecutionFilterTypeDef,
    PipelineVariableTypeDef,
    PollForJobsOutputTypeDef,
    PollForThirdPartyJobsOutputTypeDef,
    PutActionRevisionOutputTypeDef,
    PutApprovalResultOutputTypeDef,
    PutWebhookOutputTypeDef,
    RetryStageExecutionOutputTypeDef,
    RollbackStageOutputTypeDef,
    RuleExecutionFilterTypeDef,
    SourceRevisionOverrideTypeDef,
    StartPipelineExecutionOutputTypeDef,
    StopPipelineExecutionOutputTypeDef,
    TagTypeDef,
    UpdatePipelineOutputTypeDef,
    WebhookDefinitionUnionTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CodePipelineClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActionNotFoundException: Type[BotocoreClientError]
    ActionTypeAlreadyExistsException: Type[BotocoreClientError]
    ActionTypeNotFoundException: Type[BotocoreClientError]
    ApprovalAlreadyCompletedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentPipelineExecutionsLimitExceededException: Type[BotocoreClientError]
    ConditionNotOverridableException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DuplicatedStopRequestException: Type[BotocoreClientError]
    InvalidActionDeclarationException: Type[BotocoreClientError]
    InvalidApprovalTokenException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidBlockerDeclarationException: Type[BotocoreClientError]
    InvalidClientTokenException: Type[BotocoreClientError]
    InvalidJobException: Type[BotocoreClientError]
    InvalidJobStateException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidNonceException: Type[BotocoreClientError]
    InvalidStageDeclarationException: Type[BotocoreClientError]
    InvalidStructureException: Type[BotocoreClientError]
    InvalidTagsException: Type[BotocoreClientError]
    InvalidWebhookAuthenticationParametersException: Type[BotocoreClientError]
    InvalidWebhookFilterPatternException: Type[BotocoreClientError]
    JobNotFoundException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotLatestPipelineExecutionException: Type[BotocoreClientError]
    OutputVariablesSizeExceededException: Type[BotocoreClientError]
    PipelineExecutionNotFoundException: Type[BotocoreClientError]
    PipelineExecutionNotStoppableException: Type[BotocoreClientError]
    PipelineExecutionOutdatedException: Type[BotocoreClientError]
    PipelineNameInUseException: Type[BotocoreClientError]
    PipelineNotFoundException: Type[BotocoreClientError]
    PipelineVersionNotFoundException: Type[BotocoreClientError]
    RequestFailedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    StageNotFoundException: Type[BotocoreClientError]
    StageNotRetryableException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnableToRollbackStageException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    WebhookNotFoundException: Type[BotocoreClientError]

class CodePipelineClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodePipelineClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#exceptions)
        """

    async def acknowledge_job(self, *, jobId: str, nonce: str) -> AcknowledgeJobOutputTypeDef:
        """
        Returns information about a specified job and whether that job has been
        received by the job
        worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.acknowledge_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#acknowledge_job)
        """

    async def acknowledge_third_party_job(
        self, *, jobId: str, nonce: str, clientToken: str
    ) -> AcknowledgeThirdPartyJobOutputTypeDef:
        """
        Confirms a job worker has received the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.acknowledge_third_party_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#acknowledge_third_party_job)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#close)
        """

    async def create_custom_action_type(
        self,
        *,
        category: ActionCategoryType,
        provider: str,
        version: str,
        inputArtifactDetails: ArtifactDetailsTypeDef,
        outputArtifactDetails: ArtifactDetailsTypeDef,
        settings: ActionTypeSettingsTypeDef = ...,
        configurationProperties: Sequence[ActionConfigurationPropertyTypeDef] = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateCustomActionTypeOutputTypeDef:
        """
        Creates a new custom action that can be used in all pipelines associated with
        the Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.create_custom_action_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#create_custom_action_type)
        """

    async def create_pipeline(
        self, *, pipeline: PipelineDeclarationUnionTypeDef, tags: Sequence[TagTypeDef] = ...
    ) -> CreatePipelineOutputTypeDef:
        """
        Creates a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.create_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#create_pipeline)
        """

    async def delete_custom_action_type(
        self, *, category: ActionCategoryType, provider: str, version: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Marks a custom action as deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.delete_custom_action_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#delete_custom_action_type)
        """

    async def delete_pipeline(self, *, name: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.delete_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#delete_pipeline)
        """

    async def delete_webhook(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes a previously created webhook by name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.delete_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#delete_webhook)
        """

    async def deregister_webhook_with_third_party(
        self, *, webhookName: str = ...
    ) -> Dict[str, Any]:
        """
        Removes the connection between the webhook that was created by CodePipeline and
        the external tool with events to be
        detected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.deregister_webhook_with_third_party)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#deregister_webhook_with_third_party)
        """

    async def disable_stage_transition(
        self,
        *,
        pipelineName: str,
        stageName: str,
        transitionType: StageTransitionTypeType,
        reason: str,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Prevents artifacts in a pipeline from transitioning to the next stage in the
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.disable_stage_transition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#disable_stage_transition)
        """

    async def enable_stage_transition(
        self, *, pipelineName: str, stageName: str, transitionType: StageTransitionTypeType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables artifacts in a pipeline to transition to a stage in a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.enable_stage_transition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#enable_stage_transition)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#generate_presigned_url)
        """

    async def get_action_type(
        self, *, category: ActionCategoryType, owner: str, provider: str, version: str
    ) -> GetActionTypeOutputTypeDef:
        """
        Returns information about an action type created for an external provider,
        where the action is to be used by customers of the external
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_action_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_action_type)
        """

    async def get_job_details(self, *, jobId: str) -> GetJobDetailsOutputTypeDef:
        """
        Returns information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_job_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_job_details)
        """

    async def get_pipeline(self, *, name: str, version: int = ...) -> GetPipelineOutputTypeDef:
        """
        Returns the metadata, structure, stages, and actions of a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_pipeline)
        """

    async def get_pipeline_execution(
        self, *, pipelineName: str, pipelineExecutionId: str
    ) -> GetPipelineExecutionOutputTypeDef:
        """
        Returns information about an execution of a pipeline, including details about
        artifacts, the pipeline execution ID, and the name, version, and status of the
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_pipeline_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_pipeline_execution)
        """

    async def get_pipeline_state(self, *, name: str) -> GetPipelineStateOutputTypeDef:
        """
        Returns information about the state of a pipeline, including the stages and
        actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_pipeline_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_pipeline_state)
        """

    async def get_third_party_job_details(
        self, *, jobId: str, clientToken: str
    ) -> GetThirdPartyJobDetailsOutputTypeDef:
        """
        Requests the details of a job for a third party action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_third_party_job_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_third_party_job_details)
        """

    async def list_action_executions(
        self,
        *,
        pipelineName: str,
        filter: ActionExecutionFilterTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListActionExecutionsOutputTypeDef:
        """
        Lists the action executions that have occurred in a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_action_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_action_executions)
        """

    async def list_action_types(
        self,
        *,
        actionOwnerFilter: ActionOwnerType = ...,
        nextToken: str = ...,
        regionFilter: str = ...,
    ) -> ListActionTypesOutputTypeDef:
        """
        Gets a summary of all CodePipeline action types associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_action_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_action_types)
        """

    async def list_pipeline_executions(
        self,
        *,
        pipelineName: str,
        maxResults: int = ...,
        filter: PipelineExecutionFilterTypeDef = ...,
        nextToken: str = ...,
    ) -> ListPipelineExecutionsOutputTypeDef:
        """
        Gets a summary of the most recent executions for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_pipeline_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_pipeline_executions)
        """

    async def list_pipelines(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListPipelinesOutputTypeDef:
        """
        Gets a summary of all of the pipelines associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_pipelines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_pipelines)
        """

    async def list_rule_executions(
        self,
        *,
        pipelineName: str,
        filter: RuleExecutionFilterTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListRuleExecutionsOutputTypeDef:
        """
        Lists the rule executions that have occurred in a pipeline configured for
        conditions with
        rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_rule_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_rule_executions)
        """

    async def list_rule_types(
        self, *, ruleOwnerFilter: Literal["AWS"] = ..., regionFilter: str = ...
    ) -> ListRuleTypesOutputTypeDef:
        """
        Lists the rules for the condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_rule_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_rule_types)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Gets the set of key-value pairs (metadata) that are used to manage the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_tags_for_resource)
        """

    async def list_webhooks(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWebhooksOutputTypeDef:
        """
        Gets a listing of all the webhooks in this Amazon Web Services Region for this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.list_webhooks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#list_webhooks)
        """

    async def override_stage_condition(
        self,
        *,
        pipelineName: str,
        stageName: str,
        pipelineExecutionId: str,
        conditionType: ConditionTypeType,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to override a stage condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.override_stage_condition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#override_stage_condition)
        """

    async def poll_for_jobs(
        self,
        *,
        actionTypeId: ActionTypeIdTypeDef,
        maxBatchSize: int = ...,
        queryParam: Mapping[str, str] = ...,
    ) -> PollForJobsOutputTypeDef:
        """
        Returns information about any jobs for CodePipeline to act on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.poll_for_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#poll_for_jobs)
        """

    async def poll_for_third_party_jobs(
        self, *, actionTypeId: ActionTypeIdTypeDef, maxBatchSize: int = ...
    ) -> PollForThirdPartyJobsOutputTypeDef:
        """
        Determines whether there are any third party jobs for a job worker to act on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.poll_for_third_party_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#poll_for_third_party_jobs)
        """

    async def put_action_revision(
        self,
        *,
        pipelineName: str,
        stageName: str,
        actionName: str,
        actionRevision: ActionRevisionUnionTypeDef,
    ) -> PutActionRevisionOutputTypeDef:
        """
        Provides information to CodePipeline about new revisions to a source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_action_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_action_revision)
        """

    async def put_approval_result(
        self,
        *,
        pipelineName: str,
        stageName: str,
        actionName: str,
        result: ApprovalResultTypeDef,
        token: str,
    ) -> PutApprovalResultOutputTypeDef:
        """
        Provides the response to a manual approval request to CodePipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_approval_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_approval_result)
        """

    async def put_job_failure_result(
        self, *, jobId: str, failureDetails: FailureDetailsTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents the failure of a job as returned to the pipeline by a job worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_job_failure_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_job_failure_result)
        """

    async def put_job_success_result(
        self,
        *,
        jobId: str,
        currentRevision: CurrentRevisionTypeDef = ...,
        continuationToken: str = ...,
        executionDetails: ExecutionDetailsTypeDef = ...,
        outputVariables: Mapping[str, str] = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents the success of a job as returned to the pipeline by a job worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_job_success_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_job_success_result)
        """

    async def put_third_party_job_failure_result(
        self, *, jobId: str, clientToken: str, failureDetails: FailureDetailsTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents the failure of a third party job as returned to the pipeline by a
        job
        worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_third_party_job_failure_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_third_party_job_failure_result)
        """

    async def put_third_party_job_success_result(
        self,
        *,
        jobId: str,
        clientToken: str,
        currentRevision: CurrentRevisionTypeDef = ...,
        continuationToken: str = ...,
        executionDetails: ExecutionDetailsTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Represents the success of a third party job as returned to the pipeline by a
        job
        worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_third_party_job_success_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_third_party_job_success_result)
        """

    async def put_webhook(
        self, *, webhook: WebhookDefinitionUnionTypeDef, tags: Sequence[TagTypeDef] = ...
    ) -> PutWebhookOutputTypeDef:
        """
        Defines a webhook and returns a unique webhook URL generated by CodePipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.put_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#put_webhook)
        """

    async def register_webhook_with_third_party(self, *, webhookName: str = ...) -> Dict[str, Any]:
        """
        Configures a connection between the webhook that was created and the external
        tool with events to be
        detected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.register_webhook_with_third_party)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#register_webhook_with_third_party)
        """

    async def retry_stage_execution(
        self,
        *,
        pipelineName: str,
        stageName: str,
        pipelineExecutionId: str,
        retryMode: StageRetryModeType,
    ) -> RetryStageExecutionOutputTypeDef:
        """
        You can retry a stage that has failed without having to run a pipeline again
        from the
        beginning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.retry_stage_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#retry_stage_execution)
        """

    async def rollback_stage(
        self, *, pipelineName: str, stageName: str, targetPipelineExecutionId: str
    ) -> RollbackStageOutputTypeDef:
        """
        Rolls back a stage execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.rollback_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#rollback_stage)
        """

    async def start_pipeline_execution(
        self,
        *,
        name: str,
        variables: Sequence[PipelineVariableTypeDef] = ...,
        clientRequestToken: str = ...,
        sourceRevisions: Sequence[SourceRevisionOverrideTypeDef] = ...,
    ) -> StartPipelineExecutionOutputTypeDef:
        """
        Starts the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.start_pipeline_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#start_pipeline_execution)
        """

    async def stop_pipeline_execution(
        self, *, pipelineName: str, pipelineExecutionId: str, abandon: bool = ..., reason: str = ...
    ) -> StopPipelineExecutionOutputTypeDef:
        """
        Stops the specified pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.stop_pipeline_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#stop_pipeline_execution)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#untag_resource)
        """

    async def update_action_type(
        self, *, actionType: ActionTypeDeclarationUnionTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an action type that was created with any supported integration model,
        where the action type is to be used by customers of the action type
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.update_action_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#update_action_type)
        """

    async def update_pipeline(
        self, *, pipeline: PipelineDeclarationUnionTypeDef
    ) -> UpdatePipelineOutputTypeDef:
        """
        Updates a specified pipeline with edits or changes to its structure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.update_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#update_pipeline)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_action_executions"]
    ) -> ListActionExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_action_types"]
    ) -> ListActionTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pipeline_executions"]
    ) -> ListPipelineExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_executions"]
    ) -> ListRuleExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_webhooks"]) -> ListWebhooksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/#get_paginator)
        """

    async def __aenter__(self) -> "CodePipelineClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/client/)
        """
