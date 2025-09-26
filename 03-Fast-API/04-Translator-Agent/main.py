from agents import Agent, Runner, function_tool, ModelSettings
from typing import Optional
import os
import requests
from config import model


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

    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"key": api_key, "q": text, "target": target_lang}
    if source_lang:
        params["source"] = source_lang

    try:
        resp = requests.post(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data["data"]["translations"][0]["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Translate API error: {getattr(e, 'args', [str(e)])[0]}")


# Agent 1: Content generator (English)
content_agent = Agent(
    name="Content Agent",
    instructions=(
        "You are a concise teacher. Generate a clear, simple explanation in English "
        "between 100 and 130 words. Avoid jargon; use plain, friendly language."
    ),
    model=model,
)

# Agent 2: Translator that MUST call the Google Translate tool
translator_agent = Agent(
    name="Translator Agent",
    instructions=(
        "You translate the given 'text' into the 'target_lang' ISO code strictly by calling the 'translate_text' tool. "
        "Always return ONLY the translated text—no preface, no extra commentary."
    ),
    tools=[translate_text],
    model=model,
    # Force tool use so the LLM doesn't try to translate by itself
    model_settings=ModelSettings(tool_choice="required"),
)

# Orchestrator: routes to sub-agents as tools (manager pattern)
orchestrator = Agent(
    name="Orchestrator",
    instructions=(
        "You are a bilingual study assistant. Follow this plan strictly:\n"
        "1) Call generate_explanation to produce an English explanation of the requested topic.\n"
        "2) If the target language is not 'en', call translate_explanation to translate that exact text.\n"
        "3) Return the final text only (no markdown), in the target language. If target is 'en', return the English text."
    ),
    tools=[
        content_agent.as_tool(
            tool_name="generate_explanation",
            tool_description="Create a short English explanation of the user's topic.",
        ),
        translator_agent.as_tool(
            tool_name="translate_explanation",
            tool_description="Translate text to the target_lang by calling the translate_text tool.",
        ),
    ],
    model=model,
)

if __name__ == "__main__":
    topic = "Photosynthesis"
    target_lang = "en"

    user_prompt = (
        f"Topic: {topic}\n"
        f"Target language: {target_lang}\n"
        "First generate explanation, then translate if needed."
    )

    result = Runner.run_sync(orchestrator, input=user_prompt, max_turns=6)
    print("\n--- Final Answer ---\n")
    print(result.final_output)
