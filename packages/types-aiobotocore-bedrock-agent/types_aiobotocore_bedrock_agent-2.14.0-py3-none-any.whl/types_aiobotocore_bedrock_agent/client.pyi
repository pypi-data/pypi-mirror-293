"""
Type annotations for bedrock-agent service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_agent.client import AgentsforBedrockClient

    session = get_session()
    async with session.create_client("bedrock-agent") as client:
        client: AgentsforBedrockClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionGroupSignatureType,
    ActionGroupStateType,
    DataDeletionPolicyType,
    KnowledgeBaseStateType,
)
from .paginator import (
    ListAgentActionGroupsPaginator,
    ListAgentAliasesPaginator,
    ListAgentKnowledgeBasesPaginator,
    ListAgentsPaginator,
    ListAgentVersionsPaginator,
    ListDataSourcesPaginator,
    ListFlowAliasesPaginator,
    ListFlowsPaginator,
    ListFlowVersionsPaginator,
    ListIngestionJobsPaginator,
    ListKnowledgeBasesPaginator,
    ListPromptsPaginator,
)
from .type_defs import (
    ActionGroupExecutorTypeDef,
    AgentAliasRoutingConfigurationListItemTypeDef,
    APISchemaTypeDef,
    AssociateAgentKnowledgeBaseResponseTypeDef,
    CreateAgentActionGroupResponseTypeDef,
    CreateAgentAliasResponseTypeDef,
    CreateAgentResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateFlowAliasResponseTypeDef,
    CreateFlowResponseTypeDef,
    CreateFlowVersionResponseTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    CreatePromptResponseTypeDef,
    CreatePromptVersionResponseTypeDef,
    DataSourceConfigurationUnionTypeDef,
    DeleteAgentAliasResponseTypeDef,
    DeleteAgentResponseTypeDef,
    DeleteAgentVersionResponseTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteFlowAliasResponseTypeDef,
    DeleteFlowResponseTypeDef,
    DeleteFlowVersionResponseTypeDef,
    DeleteKnowledgeBaseResponseTypeDef,
    DeletePromptResponseTypeDef,
    FlowAliasRoutingConfigurationListItemTypeDef,
    FlowDefinitionUnionTypeDef,
    FunctionSchemaUnionTypeDef,
    GetAgentActionGroupResponseTypeDef,
    GetAgentAliasResponseTypeDef,
    GetAgentKnowledgeBaseResponseTypeDef,
    GetAgentResponseTypeDef,
    GetAgentVersionResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetFlowAliasResponseTypeDef,
    GetFlowResponseTypeDef,
    GetFlowVersionResponseTypeDef,
    GetIngestionJobResponseTypeDef,
    GetKnowledgeBaseResponseTypeDef,
    GetPromptResponseTypeDef,
    GuardrailConfigurationTypeDef,
    IngestionJobFilterTypeDef,
    IngestionJobSortByTypeDef,
    KnowledgeBaseConfigurationTypeDef,
    ListAgentActionGroupsResponseTypeDef,
    ListAgentAliasesResponseTypeDef,
    ListAgentKnowledgeBasesResponseTypeDef,
    ListAgentsResponseTypeDef,
    ListAgentVersionsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFlowAliasesResponseTypeDef,
    ListFlowsResponseTypeDef,
    ListFlowVersionsResponseTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListPromptsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MemoryConfigurationUnionTypeDef,
    PrepareAgentResponseTypeDef,
    PrepareFlowResponseTypeDef,
    PromptOverrideConfigurationUnionTypeDef,
    PromptVariantUnionTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    StartIngestionJobResponseTypeDef,
    StorageConfigurationTypeDef,
    UpdateAgentActionGroupResponseTypeDef,
    UpdateAgentAliasResponseTypeDef,
    UpdateAgentKnowledgeBaseResponseTypeDef,
    UpdateAgentResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateFlowAliasResponseTypeDef,
    UpdateFlowResponseTypeDef,
    UpdateKnowledgeBaseResponseTypeDef,
    UpdatePromptResponseTypeDef,
    VectorIngestionConfigurationUnionTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AgentsforBedrockClient",)

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

class AgentsforBedrockClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentsforBedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#exceptions)
        """

    async def associate_agent_knowledge_base(
        self,
        *,
        agentId: str,
        agentVersion: str,
        description: str,
        knowledgeBaseId: str,
        knowledgeBaseState: KnowledgeBaseStateType = ...,
    ) -> AssociateAgentKnowledgeBaseResponseTypeDef:
        """
        Associates a knowledge base with an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.associate_agent_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#associate_agent_knowledge_base)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#close)
        """

    async def create_agent(
        self,
        *,
        agentName: str,
        agentResourceRoleArn: str = ...,
        clientToken: str = ...,
        customerEncryptionKeyArn: str = ...,
        description: str = ...,
        foundationModel: str = ...,
        guardrailConfiguration: GuardrailConfigurationTypeDef = ...,
        idleSessionTTLInSeconds: int = ...,
        instruction: str = ...,
        memoryConfiguration: MemoryConfigurationUnionTypeDef = ...,
        promptOverrideConfiguration: PromptOverrideConfigurationUnionTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateAgentResponseTypeDef:
        """
        Creates an agent that orchestrates interactions between foundation models, data
        sources, software applications, user conversations, and APIs to carry out tasks
        to help
        customers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_agent)
        """

    async def create_agent_action_group(
        self,
        *,
        actionGroupName: str,
        agentId: str,
        agentVersion: str,
        actionGroupExecutor: ActionGroupExecutorTypeDef = ...,
        actionGroupState: ActionGroupStateType = ...,
        apiSchema: APISchemaTypeDef = ...,
        clientToken: str = ...,
        description: str = ...,
        functionSchema: FunctionSchemaUnionTypeDef = ...,
        parentActionGroupSignature: ActionGroupSignatureType = ...,
    ) -> CreateAgentActionGroupResponseTypeDef:
        """
        Creates an action group for an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent_action_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_agent_action_group)
        """

    async def create_agent_alias(
        self,
        *,
        agentAliasName: str,
        agentId: str,
        clientToken: str = ...,
        description: str = ...,
        routingConfiguration: Sequence[AgentAliasRoutingConfigurationListItemTypeDef] = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateAgentAliasResponseTypeDef:
        """
        Creates an alias of an agent that can be used to deploy the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_agent_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_agent_alias)
        """

    async def create_data_source(
        self,
        *,
        dataSourceConfiguration: DataSourceConfigurationUnionTypeDef,
        knowledgeBaseId: str,
        name: str,
        clientToken: str = ...,
        dataDeletionPolicy: DataDeletionPolicyType = ...,
        description: str = ...,
        serverSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef = ...,
        vectorIngestionConfiguration: VectorIngestionConfigurationUnionTypeDef = ...,
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector for a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_data_source)
        """

    async def create_flow(
        self,
        *,
        executionRoleArn: str,
        name: str,
        clientToken: str = ...,
        customerEncryptionKeyArn: str = ...,
        definition: FlowDefinitionUnionTypeDef = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFlowResponseTypeDef:
        """
        Creates a prompt flow that you can use to send an input through various steps
        to yield an
        output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_flow)
        """

    async def create_flow_alias(
        self,
        *,
        flowIdentifier: str,
        name: str,
        routingConfiguration: Sequence[FlowAliasRoutingConfigurationListItemTypeDef],
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFlowAliasResponseTypeDef:
        """
        Creates an alias of a flow for deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_flow_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_flow_alias)
        """

    async def create_flow_version(
        self, *, flowIdentifier: str, clientToken: str = ..., description: str = ...
    ) -> CreateFlowVersionResponseTypeDef:
        """
        Creates a version of the flow that you can deploy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_flow_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_flow_version)
        """

    async def create_knowledge_base(
        self,
        *,
        knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef,
        name: str,
        roleArn: str,
        storageConfiguration: StorageConfigurationTypeDef,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Creates a knowledge base that contains data sources from which information can
        be queried and used by
        LLMs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_knowledge_base)
        """

    async def create_prompt(
        self,
        *,
        name: str,
        clientToken: str = ...,
        customerEncryptionKeyArn: str = ...,
        defaultVariant: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        variants: Sequence[PromptVariantUnionTypeDef] = ...,
    ) -> CreatePromptResponseTypeDef:
        """
        Creates a prompt in your prompt library that you can add to a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_prompt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_prompt)
        """

    async def create_prompt_version(
        self,
        *,
        promptIdentifier: str,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreatePromptVersionResponseTypeDef:
        """
        Creates a static snapshot of your prompt that can be deployed to production.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.create_prompt_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#create_prompt_version)
        """

    async def delete_agent(
        self, *, agentId: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteAgentResponseTypeDef:
        """
        Deletes an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_agent)
        """

    async def delete_agent_action_group(
        self,
        *,
        actionGroupId: str,
        agentId: str,
        agentVersion: str,
        skipResourceInUseCheck: bool = ...,
    ) -> Dict[str, Any]:
        """
        Deletes an action group in an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_action_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_agent_action_group)
        """

    async def delete_agent_alias(
        self, *, agentAliasId: str, agentId: str
    ) -> DeleteAgentAliasResponseTypeDef:
        """
        Deletes an alias of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_agent_alias)
        """

    async def delete_agent_version(
        self, *, agentId: str, agentVersion: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteAgentVersionResponseTypeDef:
        """
        Deletes a version of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_agent_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_agent_version)
        """

    async def delete_data_source(
        self, *, dataSourceId: str, knowledgeBaseId: str
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Deletes a data source from a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_data_source)
        """

    async def delete_flow(
        self, *, flowIdentifier: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteFlowResponseTypeDef:
        """
        Deletes a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_flow)
        """

    async def delete_flow_alias(
        self, *, aliasIdentifier: str, flowIdentifier: str
    ) -> DeleteFlowAliasResponseTypeDef:
        """
        Deletes an alias of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_flow_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_flow_alias)
        """

    async def delete_flow_version(
        self, *, flowIdentifier: str, flowVersion: str, skipResourceInUseCheck: bool = ...
    ) -> DeleteFlowVersionResponseTypeDef:
        """
        Deletes a version of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_flow_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_flow_version)
        """

    async def delete_knowledge_base(
        self, *, knowledgeBaseId: str
    ) -> DeleteKnowledgeBaseResponseTypeDef:
        """
        Deletes a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_knowledge_base)
        """

    async def delete_prompt(
        self, *, promptIdentifier: str, promptVersion: str = ...
    ) -> DeletePromptResponseTypeDef:
        """
        Deletes a prompt or a version of it, depending on whether you include the
        `promptVersion` field or
        not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.delete_prompt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#delete_prompt)
        """

    async def disassociate_agent_knowledge_base(
        self, *, agentId: str, agentVersion: str, knowledgeBaseId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a knowledge base from an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.disassociate_agent_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#disassociate_agent_knowledge_base)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#generate_presigned_url)
        """

    async def get_agent(self, *, agentId: str) -> GetAgentResponseTypeDef:
        """
        Gets information about an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_agent)
        """

    async def get_agent_action_group(
        self, *, actionGroupId: str, agentId: str, agentVersion: str
    ) -> GetAgentActionGroupResponseTypeDef:
        """
        Gets information about an action group for an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_action_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_agent_action_group)
        """

    async def get_agent_alias(
        self, *, agentAliasId: str, agentId: str
    ) -> GetAgentAliasResponseTypeDef:
        """
        Gets information about an alias of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_agent_alias)
        """

    async def get_agent_knowledge_base(
        self, *, agentId: str, agentVersion: str, knowledgeBaseId: str
    ) -> GetAgentKnowledgeBaseResponseTypeDef:
        """
        Gets information about a knowledge base associated with an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_agent_knowledge_base)
        """

    async def get_agent_version(
        self, *, agentId: str, agentVersion: str
    ) -> GetAgentVersionResponseTypeDef:
        """
        Gets details about a version of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_agent_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_agent_version)
        """

    async def get_data_source(
        self, *, dataSourceId: str, knowledgeBaseId: str
    ) -> GetDataSourceResponseTypeDef:
        """
        Gets information about a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_data_source)
        """

    async def get_flow(self, *, flowIdentifier: str) -> GetFlowResponseTypeDef:
        """
        Retrieves information about a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_flow)
        """

    async def get_flow_alias(
        self, *, aliasIdentifier: str, flowIdentifier: str
    ) -> GetFlowAliasResponseTypeDef:
        """
        Retrieves information about a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_flow_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_flow_alias)
        """

    async def get_flow_version(
        self, *, flowIdentifier: str, flowVersion: str
    ) -> GetFlowVersionResponseTypeDef:
        """
        Retrieves information about a version of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_flow_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_flow_version)
        """

    async def get_ingestion_job(
        self, *, dataSourceId: str, ingestionJobId: str, knowledgeBaseId: str
    ) -> GetIngestionJobResponseTypeDef:
        """
        Gets information about a ingestion job, in which a data source is added to a
        knowledge
        base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_ingestion_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_ingestion_job)
        """

    async def get_knowledge_base(self, *, knowledgeBaseId: str) -> GetKnowledgeBaseResponseTypeDef:
        """
        Gets information about a knoweldge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_knowledge_base)
        """

    async def get_prompt(
        self, *, promptIdentifier: str, promptVersion: str = ...
    ) -> GetPromptResponseTypeDef:
        """
        Retrieves information about the working draft ( `DRAFT` version) of a prompt or
        a version of it, depending on whether you include the `promptVersion` field or
        not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_prompt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_prompt)
        """

    async def list_agent_action_groups(
        self, *, agentId: str, agentVersion: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentActionGroupsResponseTypeDef:
        """
        Lists the action groups for an agent and information about each one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_action_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_agent_action_groups)
        """

    async def list_agent_aliases(
        self, *, agentId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentAliasesResponseTypeDef:
        """
        Lists the aliases of an agent and information about each one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_agent_aliases)
        """

    async def list_agent_knowledge_bases(
        self, *, agentId: str, agentVersion: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentKnowledgeBasesResponseTypeDef:
        """
        Lists knowledge bases associated with an agent and information about each one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_knowledge_bases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_agent_knowledge_bases)
        """

    async def list_agent_versions(
        self, *, agentId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentVersionsResponseTypeDef:
        """
        Lists the versions of an agent and information about each version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agent_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_agent_versions)
        """

    async def list_agents(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListAgentsResponseTypeDef:
        """
        Lists the agents belonging to an account and information about each agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_agents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_agents)
        """

    async def list_data_sources(
        self, *, knowledgeBaseId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data sources in a knowledge base and information about each one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_data_sources)
        """

    async def list_flow_aliases(
        self, *, flowIdentifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFlowAliasesResponseTypeDef:
        """
        Returns a list of aliases for a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_flow_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_flow_aliases)
        """

    async def list_flow_versions(
        self, *, flowIdentifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFlowVersionsResponseTypeDef:
        """
        Returns a list of information about each flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_flow_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_flow_versions)
        """

    async def list_flows(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListFlowsResponseTypeDef:
        """
        Returns a list of flows and information about each flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_flows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_flows)
        """

    async def list_ingestion_jobs(
        self,
        *,
        dataSourceId: str,
        knowledgeBaseId: str,
        filters: Sequence[IngestionJobFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: IngestionJobSortByTypeDef = ...,
    ) -> ListIngestionJobsResponseTypeDef:
        """
        Lists the ingestion jobs for a data source and information about each of them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_ingestion_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_ingestion_jobs)
        """

    async def list_knowledge_bases(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        Lists the knowledge bases in an account and information about each of them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_knowledge_bases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_knowledge_bases)
        """

    async def list_prompts(
        self, *, maxResults: int = ..., nextToken: str = ..., promptIdentifier: str = ...
    ) -> ListPromptsResponseTypeDef:
        """
        Returns either information about the working draft ( `DRAFT` version) of each
        prompt in an account, or information about of all versions of a prompt,
        depending on whether you include the `promptIdentifier` field or
        not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_prompts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_prompts)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all the tags for the resource you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#list_tags_for_resource)
        """

    async def prepare_agent(self, *, agentId: str) -> PrepareAgentResponseTypeDef:
        """
        Creates a `DRAFT` version of the agent that can be used for internal testing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.prepare_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#prepare_agent)
        """

    async def prepare_flow(self, *, flowIdentifier: str) -> PrepareFlowResponseTypeDef:
        """
        Prepares the `DRAFT` version of a flow so that it can be invoked.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.prepare_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#prepare_flow)
        """

    async def start_ingestion_job(
        self,
        *,
        dataSourceId: str,
        knowledgeBaseId: str,
        clientToken: str = ...,
        description: str = ...,
    ) -> StartIngestionJobResponseTypeDef:
        """
        Begins an ingestion job, in which a data source is added to a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.start_ingestion_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#start_ingestion_job)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associate tags with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#untag_resource)
        """

    async def update_agent(
        self,
        *,
        agentId: str,
        agentName: str,
        agentResourceRoleArn: str,
        foundationModel: str,
        customerEncryptionKeyArn: str = ...,
        description: str = ...,
        guardrailConfiguration: GuardrailConfigurationTypeDef = ...,
        idleSessionTTLInSeconds: int = ...,
        instruction: str = ...,
        memoryConfiguration: MemoryConfigurationUnionTypeDef = ...,
        promptOverrideConfiguration: PromptOverrideConfigurationUnionTypeDef = ...,
    ) -> UpdateAgentResponseTypeDef:
        """
        Updates the configuration of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_agent)
        """

    async def update_agent_action_group(
        self,
        *,
        actionGroupId: str,
        actionGroupName: str,
        agentId: str,
        agentVersion: str,
        actionGroupExecutor: ActionGroupExecutorTypeDef = ...,
        actionGroupState: ActionGroupStateType = ...,
        apiSchema: APISchemaTypeDef = ...,
        description: str = ...,
        functionSchema: FunctionSchemaUnionTypeDef = ...,
        parentActionGroupSignature: ActionGroupSignatureType = ...,
    ) -> UpdateAgentActionGroupResponseTypeDef:
        """
        Updates the configuration for an action group for an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_action_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_agent_action_group)
        """

    async def update_agent_alias(
        self,
        *,
        agentAliasId: str,
        agentAliasName: str,
        agentId: str,
        description: str = ...,
        routingConfiguration: Sequence[AgentAliasRoutingConfigurationListItemTypeDef] = ...,
    ) -> UpdateAgentAliasResponseTypeDef:
        """
        Updates configurations for an alias of an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_agent_alias)
        """

    async def update_agent_knowledge_base(
        self,
        *,
        agentId: str,
        agentVersion: str,
        knowledgeBaseId: str,
        description: str = ...,
        knowledgeBaseState: KnowledgeBaseStateType = ...,
    ) -> UpdateAgentKnowledgeBaseResponseTypeDef:
        """
        Updates the configuration for a knowledge base that has been associated with an
        agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_agent_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_agent_knowledge_base)
        """

    async def update_data_source(
        self,
        *,
        dataSourceConfiguration: DataSourceConfigurationUnionTypeDef,
        dataSourceId: str,
        knowledgeBaseId: str,
        name: str,
        dataDeletionPolicy: DataDeletionPolicyType = ...,
        description: str = ...,
        serverSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef = ...,
        vectorIngestionConfiguration: VectorIngestionConfigurationUnionTypeDef = ...,
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates the configurations for a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_data_source)
        """

    async def update_flow(
        self,
        *,
        executionRoleArn: str,
        flowIdentifier: str,
        name: str,
        customerEncryptionKeyArn: str = ...,
        definition: FlowDefinitionUnionTypeDef = ...,
        description: str = ...,
    ) -> UpdateFlowResponseTypeDef:
        """
        Modifies a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_flow)
        """

    async def update_flow_alias(
        self,
        *,
        aliasIdentifier: str,
        flowIdentifier: str,
        name: str,
        routingConfiguration: Sequence[FlowAliasRoutingConfigurationListItemTypeDef],
        description: str = ...,
    ) -> UpdateFlowAliasResponseTypeDef:
        """
        Modifies the alias of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_flow_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_flow_alias)
        """

    async def update_knowledge_base(
        self,
        *,
        knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef,
        knowledgeBaseId: str,
        name: str,
        roleArn: str,
        storageConfiguration: StorageConfigurationTypeDef,
        description: str = ...,
    ) -> UpdateKnowledgeBaseResponseTypeDef:
        """
        Updates the configuration of a knowledge base with the fields that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_knowledge_base)
        """

    async def update_prompt(
        self,
        *,
        name: str,
        promptIdentifier: str,
        customerEncryptionKeyArn: str = ...,
        defaultVariant: str = ...,
        description: str = ...,
        variants: Sequence[PromptVariantUnionTypeDef] = ...,
    ) -> UpdatePromptResponseTypeDef:
        """
        Modifies a prompt in your prompt library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.update_prompt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#update_prompt)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_action_groups"]
    ) -> ListAgentActionGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_aliases"]
    ) -> ListAgentAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_knowledge_bases"]
    ) -> ListAgentKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_versions"]
    ) -> ListAgentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agents"]) -> ListAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_flow_aliases"]
    ) -> ListFlowAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_flow_versions"]
    ) -> ListFlowVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_flows"]) -> ListFlowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ingestion_jobs"]
    ) -> ListIngestionJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_prompts"]) -> ListPromptsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/#get_paginator)
        """

    async def __aenter__(self) -> "AgentsforBedrockClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html#AgentsforBedrock.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/client/)
        """
