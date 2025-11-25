import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os

from src.persistence import Repository
from src.config import Settings
from src.services import TranscriptionService

@st.cache_resource
def load_transcription_service(_settings: Settings) -> TranscriptionService:
    """Loads the transcription service."""
    return TranscriptionService(_settings)

def render(repo: Repository, settings: Settings):
    """Renders the Transcription UI tab."""
    st.subheader("Record Audio")
    audio = mic_recorder(start_prompt="🔴 Record", stop_prompt="⏹️ Stop", key='recorder')
    
    uploaded_file = st.file_uploader("Or Upload Audio File", type=["wav", "mp3"])

    audio_bytes = None
    if audio:
        audio_bytes = audio['bytes']
    elif uploaded_file is not None:
        audio_bytes = uploaded_file.getvalue()

    if audio_bytes:
        st.audio(audio_bytes)
        
        audio_path = settings.TEMP_AUDIO_PATH
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        service = load_transcription_service(settings)
        with st.spinner("Transcribing..."):
            transcription = service.transcribe(audio_path)
            
            st.session_state.transcription_text = transcription

        os.remove(audio_path)

    if 'transcription_text' in st.session_state and st.session_state.transcription_text:
        st.text_area("Transcription", st.session_state.transcription_text, height=200)
        if st.button("Save as Draft"):
            try:
                repo.add_draft(st.session_state.transcription_text)
                st.success("Draft saved successfully!")
                # Clear the text after saving
                del st.session_state.transcription_text
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save draft: {e}")
