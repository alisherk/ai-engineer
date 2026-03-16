import requests
from langchain_community.agent_toolkits import (
    FileManagementToolkit,  # Gives the LLM tools to read, write, and manage files
    PlayWrightBrowserToolkit,  # Wraps Playwright browser actions as LLM-callable tools
)
from langchain_community.tools.wikipedia.tool import (
    WikipediaQueryRun,  # A tool that allows the LLM to search and retrieve Wikipedia articles
)
from langchain_community.utilities import (
    GoogleSerperAPIWrapper,  # Wrapper for the Serper API — allows doing Google web searches programmatically
)
from langchain_community.utilities.wikipedia import (
    WikipediaAPIWrapper,  # Low-level Wikipedia API wrapper (used to configure WikipediaQueryRun)
)
from langchain_core.tools import (
    Tool,  # Base class for creating custom LangChain tools from plain Python functions
)
from langchain_experimental.tools import (
    PythonREPLTool,  # A tool that lets the LLM write and execute arbitrary Python code
)
from playwright.async_api import (
    async_playwright,  # Imports the async Playwright API for controlling a real browser
)

from src.app.settings import get_settings

settings = get_settings()

serper = (
    GoogleSerperAPIWrapper()
) 


async def playwright_tools():
    # Starts the Playwright engine asynchronously
    playwright = await async_playwright().start()
    # Runs Chromium in headless mode (no display required — needed in dev containers / servers without an X server)
    browser = await playwright.chromium.launch(headless=True)
    # Wraps the browser in a LangChain toolkit so LLMs can interact with it using tools that perform browser actions like clicking, typing, and navigating pages
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return (
        toolkit.get_tools(),
        browser,
        playwright,
    )


def push(text: str):
    """Send a push notification to the user"""
    requests.post(
        settings.pushover_api,
        data={
            "token": settings.pushover_token,
            "user": settings.pushover_user,
            "message": text,
        },
    )
    return "success"


def get_file_tools() -> list[Tool]:
    # Scopes file tools to sandbox/ directory, preventing access outside it
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools() -> list[Tool]:
    push_tool = Tool(
        name="send_push_notification",
        func=push,
        description="Use this tool when you want to send a push notification",
    )

    file_tools = get_file_tools()

    tool_search = Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search",  # Wraps Google search as a LangChain tool
    )

    # Creates the low-level Wikipedia API wrapper
    wikipedia = WikipediaAPIWrapper()
    # Creates a Wikipedia search tool for the LLM to use, which uses the WikipediaAPIWrapper to fetch and return Wikipedia articles based on search queries
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
    python_repl = PythonREPLTool()

    return file_tools + [
        push_tool,
        tool_search,
        python_repl,
        wiki_tool,
    ]
