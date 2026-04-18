# multi-vendor-llm skill

**Version:** 1.1.0  
**Author:** jyotiprakash

Generates ready-to-run Python client files for LLM vendor APIs. Supports text, image generation, and voice (TTS/STT) — only generates what you actually need.

## Supported vendors

| Vendor      | Text | Image | TTS | STT |
|-------------|------|-------|-----|-----|
| OpenAI      | ✓    | ✓     | ✓   | ✓   |
| Gemini      | ✓    | ✓     | ✓   | -   |
| Anthropic   | ✓    | -     | -   | -   |
| Groq        | ✓    | -     | -   | -   |
| OpenRouter  | ✓    | -     | -   | -   |
| Ollama      | ✓    | -     | -   | -   |

## Usage

Invoke the skill and it will ask you:
1. Which vendor(s) you want
2. Which features you need (chat / image / TTS / STT)

It then generates:
- `<vendor>_client.py` — client with only your selected features
- `.env.example` — shows which API key(s) to add to your `.env`
- `requirements.txt` — all dependencies to install

## Setup after generation

```bash
# 1. Copy .env.example and fill in your API key(s)
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify your key is loaded
python openai_client.py
```

## Structure

```
multi-vendor-llm/
├── skill.md              # Skill workflow and rules
├── README.md             # This file
├── templates/            # One template per vendor
│   ├── openai_client.py
│   ├── gemini_client.py
│   ├── anthropic_client.py
│   ├── groq_client.py
│   ├── openrouter_client.py
│   └── ollama_client.py
└── references/           # API reference docs per vendor
    ├── openai.md
    ├── gemini.md
    ├── anthropic.md
    ├── groq.md
    ├── openrouter.md
    └── ollama.md
```
