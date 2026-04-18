# Anthropic API Reference

**Official docs:** https://platform.claude.com/docs

## Auth
- Env var: `ANTHROPIC_API_KEY`
- Get key: https://console.anthropic.com/settings/keys

## Install
```bash
pip install anthropic
```
Requires Python >= 3.9

## Available Models (April 2026)

| Model ID                          | Best for                        | Context  | Input $/MTok | Output $/MTok |
|-----------------------------------|---------------------------------|----------|--------------|---------------|
| `claude-opus-4-7`                 | Most complex, agentic coding    | 1M tokens | $5          | $25           |
| `claude-sonnet-4-6`               | Balanced performance/cost       | 1M tokens | $3          | $15           |
| `claude-haiku-4-5-20251001`       | Fast, lightweight tasks         | 200k tokens | $1        | $5            |

All models support: text input, image input (vision), text output, multilingual, tool use.
No TTS, STT, or image generation support.

## Text — Messages API

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain attention mechanisms"}
    ]
)
print(message.content[0].text)
```

## System prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a helpful AI research assistant.",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Vision (image input)

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
            {"type": "text", "text": "What is in this image?"}
        ]
    }]
)
```

## Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Async client

```python
import asyncio
import anthropic

async def main():
    client = anthropic.AsyncAnthropic()
    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(message.content[0].text)
```

## Notes
- No image generation, TTS, or STT support
- Prompt caching available for repeated context — reduces cost significantly
- `max_tokens` is required for all requests
