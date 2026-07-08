import noisereduce as nr
import soundfile as sf
import os
def denoise_audio(input_path):
    audio, sr =sf.read(input_path)
    clean_audio = nr.reduce_noise(y=audio,sr=sr)
    output_path="audio/temp/clean.wav"
    sf.write(output_path, clean_audio, sr)
    return {
            "success": True,
            "clean_audio_path": output_path
        }