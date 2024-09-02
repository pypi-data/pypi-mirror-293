class AzureOpenAIChat:
    def __init__(self, client):
        self.client = client

    def generate(self, input_data):
        response = self.client.client.chat.completions.create(
            model=input_data['model'],
            messages=input_data['messages'],
            temperature=input_data.get('temperature', 0.7),
            max_tokens=input_data.get('max_tokens', 800),
            top_p=input_data.get('top_p', 0.95),
            frequency_penalty=input_data.get('frequency_penalty', 0),
            presence_penalty=input_data.get('presence_penalty', 0),
            stop=input_data.get('stop_sequences'),
            stream=input_data.get('stream', False)
        )

        if input_data.get('stream', False):
            return self._stream_response(response)
        else:
            return self._format_response(response)

    def _stream_response(self, response):
        for chunk in response:
            yield {
                "data": {
                    "chunk": chunk.choices[0].delta.content,
                    "chunk_index": chunk.choices[0].index,
                    "function_call": chunk.choices[0].delta.function_call
                }
            }

    def _format_response(self, response):
        return {
            "data": {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "function_call": response.choices[0].message.function_call
            }
        }
