from openai import AzureOpenAI

class AzureOpenAIClient:
    def __init__(self, provider_keys):
        self.base = provider_keys.get('base')
        self.api_key = provider_keys.get('api_key')
        self.api_version = provider_keys.get('api_version', "2024-05-01-preview")

        self.client = AzureOpenAI(
            azure_endpoint=self.base,
            api_key=self.api_key,
            api_version=self.api_version
        )
