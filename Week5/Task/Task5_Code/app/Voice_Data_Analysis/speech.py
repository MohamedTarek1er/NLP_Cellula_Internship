import os
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel

model = None

def get_whisper_model():
    global model

    if model is None:
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return model


def transcribe_audio(audio_path):
    whisper_model = get_whisper_model()

    segments, info = whisper_model.transcribe(
        audio_path,
        beam_size=5
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    return {
        "transcript": transcript,
        "language": info.language,
        "language_probability": round(
            info.language_probability, 3
        )
    }
