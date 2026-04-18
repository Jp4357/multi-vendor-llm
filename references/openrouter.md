# OpenRouter API Reference

## Auth
- Env var: `OPENROUTER_API_KEY`
- Get key: https://openrouter.ai/keys

## Install
```bash
pip install openai
```
OpenRouter uses the OpenAI SDK — just change `base_url`. No separate package needed.

## Key characteristic
OpenRouter is a unified gateway to 300+ models from OpenAI, Anthropic, Google, Meta, Mistral, and more.
Single API key, automatic fallback if a model is down, cost routing.

## Base URL
```
https://openrouter.ai/api/v1
```

## Available Models (sample — April 2026)

| Model ID                              | Provider    |
|---------------------------------------|-------------|
| `openai/gpt-4.1`                      | OpenAI      |
| `openai/gpt-4.1-nano`                 | OpenAI      |
| `anthropic/claude-sonnet-4-6`         | Anthropic   |
| `google/gemini-2.5-pro`               | Google      |
| `google/gemini-2.5-flash`             | Google      |
| `meta-llama/llama-4-scout`            | Meta        |
| `mistralai/mistral-large`             | Mistral     |

Full list: https://openrouter.ai/models

## Text — Chat Completions

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Explain RAG"}]
)
print(response.choices[0].message.content)
```

## Optional headers (recommended)

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    default_headers={
        "HTTP-Referer": "https://your-app.com",   # optional, shown in dashboard
        "X-Title": "My App"                        # optional
    }
)
```

## Fallback routing

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "route": "fallback",
        "models": ["anthropic/claude-sonnet-4-6", "google/gemini-2.5-flash"]
    }
)
```

## Notes
- Text only via standard chat completions
- Streaming: add `stream=True` — identical to OpenAI
- Pricing varies by model — check https://openrouter.ai/models for per-token costs
- Free models available (look for `:free` suffix)
