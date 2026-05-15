# utils/translator.py

import requests
from langdetect import detect, LangDetectException

# ── Config: pick your translator ──────────────────────
TRANSLATOR         = "gemini"        # "gemini" or "lmstudio"
GEMINI_API_KEY     = "xxx"
LMSTUDIO_BASE_URL  = "http://localhost:1234/v1"   # default LM Studio port
LMSTUDIO_MODEL     = "local-model"                # whatever model you have loaded
# ──────────────────────────────────────────────────────


def detect_language(text: str) -> str:
    """Returns ISO language code: 'en', 'ur', 'ko', etc."""
    try:
        return detect(text)
    except LangDetectException:
        return "en"   # default to English if detection fails


def translate_to_english_gemini(text: str) -> str:
    """Calls Gemini API to translate text to English."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )
    prompt = (
        f"Translate the following text to English. "
        f"Return ONLY the translated text, nothing else.\n\n{text}"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[Gemini translation error] {e}")
        return text   # fallback: return original if translation fails


def translate_to_english_lmstudio(text: str) -> str:
    """Calls local LM Studio (OpenAI-compatible API) to translate text."""
    url = f"{LMSTUDIO_BASE_URL}/chat/completions"
    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a translator. Translate any input to English. Reply with ONLY the translated text."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LM Studio translation error] {e}")
        return text   # fallback: return original if translation fails


def translate_if_needed(text: str) -> tuple[str, str, str]:
    lang = detect_language(text)
    
    if lang == "en":
        return text, "en", "none"

    # Try Gemini first
    try:
        translated = translate_to_english_gemini(text)
        # If Gemini returned something useful
        if translated and translated != text:
            return translated, lang, "gemini"
    except Exception as e:
        print(f"[Gemini failed, trying LM Studio] {e}")

    # Fallback to LM Studio if Gemini fails
    try:
        translated = translate_to_english_lmstudio(text)
        if translated and translated != text:
            return translated, lang, "lmstudio"
    except Exception as e:
        print(f"[LM Studio also failed] {e}")

    # If both fail, return original text and flag it
    print(f"[Translation failed] Returning original text")
    return text, lang, "failed"
