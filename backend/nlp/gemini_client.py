from google import genai
from backend.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt):
    """
    Send a prompt to Gemini and return only the generated text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text or "I'm sorry, I couldn't generate a response."

    except Exception as e:
        print(f"Gemini API error: {e}")
        return None