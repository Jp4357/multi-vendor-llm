# Groq API Reference

## Auth
- Env var: `GROQ_API_KEY`
- Get key: https://console.groq.com/keys

## Install
```bash
pip install groq
```
Requires Python >= 3.10

## Key characteristic
Groq uses custom LPU (Language Processing Unit) hardware for extremely fast inference.
API is OpenAI-compatible — same request/response schema.

## Available Models (April 2026)

| Model ID                                  | Context | Best for              |
|-------------------------------------------|---------|-----------------------|
| `llama-3.3-70b-versatile`                 | 128k    | General, high quality |
| `llama-4-scout-17b-16e-instruct`          | 128k    | Fast, instruction     |
| `llama-3.1-8b-instant`                    | 128k    | Ultra fast, simple    |
| `allam-2-7b-instruct`                     | 32k     | Arabic + English      |
| `mixtral-8x7b-32768`                      | 32k     | Mixture of experts    |

Check https://console.groq.com/docs/models for the full current list.

## Text — Chat Completions

```python
from groq import Groq

client = Groq()  # reads GROQ_API_KEY from env

chat = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain LoRA fine-tuning"}],
    model="llama-3.3-70b-versatile"
)
print(chat.choices[0].message.content)
```

## Streaming

```python
stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="llama-3.3-70b-versatile",
    stream=True
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## Async client

```python
import asyncio
from groq import AsyncGroq

async def main():
    client = AsyncGroq()
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="llama-3.3-70b-versatile"
    )
    print(response.choices[0].message.content)
```

## Notes
- Text only — no image generation, TTS, or STT
- Very low latency (often 10-30x faster than GPT-4 equivalent quality)
- Free tier available with rate limits
- Tool/function calling supported on most models
