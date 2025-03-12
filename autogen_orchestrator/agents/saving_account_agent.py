from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from autogen_orchestrator.agents import (
    INVESTMENT_AGENT,
    SAVING_ACCOUNT_AGENT,
)
from autogen_orchestrator.tools.tools import (
    get_saving_account_balance,
)

message = "You are a saving account agent who can provide "
"information about the saving account balance. "
"Look at the chat history to understand the context of the conversation "
"and the account ID is in the it. Look for account ID and "
"use the tool provided to generate the saving account balance. "
"You are not allowed to ask for more question, just complete the task. "
"Your response SHOULD be in this format: "
"'The saving and investment account ID is <account id> and "
"the saving account balance is <balance>"


def agent(llm_client: AzureOpenAIChatCompletionClient, with_handoffs: bool = False):
    return AssistantAgent(
        SAVING_ACCOUNT_AGENT,
        model_client=llm_client,
        description="An saving account agent.",
        tools=[get_saving_account_balance],
        system_message=message,
        handoffs=[INVESTMENT_AGENT] if with_handoffs else [],
    )
