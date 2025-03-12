from dataclasses import dataclass

from autogen_agentchat.teams import SelectorGroupChat
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

selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the
next task.

Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.
"""


@dataclass
class SelectorOrchestrator(IOrchestrator):
    llm_client: IAzureOpenAIService

    def name(self) -> str:
        return "Selector Orchestrator"

    async def execute(self, task: str) -> GenerationResult:
        llm_model = self.llm_client.get_model()

        team = SelectorGroupChat(
            [
                customer_agent(llm_model),
                account_agent(llm_model),
                saving_account_agent(llm_model),
                investment_agent(llm_model),
            ],
            model_client=llm_model,
            termination_condition=get_termination_criteria(),
            selector_prompt=selector_prompt,
            allow_repeated_speaker=False,
        )
        result = await Console(team.run_stream(task=task))
        return GenerationResult.build(
            stop_reason=result.stop_reason, messages=result.messages
        )
