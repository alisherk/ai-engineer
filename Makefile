.PHONY: debate-run help

help:
	@echo "Available commands:"
	@echo "  make debate-run  - Run the CrewAI debate program"

debate-run:
	cd src/app/crew_ai/debate && uv run crewai run
