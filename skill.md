---
name: multi-vendor-llm
version: 1.1.0
author: jyotiprakash
description: |
  Sets up and generates Python client code for LLM vendor APIs.
  Trigger when the user wants to: use OpenAI / Gemini / Anthropic / Groq /
  OpenRouter / Ollama; make text completions, generate images, do TTS or
  speech transcription; set up API keys; or switch/compare between LLM providers.
  Generates ready-to-run Python client files per vendor with text/image/voice functions.
---

# Multi-Vendor LLM Skill

This skill generates ready-to-run Python client files for LLM vendor APIs.
Each client exposes a consistent interface: `chat()`, `generate_image()`, `text_to_speech()`, `transcribe()`.

## Supported vendors

| Vendor      | Text | Image | TTS | STT | Package            |
|-------------|------|-------|-----|-----|--------------------|
| OpenAI      | ✓    | ✓     | ✓   | ✓   | `openai`           |
| Gemini      | ✓    | ✓     | ✓   | -   | `google-genai`     |
| Anthropic   | ✓    | -     | -   | -   | `anthropic`        |
| Groq        | ✓    | -     | -   | -   | `groq`             |
| OpenRouter  | ✓    | -     | -   | -   | `openai`           |
| Ollama      | ✓    | -     | -   | -   | `ollama`           |

## Workflow

When the user invokes this skill:

1. **Identify vendor(s)** — determine which vendor(s) the user wants. Ask if ambiguous.
2. **Ask which features** — ALWAYS ask the user which features they need before generating. Present as a checklist:
   - Chat (text completions + streaming + multi-turn session)
   - Image generation
   - Text-to-speech (TTS)
   - Speech-to-text / transcription (STT)
   Only generate code for the features the user selects. If they say "all", include everything.
3. **API key setup** — NEVER touch or create the user's `.env` file. Instead:
   - Create a `.env.example` file (if one doesn't exist) showing which key(s) are needed
   - Tell the user: "Add your API key to `.env` — copy `.env.example` as a reference"
   - Key names by vendor:
     - OpenAI: `OPENAI_API_KEY`
     - Gemini: `GEMINI_API_KEY`
     - Anthropic: `ANTHROPIC_API_KEY`
     - Groq: `GROQ_API_KEY`
     - OpenRouter: `OPENROUTER_API_KEY`
     - Ollama: `OLLAMA_API_KEY` (optional — omit for local mode, set for cloud API)
   - The generated client file uses `load_dotenv()` to read from `.env` automatically
4. **Generate client file** — read the matching template from `templates/`, strip out any sections for unselected features, add dotenv loading at the top, and write it into the user's current working directory (e.g. `openai_client.py`)
5. **Customize** — adjust the default model or parameters if the user specified any
6. **requirements.txt** — add the required packages to `requirements.txt` in the project root (create it if missing, append if it already exists — never duplicate existing entries). Always include `python-dotenv`. Packages per vendor:
   - OpenAI: `openai`
   - Gemini: `google-genai`
   - Anthropic: `anthropic`
   - Groq: `groq`
   - OpenRouter: `openai`
   - Ollama: `ollama`
   Then tell the user: "Run `pip install -r requirements.txt` to install dependencies."
   NEVER run `pip install` directly.
7. **Report** — show what was created and a usage example

## Reference docs

Load these into context as needed:
- [references/openai.md](references/openai.md)
- [references/gemini.md](references/gemini.md)
- [references/anthropic.md](references/anthropic.md)
- [references/groq.md](references/groq.md)
- [references/openrouter.md](references/openrouter.md)
- [references/ollama.md](references/ollama.md)

## Template files

Copy from these into the user's project directory:
- [templates/openai_client.py](templates/openai_client.py)
- [templates/gemini_client.py](templates/gemini_client.py)
- [templates/anthropic_client.py](templates/anthropic_client.py)
- [templates/groq_client.py](templates/groq_client.py)
- [templates/openrouter_client.py](templates/openrouter_client.py)
- [templates/ollama_client.py](templates/ollama_client.py)

## Rules

- Never hardcode API keys — always use `os.environ`
- If a vendor does not support a modality, the function raises `NotImplementedError` with a clear message
- Always install the required package before running the smoke test
- If the user asks for multiple vendors, generate all requested client files
