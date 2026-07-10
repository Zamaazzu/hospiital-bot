'''from silero_vad import read_audio, get_speech_timestamps, load_silero_vad
model = load_silero_vad()
def detect_speech(audio_file):
    
    audio = read_audio(audio_file)
    speech_timestamps = get_speech_timestamps(audio,model)
    if len(speech_timestamps) > 0:
        return {"speech_detected": True, "speech_segment": speech_timestamps}
    else:
        return {"speech_detected": False, "speech_segment": []}'''
import os

import numpy as np
import soundfile as sf
import torch
import torchaudio

from silero_vad import load_silero_vad, get_speech_timestamps

# Load Silero VAD model only once
model = load_silero_vad()


def detect_speech(audio_path):

    try:
        # Check if file exists
        if not os.path.exists(audio_path):
            return {
                "success": False,
                "speech_detected": False,
                "speech_audio_path": None,
                "error": "Audio file not found."
            }

        # Load audio
        audio, sample_rate = sf.read(audio_path)

        # Convert stereo to mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # Convert to torch tensor
        audio = torch.from_numpy(audio).float()

        # Resample to 16 kHz if needed
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate,
                new_freq=16000
            )
            audio = resampler(audio)
            sample_rate = 16000

        # Normalize audio
        max_value = torch.max(torch.abs(audio))

        if max_value > 0:
            audio = audio / max_value

        # Detect speech
        speech_timestamps = get_speech_timestamps(audio, model)

        if len(speech_timestamps) == 0:
            return {
                "success": True,
                "speech_detected": False,
                "speech_audio_path": None
            }

        # Extract speech segment
        start = speech_timestamps[0]["start"]
        end = speech_timestamps[-1]["end"]

        speech_audio = audio[start:end]

        output_path = "audio/temp/speech.wav"

        sf.write(
            output_path,
            speech_audio.numpy(),
            sample_rate
        )

        return {
            "success": True,
            "speech_detected": True,
            "speech_audio_path": output_path
        }

    except Exception as e:
        return {
            "success": False,
            "speech_detected": False,
            "speech_audio_path": None,
            "error": str(e)
        }