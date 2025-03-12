from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination,
)


def get_termination_criteria(max_messages: int = 25) -> TerminationCondition:
    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=max_messages)
    return text_mention_termination | max_messages_termination
