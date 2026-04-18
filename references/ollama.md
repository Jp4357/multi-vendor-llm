# Ollama API Reference

## Auth
- No API key needed — Ollama runs locally
- Default host: `http://localhost:11434`

## Install

1. Install Ollama: https://ollama.com/download
2. Install Python client:
```bash
pip install ollama
```

## Pull a model first
```bash
ollama pull llama3.2
ollama pull gemma3
ollama pull qwen2.5
```

## Available Models (popular choices)

| Model           | Pull command             | Size   | Best for         |
|-----------------|--------------------------|--------|------------------|
| `llama3.2`      | `ollama pull llama3.2`   | 2GB    | General purpose  |
| `llama3.3`      | `ollama pull llama3.3`   | 43GB   | High quality     |
| `gemma3`        | `ollama pull gemma3`     | 5GB    | Google's model   |
| `qwen2.5`       | `ollama pull qwen2.5`    | 4.7GB  | Multilingual     |
| `deepseek-r1`   | `ollama pull deepseek-r1`| 4.7GB  | Reasoning        |
| `phi4`          | `ollama pull phi4`       | 9GB    | Microsoft, small |

Full list: https://ollama.com/library

## Text — Chat (ollama SDK)

```python
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explain transformers"}]
)
print(response.message.content)
```

## Streaming

```python
stream = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)
for chunk in stream:
    print(chunk.message.content, end="", flush=True)
```

## Custom host

```python
client = ollama.Client(host="http://192.168.1.10:11434")
response = client.chat(model="llama3.2", messages=[...])
```

## OpenAI-compatible API (alternative)

Ollama also exposes an OpenAI-compatible endpoint at `/v1/`:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # required by SDK but not checked
)
response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Async client

```python
import asyncio
import ollama

async def main():
    client = ollama.AsyncClient()
    response = await client.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.message.content)
```

## Notes
- Text only — no image generation, TTS, or STT
- Completely local — no data sent to the cloud
- Must have the model pulled before using (`ollama pull <model>`)
- Check running models: `ollama list`
