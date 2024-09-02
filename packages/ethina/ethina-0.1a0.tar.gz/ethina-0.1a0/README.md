## WORK IN PROGRESS | PLEASE DO NOT USE YET !!
I am still working on this, I don't have the package built yet, I recommend not to use this yet. I haven't tested it thoroughly, and will most probably break.

# Ethina

Ethina is a powerful Python package that provides a unified interface for interacting with various Language Model (LLM) providers such as OpenAI, Anthropic, AWS Bedrock, Azure AI, Azure OpenAI, Google, and Ollama.

## Features

- Unified API for multiple LLM providers
- Supports both streaming and non-streaming responses
- Easy-to-use client generation
- Consistent input and output formats across providers
- Customizable parameters for LLM interactions

## Installation

To install Ethina, use pip:


```bash
pip install ethina
```

## Quick Start

Here's a quick example using Azure OpenAI:


```python
from ethina import AzureOpenAIClient, AzureOpenAIChat

# Create client
provider_keys = {
    "base": "https://your-resource-name.openai.azure.com/",
    "api_key": "your-api-key",
    "api_version": "2024-05-01-preview"
}
client = AzureOpenAIClient(provider_keys)


# Create chat object
chat = AzureOpenAIChat(client)

# Prepare input data
input_data = {
    "model": "your-deployment-name",
    "messages": [
        {"role": "user", "content": "What is Ethina?"}
    ],
    "max_tokens": 800,
    "temperature": 0.7
}

# Generate response
response = chat.generate(input_data)
print(response)
```

## Supported Providers

- OpenAI
- Azure OpenAI
- Anthropic
- AWS Bedrock
- Azure AI
- Google
- Ollama

## Documentation

For detailed usage instructions and API reference, please refer to the [documentation](#).

## Contributing

We welcome contributions! Please see our [Contributing Guide](#) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



This version includes a more structured format, consistent code block styles, and links placeholders for documentation and contributing guide. Adjust the links as needed based on your actual documentation and contributing guide URLs.
