from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Coder:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],
            verbose=True,
            max_execution_time=30,
            max_retry_limit=3,
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config["coding_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
