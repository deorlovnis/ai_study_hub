import torch
from nemo.collections.asr.models import EncDecRNNTModel
import soundfile as sf
import numpy as np
import os

from .config import Settings
from .domain import Draft, Pipeline

class TranscriptionService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self._load_model(self.settings.ASR_MODEL)

    def _is_stereo(self, data: np.ndarray) -> bool:
        """Checks if the audio data is stereo."""
        # A mono audio file will have a shape like (n_samples,) which has 1 dimension.
        # A stereo audio file will have a shape like (n_samples, 2) which has 2 dimensions.
        if data.ndim < self.settings.MIN_AUDIO_DIMENSIONS:
            return False
            
        channel_index = self.settings.NUMPY_CHANNEL_DIM_INDEX
        has_multiple_channels = data.shape[channel_index] > self.settings.MONO_CHANNEL_COUNT
        
        return has_multiple_channels

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

class PipelineService:
    """
    Handles the business logic for assembling and executing content pipelines.
    """
    def execute_pipeline(self, draft: Draft, pipeline: Pipeline) -> str:
        """
        Assembles the final prompt from a draft and a pipeline.
        
        For now, this returns the assembled prompt string for verification.
        In the future, this method will interact with an LLM.
        """
        # This is a simplified assembly based on the user's provided prompt structure.
        # It can be made more complex and templated later.
        
        system_context = """
        SYSTEM CONTEXT

        You are an expert content transformation system.
        Your task is to transform the provided input text
        according to the specific guidelines below.
        """
        
        # Assemble the final prompt
        final_prompt = (
            f"{system_context}\n"
            f"--- AGENT PERSONA & GUIDELINES ---\n"
            f"{pipeline.language_avatar}\n\n"
            f"--- TARGET AUDIENCE ---\n"
            f"{pipeline.user_persona}\n\n"
            f"--- POST CONFIGURATION & STYLE ---\n"
            f"{pipeline.post_config}\n\n"
            f"--- INPUT TEXT TO TRANSFORM ---\n"
            f"{draft.raw_text}\n\n"
            f"--- FINAL INSTRUCTIONS ---\n"
            f"Follow the agent persona and methodology exactly.\n"
            f"Adhere to all language and voice guidelines.\n"
            f"Apply channel-specific formatting and style requirements.\n"
            f"Preserve the authentic voice and factual accuracy of the original.\n"
            f"Output only the transformed content, no additional commentary."
        )
        
        return final_prompt
