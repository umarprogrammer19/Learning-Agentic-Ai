from agents import Agent, Runner, function_tool, ModelSettings
from typing import Optional
import os


@function_tool
def translate_text(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> str:
    """Translate `text` into `target_lang` (ISO code like 'ur', 'en') using Google Translate v2.


    Args:
    text: The English text to translate.
    target_lang: ISO 639-1 language code (e.g., 'ur', 'en', 'ar', 'fr').
    source_lang: Optional ISO code for source language; omit to auto-detect.
    Returns:
    The translated text as a string.
    """
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY not set.")
