from src.app.settings import get_settings

settings = get_settings()

completed = []

descriptions = ["a", "b"]

completed.extend([False] * len(descriptions))

print(completed)
