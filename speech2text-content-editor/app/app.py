import streamlit as st

from src.persistence import Repository
from src.services import PipelineService
from src.config import Settings
from ui import transcription_ui, pipeline_ui, workspace_ui

def main():
    """Main function to initialize and run the application."""
    st.set_page_config(page_title="AI Content Workflow", layout="wide")
    st.title("AI Content Workflow Engine")

    try:
        settings = Settings()
        repo = Repository()
        pipeline_service = PipelineService()
    except Exception as e:
        st.error(f"Failed to initialize the application: {e}")
        return

    transcription_tab, pipelines_tab, workspace_tab = st.tabs(
        ["Transcription", "Pipelines", "Workspace"]
    )

    with transcription_tab:
        transcription_ui.render(repo, settings)

    with pipelines_tab:
        pipeline_ui.render(repo)

    with workspace_tab:
        workspace_ui.render(repo, pipeline_service)


if __name__ == "__main__":
    main()
