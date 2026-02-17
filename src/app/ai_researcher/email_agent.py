from typing import Dict

from agents.agent import Agent
from agents.tool import function_tool

from src.app.ai_researcher.agent_name_enum import AgentNames
from src.app.settings import get_settings

settings = get_settings()

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    print(f"Sending email with subject: {subject}")
    print(f"Email body (HTML): {html_body}")
    return {"success": "Email sent successfully!"}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name=AgentNames.EMAIL_AGENT.value,
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=settings.openai_model,
)
