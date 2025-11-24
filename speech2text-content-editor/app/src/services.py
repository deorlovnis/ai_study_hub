import torch
from nemo.collections.asr.models import EncDecRNNTModel
import soundfile as sf
import numpy as np
import os

from .config import Settings

class TranscriptionService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self._load_model(self.settings.ASR_MODEL)

    def _is_stereo(self, data: np.ndarray) -> bool:
        """Checks if the audio data is stereo."""
        is_multidimensional = data.ndim >= self.settings.MIN_AUDIO_DIMENSIONS
        has_multiple_channels = data.shape[
            self.settings.NUMPY_CHANNEL_DIM_INDEX] > self.settings.MONO_CHANNEL_COUNT
        return is_multidimensional and has_multiple_channels

    def _convert_to_mono(self, data: np.ndarray) -> np.ndarray:
        """Converts stereo audio data to mono by averaging channels."""
        return np.mean(data, axis=self.settings.NUMPY_CHANNEL_AXIS)

    def _load_model(self, model_name: str) -> EncDecRNNTModel:
        """Loads the ASR model."""
        model = EncDecRNNTModel.from_pretrained(model_name, map_location=self.device)
        model.eval()
        return model

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes an audio file, converting to mono if necessary.

        Args:
            audio_path: Path to the audio file.

        Returns:
            The transcribed text.
        """
        if not audio_path:
            return ""

        data, samplerate = sf.read(audio_path)
        
        processed_audio_path = audio_path
        is_temp_file = False
        if self._is_stereo(data):
            mono_data = self._convert_to_mono(data)
            processed_audio_path = self.settings.MONO_TEMP_AUDIO_PATH
            sf.write(processed_audio_path, mono_data, samplerate)
            is_temp_file = True
        
        hypotheses = []
        try:
            hypotheses = self.model.transcribe(audio=[processed_audio_path])
        finally:
            if is_temp_file:
                os.remove(processed_audio_path)

        if hypotheses and hypotheses[self.settings.BEST_HYPOTHESIS_INDEX]:
            return hypotheses[self.settings.BEST_HYPOTHESIS_INDEX].text
        return ""
