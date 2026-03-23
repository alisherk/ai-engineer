import importlib
import logging
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import (
    TRACE_LOGGER_NAME,
    AgentId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.app.autogen.agent_creator.message import Message
from src.app.settings import get_settings

settings = get_settings()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

CURRENT_DIR = Path(__file__).parent

class Creator(RoutedAgent):
    system_message = """
    You are an Agent that is able to create new AI Agents.
    You receive a template in the form of Python code that creates an Agent using Autogen Core and Autogen Agentchat.
    You should use this template to create a new Agent with a unique system message that is different from the template,
    and reflects their unique characteristics, interests and goals.
    You can choose to keep their overall goal the same, or change it.
    You can choose to take this Agent in a completely different direction. The only requirement is that the class must be named Agent,
    and it must inherit from RoutedAgent and have an __init__ method that takes a name parameter.
    Also avoid environmental interests - try to mix up the business verticals so that every agent is different.
    Respond only with the python code, no other text, and no markdown code blocks.
    Please set BOUNCE_THRESHOLD to a value between 0 and 1 that determines how likely the agent is to bounce its business idea off another agent for feedback and improvement.
    """

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model=settings.openai_model)
        self._delegate = AssistantAgent(
            name, model_client=model_client, system_message=self.system_message
        )

    def get_user_prompt(self):
        prompt = (
            "Please generate a new Agent based strictly on this template. Stick to the class structure. \
            Respond only with the python code, no other text, and no markdown code blocks.\n\n\
            Be creative about taking the agent in a new direction, but don't change method signatures.\n\n\
            Here is the template:\n\n"
        )
        with open(CURRENT_DIR / "agent.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template

    @message_handler
    async def handle_my_message_type(
        self, message: Message, ctx: MessageContext
    ) -> Message:
        filename = message.content
        agent_name = filename.split(".")[0]
        text_message = TextMessage(content=self.get_user_prompt(), source="user")
        response = await self._delegate.on_messages(
            [text_message], ctx.cancellation_token
        )

        with open(CURRENT_DIR / filename, "w", encoding="utf-8") as f:
            f.write(response.chat_message.content)
        print(
            f"** Creator has created python code for agent {agent_name} - about to register with Runtime"
        )

        module = importlib.import_module(agent_name)
        await module.Agent.register(
            self.runtime, agent_name, lambda: module.Agent(agent_name)
        )
        logger.info(f"** Agent {agent_name} is live")

        result = await self.send_message(
            Message(content="Give me an idea"), AgentId(agent_name, "default")
        )

        return Message(content=result.content)
