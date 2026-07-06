from google import genai
from backend.config import GEMINI_API_KEY

client=genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt):
    """
    send a prompt to gemini and return only generated text
    """
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
