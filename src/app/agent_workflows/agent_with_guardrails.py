import asyncio

from pydantic import BaseModel
from agents.agent import Agent
from agents.guardrail import GuardrailFunctionOutput, input_guardrail, output_guardrail
from agents.run import Runner, RunContextWrapper
from agents.items import TResponseInputItem
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

from src.app.settings import get_settings

settings = get_settings()

# This is an example of how to use the input guardrail to prevent the agent from doing math homework. The guardrail checks if the user is asking the agent to do their math homework, and if so, it trips a tripwire and prevents the agent from answering the question.
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=settings.openai_model
)

@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )

agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
    model=settings.openai_model
)

async def run_agent_with_input_guardrail():
    # This should trip the guardrail
    try:
        output = await Runner.run(agent, "What is 2+2?")
        print("Guardrail didn't trip")
        print(output.final_output)

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped. You are not allowed to ask the agent to do your math homework!")

    
# This is an example of how to use the output guardrail to prevent the agent from doing math homework. The guardrail checks if the agent's output includes any math, and if so, it trips a tripwire and prevents the agent from answering the question.
class MessageOutput(BaseModel): 
    response: str

class MathOutput(BaseModel): 
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
    model=settings.openai_model
)

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent( 
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
    model=settings.openai_model
)

async def run_agent_with_output_guardrail():
    # This should trip the guardrail
    try:
        output = await Runner.run(agent, "What is 2+2?")
        print("Guardrail didn't trip")
        print(output.final_output)

    except OutputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped. Agent is not allowed to do math homework!")

asyncio.run(run_agent_with_output_guardrail())
