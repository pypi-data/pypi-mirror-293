import openai
from ..exceptions import EthinaException

class OpenAIProvider:
    def __init__(self, api_key, base_url=None):
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def chat_completion(self, messages, model, **kwargs):
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return completion
        except Exception as e:
            raise EthinaException(f"OpenAI API error: {str(e)}")

    def stream_chat_completion(self, messages, model, **kwargs):
        try:
            for chunk in self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                **kwargs
            ):
                yield chunk
        except Exception as e:
            raise EthinaException(f"OpenAI API streaming error: {str(e)}")
