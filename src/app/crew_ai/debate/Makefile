.PHONY: install run train replay test help

help:
	@echo "Available commands:"
	@echo "  make install     - Install the debate package in editable mode"
	@echo "  make run         - Run the debate crew"
	@echo "  make train       - Train the debate crew"
	@echo "  make replay      - Replay the debate crew"
	@echo "  make test        - Test the debate crew"

install:
	uv pip install -e .

run:
	cd src && uv run python -m debate.main

train:
	cd src && uv run python -c "from debate.main import train; train()"

replay:
	cd src && uv run python -c "from debate.main import replay; replay()"

test:
	cd src && uv run python -c "from debate.main import test; test()"
