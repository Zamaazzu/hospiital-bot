from google import genai
from backend.config import GEMINI_API_KEY
import requests

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_ollama(prompt, model="qwen3:14b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "think": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip() or None
        return None
    except Exception as e:
        print(f"Ollama fallback error: {e}")
        return None

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
        print("Falling back to Ollama...")
        return ask_ollama(prompt)