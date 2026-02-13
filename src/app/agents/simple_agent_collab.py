from typing import Dict
import asyncio

from agents import Agent, Runner, function_tool, trace
from openai.types.responses import ResponseTextDeltaEvent

from src.app.settings import get_settings

settings = get_settings()

@function_tool
async def send_test_email(email_content: str) -> dict:
    """A test tool that simulates sending an email."""
    print("Sending test email...")
    print(f"Email content:\n{email_content}")
    await asyncio.sleep(1)
    print("Test email sent!")
    return {"status": "success", "message": "Test email sent successfully."}


instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

sales_agent1 = Agent(
    name="Professional Sales Agent",
    instructions=instructions1,
    model=settings.openai_model,
)

sales_agent2 = Agent(
    name="Engaging Sales Agent", instructions=instructions2, model=settings.openai_model
)

sales_agent3 = Agent(
    name="Busy Sales Agent", instructions=instructions3, model=settings.openai_model
)


async def run_agent_one():
    result = Runner.run_streamed(sales_agent1, input="Write a cold sales email")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data.delta, end="", flush=True)


async def run_agents_in_parallel():
    message = "Write a cold sales email"

    with trace("Parallel cold emails"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )

    outputs = [result.final_output for result in results]

    for output in outputs:
        print(output + "\n\n")


sales_picker = Agent(
    name="sales_picker",
    instructions="You pick the best cold sales email from the given options. \
Imagine you are a customer and pick the one you are most likely to respond to. \
Do not give an explanation; reply with the selected email only.",
    model=settings.openai_model,
)


async def run_agent_collaboration():
    message = "Write a cold sales email"

    with trace("Collaborative cold email"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )

    outputs = [result.final_output for result in results]

    emails = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(outputs)

    picker_result = await Runner.run(sales_picker, emails)

    print(f"Best sales email:\n{picker_result.final_output}")


# Part 2 - Use of tools in agents
description = "Write a cold sales email"
# We can convert agents into tools and give them to other agents to use. This allows for more complex interactions and collaborations between agents, where they can call each other as tools to accomplish a task.
tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

tools = [tool1, tool2, tool3, send_test_email]

async def run_master_agent_with_tools():
    instructions = """
        You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
        
        Follow these steps carefully:
        1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
        
        2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
        
        3. Use the send_email tool to send the best email (and only the best email) to the user.
        
        Crucial Rules:
        - You must use the sales agent tools to generate the drafts — do not write them yourself.
        - You must send ONE email using the send_email tool — never more than one.
        """

    sales_manager = Agent(
        name="Sales Manager",
        instructions=instructions,
        tools=tools,
        model=settings.openai_model,
    )

    message = "Send a cold sales email addressed to 'Dear CEO'"

    with trace("Sales manager"):
        await Runner.run(sales_manager, message)


# Handoffs represent a way agent can delegate to another agent, passing control to it
# Handoff and Agent as tools are similar,
# With tools, control passes back to the original agent after the tool is done, while with handoffs, control is fully passed to the other agent and does not return

subject_instructions = "You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response."
subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model=settings.openai_model)
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."
html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model=settings.openai_model)
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

instructions = "You are an email formatter and sender. You receive the body of an email to be sent. \
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
Finally, you use the send_html_email tool to send the email with the subject and HTML body."

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    print("Sending email with subject:", subject)
    print("HTML body:", html_body)
    return {"status": "success"}

email_agent_tools = [subject_tool, html_tool, send_html_email]
emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_agent_tools,
    model=settings.openai_model,
    handoff_description="Convert an email to HTML and send it",
)


async def run_master_agent_with_handoffs():
    sales_manager_instructions = """
        You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
        
        Follow these steps carefully:
        1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
        
        2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
        You can use the tools multiple times if you're not satisfied with the results from the first try.
        
        3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
        
        Crucial Rules:
        - You must use the sales agent tools to generate the drafts — do not write them yourself.
        - You must hand off exactly ONE email to the Email Manager — never more than one.
        """

    sales_manager_tools = [tool1, tool2, tool3]
    handoffs = [emailer_agent]
    sales_manager = Agent(
        name="Sales Manager",
        instructions=sales_manager_instructions,
        tools=sales_manager_tools,
        handoffs=handoffs,
        model=settings.openai_model,
    )

    message = "Send out a cold sales email addressed to Dear CEO from Alice"

    with trace("Automated SDR"):
       result = await Runner.run(sales_manager, message)
       print("Final output from Sales Manager (should be from Email Manager):", result.final_output)


asyncio.run(run_master_agent_with_handoffs())