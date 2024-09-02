from openai import OpenAI

class OpenAIClient:
    def __init__(self, provider_keys):
        self.base = provider_keys.get('base', "https://api.openai.com/v1")
        self.api_key = provider_keys.get('api_key')

        self.client = OpenAI(
            base_url=self.base,
            api_key=self.api_key
        )
