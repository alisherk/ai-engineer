import asyncio
from pathlib import Path

from autogen_core import AgentId
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime, GrpcWorkerAgentRuntimeHost

from src.app.autogen.agent_creator.creator import Creator
from src.app.autogen.agent_creator.message import Message

AGENTS = 2
CURRENT_DIR = Path(__file__).parent


async def create_and_message(
    worker: GrpcWorkerAgentRuntime, creator_id: AgentId, i: int
):
    try:
        result = await worker.send_message(Message(content=f"agent{i}.py"), creator_id)
        with open(CURRENT_DIR / f"idea{i}.md", "w") as f:
            f.write(result.content)
    except Exception as e:
        print(f"Failed to run worker {i} due to exception: {e}")


async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker.start()
    await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = AgentId("Creator", "default")
    coroutines = [
        create_and_message(worker, creator_id, i) for i in range(1, AGENTS + 1)
    ]
    await asyncio.gather(*coroutines)

    try:
        await worker.stop()
        await host.stop()

    except Exception as e:
        print(e)


asyncio.run(main())
