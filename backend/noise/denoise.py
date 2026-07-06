import noisereduce as nr
import soundfile as sf
def denoise_audio(input_path):
    audio, sr =sf.read(input_path)
    clean_audio = nr.reduce_noise(y=audio,sr=sr)
    output_path="denoised"
    sf.write(output_path, clean_audio, sr)
    return output_path