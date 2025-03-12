from typing import Protocol

from autogen_orchestrator.models.generation_result import GenerationResult


class IOrchestrator(Protocol):
    def name(self) -> str: ...

    async def execute(self, task: str) -> GenerationResult: ...
