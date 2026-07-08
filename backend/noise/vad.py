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
import torch
import torchaudio

from silero_vad import (
    load_silero_vad,
    get_speech_timestamps
)

# Load the model once
model = load_silero_vad()

TARGET_SAMPLE_RATE = 16000


def detect_speech(audio_file):

    # Check if the audio file exists
    if not os.path.exists(audio_file):
        return {
            "success": False,
            "speech_detected": False,
            "speech_audio_path": None,
            "error": "Audio file not found."
        }

    try:

        # Load the audio file
        waveform, sample_rate = torchaudio.load(audio_file)

        # Convert stereo audio to mono
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Convert sample rate to 16 kHz
        if sample_rate != TARGET_SAMPLE_RATE:

            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate,
                new_freq=TARGET_SAMPLE_RATE
            )

            waveform = resampler(waveform)

        # Remove the channel dimension
        waveform = waveform.squeeze()

        # Detect speech
        speech_timestamps = get_speech_timestamps(
            waveform,
            model,
            sampling_rate=TARGET_SAMPLE_RATE,
            threshold=0.5,
            min_silence_duration_ms=300,
            speech_pad_ms=200
        )

        # No speech found
        if not speech_timestamps:
            return {
                "success": True,
                "speech_detected": False,
                "speech_audio_path": None
            }

        # Extract speech segments
        speech_chunks = []

        for segment in speech_timestamps:

            start = segment["start"]
            end = segment["end"]

            speech_chunks.append(
                waveform[start:end]
            )

        # Merge all speech segments
        speech_waveform = torch.cat(speech_chunks)

        # Add channel dimension for saving
        speech_waveform = speech_waveform.unsqueeze(0)

        # Save speech audio
        output_path = "audio/temp/speech.wav"

        torchaudio.save(
            output_path,
            speech_waveform,
            TARGET_SAMPLE_RATE
        )

        return {
            "success": True,
            "speech_detected": True,
            "speech_audio_path": output_path,
            "speech_segments": speech_timestamps
        }

    except Exception as e:

        return {
            "success": False,
            "speech_detected": False,
            "speech_audio_path": None,
            "error": str(e)
        }