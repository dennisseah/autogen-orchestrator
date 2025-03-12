import argparse
import asyncio
import os

from autogen_orchestrator.hosting import container
from autogen_orchestrator.protocols.i_orchestrator import IOrchestrator

task = "Get the account ID and then get the saving balance "
"and investment balance. Both saving and investment account have "
"the same account ID. Sum thes balances when they are available."


async def main():
    parser = argparse.ArgumentParser(prog="Orchestrator")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["selector", "round_robin", "swarm"],
        default="selector",
    )
    args = parser.parse_args()
    os.environ["ORCHESTRATOR_TYPE"] = args.type

    orchestrator = container[IOrchestrator]

    print(orchestrator.name())
    result = await orchestrator.execute(task)
    print(result.show())


if __name__ == "__main__":
    asyncio.run(main())
