import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os

from src.services import TranscriptionService
from src.config import Settings

@st.cache_resource
def load_service(_settings: Settings) -> TranscriptionService:
    """Loads the transcription service."""
    return TranscriptionService(_settings)

def process_audio(audio_bytes, service: TranscriptionService, settings: Settings):
    """
    Saves, transcribes, and cleans up an audio file.
    """
    st.audio(audio_bytes)
    
    audio_path = settings.TEMP_AUDIO_PATH
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    with st.spinner("Transcribing..."):
        transcription = service.transcribe(audio_path)
        st.text_area("Transcription", transcription, height=200)

    os.remove(audio_path)

def main():
    st.title("Speech-to-Text Content Editor")

    settings = Settings()
    service = load_service(settings)

    st.subheader("Record Audio")
    audio = mic_recorder(start_prompt="🔴 Record", stop_prompt="⏹️ Stop", key='recorder')
    if audio:
        process_audio(audio['bytes'], service, settings)

    st.subheader("Upload Audio File")
    uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        process_audio(bytes_data, service, settings)

if __name__ == "__main__":
    main()
