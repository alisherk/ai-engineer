import json
from pathlib import Path

import requests
from openai import OpenAI
from pypdf import PdfReader

from src.app.settings import get_settings

SCRIPT_DIR = Path(__file__).parent

setting = get_settings()
openai = OpenAI(api_key=setting.openai_api_key)

def push(message: str):
    payload = {
        "user": setting.pushover_user,
        "token": setting.pushover_token,
        "message": message,
    }
    response = requests.post(setting.pushover_api, data=payload)
    if response.status_code != 200:
        print(f"Failed to send notification: {response.text}")


def record_user_details(email: str, name: str, notes: str):
    push(f"Recording user details: {email}, {name} and notes: {notes}")

    return {"recorded": "OK"}


def record_unknown_question(question: str):
    push(f"Recording unknown question: {question}")

    return {"recorded": "OK"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user",
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it",
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
            },
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

# in python we can access globals() to get a reference to the function by name, which is how we can dynamically call the tool function based on the tool call from the LLM
# example globals()["record_user_details"]("some questions") will give us a reference to the record_user_details function that we can then call with the arguments from the tool call
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})

    return results


linkedin = ""
for page in PdfReader(SCRIPT_DIR / "resume.pdf").pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open(SCRIPT_DIR / "summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Alisher Kabildjanov"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."


def chat(message, history):
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )
    done = False
    while not done:
        # This is the call to the LLM - see that we pass in the tools json
        response = openai.chat.completions.create(messages=messages, model=setting.openai_model, tools=tools)

        finish_reason = response.choices[0].finish_reason

        # If the LLM wants to call a tool, we do that!
        if finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            print("tool calls:", tool_calls, flush=True)
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True

    return response.choices[0].message.content

chat_history = []
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = chat(user_input, chat_history)
    print(f"{name}: {response}")
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

