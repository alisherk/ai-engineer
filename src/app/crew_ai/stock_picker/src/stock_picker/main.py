#!/usr/bin/env python

from stock_picker.crew import StockPicker

def run():
    inputs = {
        "sector": "Technology",
    }

    try:
        result = StockPicker().crew().kickoff(inputs=inputs)

        print("\n\n== Final decision ==")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

