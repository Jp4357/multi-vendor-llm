# Google Gemini API Reference

**Official docs:** https://ai.google.dev/gemini-api/docs/

## IMPORTANT: Use `google-genai`, NOT `google-generativeai`
The old `google-generativeai` SDK reached end-of-life on November 30, 2025.
Always use the new unified `google-genai` package.

## Auth
- Env var: `GEMINI_API_KEY`
- Get key: https://aistudio.google.com/app/apikey

## Install
```bash
pip install google-genai
```
Requires Python >= 3.10

## Text — Generate Content

**Models** (latest first):
- `gemini-2.5-pro` — most capable
- `gemini-2.5-flash` — fast, recommended default
- `gemini-2.0-flash` — stable, widely used

```python
from google import genai

client = genai.Client()  # reads GEMINI_API_KEY from env

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain transformers in ML"
)
print(response.text)
```

## Multi-turn Chat

```python
chat = client.chats.create(model="gemini-2.5-flash")
response = chat.send_message("Hello")
print(response.text)
response2 = chat.send_message("Follow up question")
print(response2.text)
```

## Image Input (Vision)

```python
import PIL.Image

img = PIL.Image.open("image.jpg")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Describe this image", img]
)
print(response.text)
```

## Image Generation (Imagen 4)

Three tiers available:
- `imagen-4.0-generate-001` — standard
- `imagen-4.0-ultra-generate-001` — highest quality
- `imagen-4.0-fast-generate-001` — fastest

Supports aspect ratios: 1:1, 3:4, 4:3, 9:16, 16:9. Generates 1-4 images per request. All images include SynthID watermark. Max prompt: 480 tokens, English only.

```python
from google.genai import types

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A futuristic city at night",
    config=types.GenerateImagesConfig(number_of_images=1)
)
for image in response.generated_images:
    image.image.save("output.png")
```

## Async client

```python
import asyncio
from google import genai

client = genai.Client()

async def main():
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello"
    )
    print(response.text)
```

## TTS (Text-to-Speech)

Three models available (all support single and multi-speaker):
- `gemini-3.1-flash-tts-preview`
- `gemini-2.5-flash-preview-tts`
- `gemini-2.5-pro-preview-tts`

30 voice options: Kore, Puck, Charon, Fenrir, Leda, and more. Auto-detects language (100+ supported). Output: PCM 24kHz mono 16-bit.

```python
import wave
from google.genai import types

# Single speaker
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Have a wonderful day!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
            )
        ),
    ),
)
pcm = response.candidates[0].content.parts[0].inline_data.data
with wave.open("out.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(pcm)
```

## Live API (Real-time Voice)

WebSocket-based streaming for real-time voice agents. Supports barge-in (interruption), audio transcription, 70 languages, affective dialogue.

- Input: raw PCM 16-bit 16kHz audio, JPEG images, text
- Output: raw PCM 16-bit 24kHz audio
- Connect via WSS; supports server-to-server and client-to-server modes

```python
# Live API uses a different async WebSocket interface — see:
# https://ai.google.dev/gemini-api/docs/live
```

## Notes
- TTS supported via `gemini-2.5-flash-preview-tts` and others (see above)
- No STT/transcription as a standalone API — use Live API for real-time voice input
- Streaming: use `client.models.generate_content_stream(...)`
- System instructions: pass via `config=types.GenerateContentConfig(system_instruction="...")`
