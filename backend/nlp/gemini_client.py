from google import genai
from config import GEMINI_API_KEY

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
"""
import google.generativeai as genai

from config import GEMINI_API_KEY

# Configure Gemini with your API key
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(prompt: str) -> str:
    
    
    Sends a prompt to Gemini and returns the generated text.
    

    response = model.generate_content(prompt)

    return response.text"""