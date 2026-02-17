import asyncio

from agents.agent import Agent
from agents.run import Runner
from pydantic import BaseModel, ValidationError, field_validator

from src.app.settings import get_settings

settings = get_settings()

class Section(BaseModel):
    heading: str
    content: str

    @field_validator("heading")
    @classmethod
    def heading_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("heading cannot be empty")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        return v.strip()


class Metadata(BaseModel):
    author: str
    date: str | None = None

    @field_validator("author")
    @classmethod
    def author_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("author cannot be empty")
        return v.strip()


class MarkdownExtraction(BaseModel):
    title: str
    sections: list[Section]
    metadata: Metadata

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()

    @field_validator("sections")
    @classmethod
    def sections_not_empty(cls, v: list[Section]) -> list[Section]:
        if len(v) == 0:
            raise ValueError(
                "sections cannot be empty - must extract at least one section"
            )
        return v


agent = Agent(
    name="Markdown extractor",
    instructions="""Extract structured information from markdown text.
    
    You must extract:
    1. A title (the main heading)
    2. Sections with headings and content
    3. Metadata with author (required), and optionally date and tags
    
    Example output structure:
    {
        "title": "Getting Started Guide",
        "sections": [
            {"heading": "Introduction", "content": "This guide covers..."},
            {"heading": "Setup", "content": "First, install..."}
        ],
        "metadata": {
            "author": "John Doe", 
            "date": "2026-02-17",
            "tags": ["tutorial", "python"]
        }
    }
    """,
    output_type=MarkdownExtraction,
    model=settings.openai_model,
)


async def run_agent_with_valid_extraction():
    """Test cases showing both success and validation failures."""
    print("=" * 60)
    print("Test 1: Valid markdown extraction")
    print("=" * 60)
    markdown_input = """
    # Complete Guide to Python
    
    Author: Jane Smith
    Date: 2026-02-17
    
    ## Introduction
    Python is a versatile programming language.
    
    ## Getting Started
    Install Python from python.org.
    """
    try:
        result = await Runner.run(agent, markdown_input)
        print(f"\nFull output:\n{result.final_output.model_dump_json(indent=2)}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")

async def run_agent_with_invalid_extraction():
    print("\n" + "=" * 60)
    print("Test 2: Invalid input (no markdown structure)")
    print("=" * 60)

    try:
        result = await Runner.run(agent, "# Complete Guide to Python")
        print("✗ Validation didn't catch the error - unexpected!")
        print(result.final_output)
    except ValidationError as e:
        print("✓ Validation correctly failed!")
        print(f"Errors: {e.errors()}")
    except Exception as e:
        print(e)
        print(f"✓ Agent framework caught the issue: {type(e).__name__}")

asyncio.run(run_agent_with_valid_extraction())
