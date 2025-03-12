from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from autogen_orchestrator.agents import (
    ACCOUNT_AGENT,
    CUSTOMER_AGENT,
    INVESTMENT_AGENT,
    SAVING_ACCOUNT_AGENT,
)
from autogen_orchestrator.output_format import output_format

message = f"""You are a bank assistant.
Your job is to break down complex tasks into smaller, manageable subtasks.

Your team members are:
    {ACCOUNT_AGENT}: provides account ID
    {SAVING_ACCOUNT_AGENT}: provides saving account balance
    {INVESTMENT_AGENT}: provides investment account balance

You only plan and delegate tasks - you do not execute them yourself.

When assigning tasks, use this format:
<agent> : <task>

After all tasks are complete. Do not ask user for any more questions.

Look into the chat history and gather all the information.
{output_format}
And, end with "TERMINATE".
"""


def agent(llm_client: AzureOpenAIChatCompletionClient, with_handoffs: bool = False):
    return AssistantAgent(
        CUSTOMER_AGENT,
        model_client=llm_client,
        description="A customer agent",
        system_message=message,
        handoffs=[ACCOUNT_AGENT, SAVING_ACCOUNT_AGENT] if with_handoffs else [],
    )
