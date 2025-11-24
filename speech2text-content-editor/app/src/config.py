class Settings:
    """
    Holds all the configuration for the application.
    """
    # ASR Model
    ASR_MODEL = "nvidia/parakeet-tdt-0.6b-v2"
    
    # File Paths
    TEMP_AUDIO_PATH = "temp_audio.wav"
    MONO_TEMP_AUDIO_PATH = "temp_audio_mono.wav"

    # Audio Properties
    MIN_AUDIO_DIMENSIONS = 2
    MONO_CHANNEL_COUNT = 1
    NUMPY_CHANNEL_AXIS = 1
    NUMPY_CHANNEL_DIM_INDEX = 1
    
    # Transcription Properties
    BEST_HYPOTHESIS_INDEX = 0
