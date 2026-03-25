.PHONY: debate-run help install

help:
	@echo "Available commands:"
	@echo "  make install         - Install all dependencies and Playwright browsers"
	@echo "  make debater-run  - Run the CrewAI debate program"
	@echo "  make researcher-run  - Run the CrewAI financial researcher program"
	@echo "  make stock-picker-run  - Run the CrewAI stock picker program"
	@echo "  make coder-run  - Run the CrewAI coder program"

install:
	uv sync
	uv run playwright install chromium
	uv run playwright install-deps chromium

debater-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/debate && uv run crewai run

researcher-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/financial_researcher && uv run crewai run

stock-picker-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/stock_picker && uv run crewai run

coder-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/coder && uv run crewai run

eng-team-run:
	export $$(cat .env | xargs) && cd src/app/crew_ai/eng_team && uv run crewai run
