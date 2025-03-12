"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging
import os

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from autogen_orchestrator.protocols.i_azure_openai_service import IAzureOpenAIService
from autogen_orchestrator.protocols.i_orchestrator import IOrchestrator

load_dotenv(dotenv_path=".env")


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def logger() -> logging.Logger:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "ERROR"))
    logging.Formatter(fmt=" %(name)s :: %(levelname)-8s :: %(message)s")
    return logging.getLogger("autogen_selector")


@dependency_definition(container, singleton=True)
def azure_openai_service() -> IAzureOpenAIService:
    from autogen_orchestrator.services.azure_openai_service import (
        AzureOpenAIService,
    )

    return container[AzureOpenAIService]


@dependency_definition(container, singleton=True)
def orchestrator() -> IOrchestrator:
    type = os.getenv("ORCHESTRATOR_TYPE", "selector")

    if type == "swarm":
        from autogen_orchestrator.orchestrators.swarm_orchestrator import (
            SwarmOrchestrator,
        )

        return container[SwarmOrchestrator]

    if type == "round_robin":
        from autogen_orchestrator.orchestrators.round_robin_orchestrator import (
            RoundRobinOrchestrator,
        )

        return container[RoundRobinOrchestrator]

    from autogen_orchestrator.orchestrators.selector_orchestrator import (
        SelectorOrchestrator,
    )

    return container[SelectorOrchestrator]
