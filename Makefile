.PHONY: debate-run help

help:
	@echo "Available commands:"
	@echo "  make debater-run  - Run the CrewAI debate program"
	@echo "  make researcher-run  - Run the CrewAI financial researcher program"

debater-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/debate && uv run crewai run

researcher-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/financial_researcher && uv run crewai run
