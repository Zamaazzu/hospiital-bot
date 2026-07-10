from noise.vad import detect_speech
from noise.denoise import denoise_audio
from stt.transcribe import transcribe_audio


def process_audio(audio_path):

    # Step 1 : Detect Speech
    vad_result = detect_speech(audio_path)

    if not vad_result.get("success", False):
        return vad_result

    if not vad_result.get("speech_detected", False):
        return {
            "success": False,
            "error": "No speech detected."
        }

    # Step 2 : Remove Noise
    denoise_result = denoise_audio(
        vad_result["speech_audio_path"]
    )

    if not denoise_result.get("success", False):
        return denoise_result

    # Step 3 : Speech To Text
    transcription_result = transcribe_audio(
        denoise_result["clean_audio_path"]
    )

    if not transcription_result.get("success", False):
        return transcription_result

    # Final Output
    return {
        "success": True,
        "transcript": transcription_result["transcript"],
        "confidence": transcription_result["confidence"]
    }