import os
from urllib import response
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
api_key = os.getenv("SARVAM_API_KEY")
url="https://api.sarvam.ai/text-to-speech"
default_language = "ml-IN"
def speak(text:str):
    if not api_key:
        return { "success": False, "message": "API key not found." }
    if not text or not text.strip():
        return { "success": False, "message": "Text is empty" }
    try:
        headers = { "api-subscription-key": api_key,
             "Content-Type": "application/json"}
        data ={"text": text,
               "speaker": "kavya",
                "target_language_code": default_language,
                "model": "bulbul:v3"}
        response = requests.post(url=url,headers=headers,json=data,timeout=60 )
        
        if response.status_code != 200:
            return {
                "success": False,
                "message": f"API request failed with status code {response.status_code}: {response.text}"
            }
        result = response.json()

        audio_base64 = result["audios"][0]

        audio_bytes = base64.b64decode(audio_base64)    
        output_path="audio/temp/response.wav"
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        return {
            "success": True,
            "audio_path": output_path,
            "audio_base64": audio_base64
        }
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