.PHONY: run-debate help

help:
	@echo "Available commands:"
	@echo "  make run-debate  - Run the debate crew"

run-debate:
	cd src/app/crew_ai/debate && crewai run
