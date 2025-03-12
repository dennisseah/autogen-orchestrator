from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from autogen_orchestrator.agents import (
    ACCOUNT_AGENT,
    CUSTOMER_AGENT,
)
from autogen_orchestrator.tools.tools import get_bank_account_id

message = "You are an account agent who can provide account ID. "
"You should always use the tool provided to generate the account balance. "
"You are not allowed to ask for more question, just complete the task. "
"In your response it is important to state that the The account ID for saving "
"and investment accounts are the same ID. Return the account ID in the response"
"in this format: 'The saving and investment account ID is: <account_id>'."


def agent(llm_client: AzureOpenAIChatCompletionClient, with_handoffs: bool = False):
    return AssistantAgent(
        ACCOUNT_AGENT,
        model_client=llm_client,
        description="An account agent.",
        tools=[get_bank_account_id],
        system_message=message,
        handoffs=[CUSTOMER_AGENT] if with_handoffs else [],
    )
