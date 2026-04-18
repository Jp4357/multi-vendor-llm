"""
Google Gemini client — text and image generation.
Requires: pip install google-genai python-dotenv
Env var:  GEMINI_API_KEY (loaded from .env automatically)
NOTE: Use google-genai, NOT google-generativeai (deprecated since Nov 2025)
"""
import os
from typing import Generator
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # loads GEMINI_API_KEY from .env file

_client = genai.Client()  # reads GEMINI_API_KEY from environment

DEFAULT_CHAT_MODEL = "gemini-2.5-flash"
DEFAULT_IMAGE_MODEL = "imagen-4.0-generate-001"


# ── Single-shot ───────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_CHAT_MODEL, system: str = None, **kwargs) -> str:
    """Send a single prompt and return the full reply as a string."""
    config = types.GenerateContentConfig(system_instruction=system) if system else None
    response = _client.models.generate_content(model=model, contents=prompt, config=config, **kwargs)
    return response.text


def stream_chat(prompt: str, model: str = DEFAULT_CHAT_MODEL, system: str = None, **kwargs) -> Generator[str, None, None]:
    """Stream a single prompt. Yields text chunks as they arrive."""
    config = types.GenerateContentConfig(system_instruction=system) if system else None
    for chunk in _client.models.generate_content_stream(model=model, contents=prompt, config=config, **kwargs):
        if chunk.text:
            yield chunk.text


# ── Multi-turn session ────────────────────────────────────────────────────────

class ChatSession:
    """Stateful multi-turn conversation using Gemini's native chat API."""

    def __init__(self, model: str = DEFAULT_CHAT_MODEL, system: str = None):
        self.model = model
        self._system = system
        self._session = self._new_session()

    def _new_session(self):
        config = types.GenerateContentConfig(system_instruction=self._system) if self._system else None
        return _client.chats.create(model=self.model, config=config)

    @property
    def history(self) -> list:
        return self._session.get_history()

    def reset(self):
        """Start a fresh session (clears history, keeps system prompt)."""
        self._session = self._new_session()

    def chat(self, prompt: str, **kwargs) -> str:
        """Send a message and return the full reply."""
        response = self._session.send_message(prompt, **kwargs)
        return response.text

    def stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream a message. Yields text chunks as they arrive."""
        for chunk in self._session.send_message_stream(prompt, **kwargs):
            if chunk.text:
                yield chunk.text


# ── Image ─────────────────────────────────────────────────────────────────────

def generate_image(prompt: str, model: str = DEFAULT_IMAGE_MODEL, number_of_images: int = 1, output_dir: str = ".") -> list[str]:
    """Generate image(s) via Imagen and save to disk. Returns list of saved file paths."""
    response = _client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=number_of_images)
    )
    paths = []
    for i, generated in enumerate(response.generated_images):
        path = f"{output_dir}/generated_{i}.png"
        generated.image.save(path)
        paths.append(path)
    return paths


def text_to_speech(text: str, output_path: str = "out.wav", voice_name: str = "Kore") -> str:
    """Convert text to speech using Gemini TTS, save as WAV, return the output path."""
    import wave
    response = _client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                )
            ),
        ),
    )
    pcm = response.candidates[0].content.parts[0].inline_data.data
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)
    return output_path


def transcribe(audio_path: str, **kwargs) -> str:
    raise NotImplementedError("Gemini API does not support STT/transcription as of April 2026.")


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("GEMINI_API_KEY")
    if not key or key == "your-api-key-here":
        print("ERROR: GEMINI_API_KEY is not set. Add it to your .env file.")
    else:
        print("OK: GEMINI_API_KEY is set.")
        print("Run your code to make your first API call.")
