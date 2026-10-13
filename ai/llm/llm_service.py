from google import genai
from ai.rag.config import GEMINI_API_KEY


MODEL_NAME = "gemini-3.5-flash-lite"


def get_llm_client():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Please add it to the .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(prompt):
    client = get_llm_client()

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text