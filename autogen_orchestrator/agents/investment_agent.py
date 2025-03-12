from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from autogen_orchestrator.agents import CUSTOMER_AGENT, INVESTMENT_AGENT
from autogen_orchestrator.tools.tools import (
    get_investment_account_balance,
)

message = "You are an investment account agent who can provide "
"information about the investment account balance. "
"Look at the chat history to understand the context of the conversation "
"and the account ID is in the it. Look for account ID and "
"use the tool provided to generate the investment account balance. "
"You are not allowed to ask for more question, just complete the task. "
"Your response SHOULD be in this format: "
"'The saving and investment account ID is <account id> and "
"the investment balance is <balance>'"


def agent(llm_client: AzureOpenAIChatCompletionClient, with_handoffs: bool = False):
    return AssistantAgent(
        INVESTMENT_AGENT,
        model_client=llm_client,
        description="An investment account agent.",
        tools=[get_investment_account_balance],
        system_message=message,
        handoffs=[CUSTOMER_AGENT] if with_handoffs else [],
    )
