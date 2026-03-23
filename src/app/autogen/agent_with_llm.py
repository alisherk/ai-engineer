import asyncio
from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.app.settings import get_settings

settings = get_settings()

@dataclass
class Message:
    content: str


class MyLLMAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("LLMAgent")
        model_client = OpenAIChatCompletionClient(model=settings.openai_model)
        self._delegate = AssistantAgent("LLMAgent", model_client=model_client)

    @message_handler
    async def handle_my_message_type(self, message: Message, ctx: MessageContext) -> Message:
        print(f"{self.id.type} received message: {message.content}")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        reply = response.chat_message.content
        print(f"{self.id.type} responded: {reply}")
        return Message(content=reply)

async def main():
    runtime = SingleThreadedAgentRuntime()
    await MyLLMAgent.register(runtime, "LLMAgent", lambda: MyLLMAgent())
    runtime.start()

    agent_id = AgentId("LLMAgent", "agent1")
    response = await runtime.send_message(Message("Hello, LLM Agent!"), agent_id)
    print("Final response from LLM Agent:", response.content)

    await runtime.stop()
    await runtime.close()


asyncio.run(main())