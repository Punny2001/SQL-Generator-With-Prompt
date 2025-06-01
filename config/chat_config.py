import os

class ChatConfig:
    api_key: str
    model_name: str
    temperature: float
    max_tokens: int

    def __init__(self):
        self.api_key = os.getenv("API_KEY", "")
        self.model_name = "gpt-4-turbo"
        self.temperature = 0
        self.max_tokens = 300

