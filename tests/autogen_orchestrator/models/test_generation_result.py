from unittest.mock import MagicMock

from autogen_orchestrator.models.generation_result import GenerationResult, Usage


def test_usage_build():
    results = Usage.build(
        MagicMock(
            source="agent1",
            models_usage=MagicMock(prompt_tokens=10, completion_tokens=20),
        )
    )
    assert results.agent_name == "agent1"
    assert results.prompt_tokens == 10
    assert results.completion_tokens == 20


def test_generation_result_build():
    messages = [
        MagicMock(
            source="agent1",
            models_usage=MagicMock(prompt_tokens=10, completion_tokens=20),
        ),
        MagicMock(
            source="agent2",
            models_usage=MagicMock(prompt_tokens=15, completion_tokens=25),
        ),
        MagicMock(
            source="agent3",
            models_usage=None,
        ),
    ]
    results = GenerationResult.build("stop", messages)
    assert results.stop_reason == "stop"
    assert len(results.usages) == 2
    assert results.usages[0].agent_name == "agent1"
    assert results.usages[0].prompt_tokens == 10
    assert results.usages[0].completion_tokens == 20
    assert results.usages[1].agent_name == "agent2"
    assert results.usages[1].prompt_tokens == 15
    assert results.usages[1].completion_tokens == 25
