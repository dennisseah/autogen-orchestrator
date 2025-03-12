from typing import Sequence

import tabulate
from autogen_agentchat.messages import AgentEvent, ChatMessage
from pydantic import BaseModel


class Usage(BaseModel):
    agent_name: str
    prompt_tokens: int
    completion_tokens: int

    @staticmethod
    def build(message: AgentEvent | ChatMessage) -> "Usage":
        return Usage(
            agent_name=message.source,
            prompt_tokens=message.models_usage.prompt_tokens,  # type: ignore
            completion_tokens=message.models_usage.completion_tokens,  # type: ignore
        )


class GenerationResult(BaseModel):
    stop_reason: str | None
    usages: list[Usage]

    @staticmethod
    def build(
        stop_reason: str | None, messages: Sequence[AgentEvent | ChatMessage]
    ) -> "GenerationResult":
        usages = [Usage.build(msg) for msg in messages if msg.models_usage]

        return GenerationResult(stop_reason=stop_reason, usages=usages)

    def show(self) -> str:
        reason = f"Stop reason: {self.stop_reason}"
        data = {
            "Agent Name": [usage.agent_name for usage in self.usages],
            "Prompt Tokens": [usage.prompt_tokens for usage in self.usages],
            "Completion Tokens": [usage.completion_tokens for usage in self.usages],
        }
        return f"{reason}\n" + tabulate.tabulate(data, headers="keys")
