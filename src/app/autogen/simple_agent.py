import asyncio
from dataclasses import dataclass

from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    message_handler,
)

from src.app.settings import get_settings

settings = get_settings()


@dataclass
class Message:
    content: str


class SimpleAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("simple_agent")

    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext) -> Message:
        return Message(
            content=f"This is {self.id.type}-{self.id.key}. You said '{message.content}' and I disagree."
        )


async def main():
    runtime = SingleThreadedAgentRuntime()
    await SimpleAgent.register(runtime, "simple_agent", lambda: SimpleAgent())

    runtime.start()

    agent_id = AgentId("simple_agent", "alisher_agent")
    response = await runtime.send_message(Message("Well hi there!"), agent_id)
    print(">>>", response.content)

    await runtime.stop()
    await runtime.close()


asyncio.run(main())
