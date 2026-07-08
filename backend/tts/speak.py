import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("sarvam_api_key")
url="https://api.sarvam.ai/v1/tts"
default_language = "ml-IN"
def speak(text:str):
    if not api_key:
        return { "success": False, "message": "API key not found." }
    if not text or not text.strip():
        return { "success": False, "message": "Text is empty" }
    try:
        headers = {"sarvam-api-key": api_key}
        data ={"text": text, "language": default_language}
        response = requests.post(url=url,headers=headers,json=data,timeout=60 )
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"API request failed with status code {response.status_code}: {response.text}"
            }
        output_path="audio/output/response.mp3"
        with open(output_path,"wb")as f:
            f.write(response.content)
        return { "success": True, "audio_path": output_path }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Sarvam API request timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

    except PermissionError:
        return {
            "success": False,
            "error": "Cannot save audio file."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }