from dataclasses import dataclass

from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console

from autogen_orchestrator.agents.account_agent import agent as account_agent
from autogen_orchestrator.agents.customer_agent import agent as customer_agent
from autogen_orchestrator.agents.investment_agent import agent as investment_agent
from autogen_orchestrator.agents.saving_account_agent import (
    agent as saving_account_agent,
)
from autogen_orchestrator.models.generation_result import GenerationResult
from autogen_orchestrator.protocols.i_azure_openai_service import IAzureOpenAIService
from autogen_orchestrator.protocols.i_orchestrator import IOrchestrator
from autogen_orchestrator.termination import get_termination_criteria


@dataclass
class SwarmOrchestrator(IOrchestrator):
    llm_client: IAzureOpenAIService

    def name(self) -> str:
        return "Swarm Orchestrator"

    async def execute(self, task: str) -> GenerationResult:
        llm_model = self.llm_client.get_model()

        team = Swarm(
            participants=[
                customer_agent(llm_model, with_handoffs=True),
                account_agent(llm_model, with_handoffs=True),
                saving_account_agent(llm_model, with_handoffs=True),
                investment_agent(llm_model, with_handoffs=True),
            ],
            termination_condition=get_termination_criteria(max_messages=50),
        )
        result = await Console(team.run_stream(task=task))
        return GenerationResult.build(
            stop_reason=result.stop_reason, messages=result.messages
        )
