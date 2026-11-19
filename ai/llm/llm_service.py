
from google import genai
from ai.rag.config import GEMINI_API_KEY


MODEL_NAME = "gemini-3.5-flash-lite"

LANGUAGE_INSTRUCTIONS = {
    "en-IN": "English",
    "hi-IN": "Hindi",
    "mr-IN": "Marathi"
}


def get_llm_client():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Please add it to the .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(prompt, language="en-IN"):
    client = get_llm_client()

    selected_language = LANGUAGE_INSTRUCTIONS.get(
        language, "English"
    )

    language_instruction = f"""
IMPORTANT LANGUAGE REQUIREMENT:

You MUST write your entire answer in {selected_language}.

The user's selected response language is {selected_language}.
Do not answer in Hindi unless Hindi is selected.
Do not answer in Marathi unless Marathi is selected.
Do not switch languages based on the language of retrieved documents.

Keep government scheme names, official abbreviations,
and technical terms in their commonly recognized form.

Use natural, simple {selected_language} suitable for beginners.

This language requirement is mandatory.
"""

    accuracy_instruction = """
IMPORTANT RESPONSE RULES:

1. Treat retrieved government documents as the primary
   source of information.

2. Never invent, modify, or add extra zeros to numerical
   values, loan amounts, dates, percentages, or limits.

3. Preserve the exact numerical meaning in the documents.

4. For Indian currency, use the Indian numbering system.
   Examples:
   - 50000 = ₹50,000
   - 500000 = ₹5,00,000
   - 1000000 = ₹10,00,000
   - 2000000 = ₹20,00,000

5. For PMMY loan categories, use these amounts only
   when supported by retrieved documents:
   - Shishu: Up to ₹50,000
   - Kishore: Above ₹50,000 and up to ₹5 lakh
   - Tarun: Above ₹5 lakh and up to ₹10 lakh
   - Tarun Plus: Above ₹10 lakh and up to ₹20 lakh

6. Check every numerical value before answering.

7. If the documents do not establish a numerical value,
   do not guess.
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=(
            language_instruction
            + "\n\n"
            + accuracy_instruction
            + "\n\n"
            + prompt
        )
    )

    return interaction.output_text
