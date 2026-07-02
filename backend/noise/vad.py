from silero_vad import read_audio, get_speech_timestamps, load_silero_vad
model = load_silero_vad()
def detect_speech(audio_file):
    
    audio = read_audio(audio_file)
    speech_timestamps = get_speech_timestamps(audio,model)
    if len(speech_timestamps) > 0:
        return {"speech_detected": True, "speech_segment": speech_timestamps}
    else:
        return {"speech_detected": False, "speech_segment": []}