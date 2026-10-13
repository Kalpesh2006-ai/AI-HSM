from google import genai
from ai.rag.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Say hello in one sentence."
)

print(response.output_text)