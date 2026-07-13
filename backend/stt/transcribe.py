import os
from dotenv import load_dotenv
import requests
load_dotenv()
api_key = os.getenv("sarvam_api_key")
url = "https://api.sarvam.ai/speech-to-text"

def transcribe_audio(audio_path):
    if not api_key:
        
        return {
    "success": False,
    "error": "Sarvam API key not found."
}
    try:
        
        with open(audio_path,"rb") as audio_file:
            headers = {
                     "api-subscription-key": api_key
                                    }
            data = { "language_code": "ml-IN",  "model": "saaras:v3" }
            
            files = {
                        "file": (
                            "clean.wav",
                            audio_file,
                            "audio/wav"
                        )
                    }
            response = requests.post(url=url, headers=headers, data=data, files=files,timeout=60)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"API request failed with status code {response.status_code}: {response.text}"
                }
            result = response.json()
            transcript = result.get("transcript", "")
            confidence = float(result.get("confidence", 0.0))
            return{"success": True, "transcript": transcript, "confidence": confidence}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Audio file not found."
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Sarvam API timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
         
        