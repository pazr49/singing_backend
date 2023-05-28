import numpy as np
import soundfile as sf

def normalize_audio(audio):
    # Calculate the maximum amplitude of the audio
    max_amplitude = np.max(np.abs(audio))

    # Normalize the audio by dividing each sample by the maximum amplitude
    normalized_audio = audio / max_amplitude

    return normalized_audio

