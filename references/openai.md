# OpenAI API Reference

## Auth
- Env var: `OPENAI_API_KEY`
- Get key: https://platform.openai.com/api-keys

## Install
```bash
pip install openai
```
SDK version: 2.x (latest 2.32.0 as of April 2026)

## Text — Chat Completions

**Models** (latest first):
- `gpt-4.1` — most capable
- `gpt-4.1-mini` — fast, cheap
- `gpt-4o` — multimodal (text + image input)
- `gpt-4o-mini` — fast multimodal

```python
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY from env

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Image Generation

**Models**:
- `gpt-image-1.5` — latest (April 2026)
- `dall-e-3` — stable, widely used

```python
response = client.images.generate(
    model="gpt-image-1.5",
    prompt="A futuristic city",
    n=1,
    size="1024x1024"
)
print(response.data[0].url)
```

## Text-to-Speech (TTS)

**Models**: `tts-1`, `tts-1-hd`
**Voices**: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

```python
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world"
)
response.stream_to_file("output.mp3")
```

## Speech-to-Text (Whisper / STT)

**Model**: `whisper-1`

```python
with open("audio.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )
print(transcript.text)
```

## Async client

```python
from openai import AsyncOpenAI
client = AsyncOpenAI()
response = await client.chat.completions.create(...)
```

## Notes
- All requests require `OPENAI_API_KEY` in environment
- Streaming: add `stream=True` to chat completions
- Vision: pass image URLs in message content as `{"type": "image_url", "image_url": {"url": "..."}}`
