from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.memory import EntityMemory, LongTermMemory, ShortTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

from .tools.push_tool import PushNotificationTool


class TrendingCompany(BaseModel):
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")


class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany] = Field(
        description="List of companies trending in the news"
    )


class TrendingCompanyResearch(BaseModel):
    name: str = Field(description="Company name")
    market_position: str = Field(
        description="Current market position and competitive analysis"
    )
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(
        description="Investment potential and suitability for investment"
    )


class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(
        description="Comprehensive research on all trending companies"
    )


@CrewBase
class StockPicker:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],
            verbose=True,
            memory=True,
        )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"],
            output_file="output/trending_companies.json",
            output_pydantic=TrendingCompanyList,
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies"],
            output_file="output/trending_companies_research.json",
            output_pydantic=TrendingCompanyResearchList,
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            verbose=True,
            tools=[PushNotificationTool()],
            memory=True,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_company"],
        )

    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config=self.agents_config["manager"],
            allow_delegation=True,
            verbose=True,
        )

        short_term_memory = ShortTermMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small",
                    },
                },
                type="short_term",
                path="./memory/",
            ),
        )

        long_term_memory = LongTermMemory(
            storage=LTMSQLiteStorage(db_path="./memory/ltm.db"),
        )

        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small",
                    },
                },
                type="short_term",
                path="./memory/",
            )
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # why not sequential? We want the manager to be able to delegate tasks to the agents as needed, rather than having a fixed order of execution. This allows for more flexibility and adaptability in the crew's workflow.
            verbose=True,
            manager_agent=manager,
            memory=True,
            long_term_memory=long_term_memory,
            short_term_memory=short_term_memory,
            entity_memory=entity_memory,
        )
