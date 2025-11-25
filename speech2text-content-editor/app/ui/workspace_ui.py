import streamlit as st
from src.persistence import Repository
from src.services import PipelineService

def render(repo: Repository, pipeline_service: PipelineService):
    """Renders the Workspace UI tab."""
    st.subheader("Content Generation Workspace")

    try:
        drafts = repo.get_all_drafts()
        pipelines = repo.get_all_pipelines()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    if not drafts:
        st.warning("No drafts found. Please create a draft in the 'Transcription' tab first.")
        return

    if not pipelines:
        st.warning("No pipelines found. Please create a pipeline in the 'Pipelines' tab first.")
        return

    # Create selection boxes
    draft_options = {d.id: f"Draft {d.id} - '{d.raw_text[:50]}...'" for d in drafts}
    selected_draft_id = st.selectbox("Choose a Draft to Work On", options=list(draft_options.keys()), format_func=lambda x: draft_options[x])

    pipeline_options = {p.id: p.name for p in pipelines}
    selected_pipeline_id = st.selectbox("Choose a Pipeline to Use", options=list(pipeline_options.keys()), format_func=lambda x: pipeline_options[x])

    if st.button("Generate Post"):
        if selected_draft_id and selected_pipeline_id:
            selected_draft = next((d for d in drafts if d.id == selected_draft_id), None)
            selected_pipeline = next((p for p in pipelines if p.id == selected_pipeline_id), None)
            
            if selected_draft and selected_pipeline:
                with st.spinner("Assembling prompt..."):
                    try:
                        assembled_prompt = pipeline_service.execute_pipeline(selected_draft, selected_pipeline)
                        st.session_state.assembled_prompt = assembled_prompt
                    except Exception as e:
                        st.error(f"Failed to execute pipeline: {e}")
            else:
                st.error("Could not find the selected draft or pipeline.")
    
    if 'assembled_prompt' in st.session_state:
        st.subheader("Assembled Prompt for Verification")
        st.code(st.session_state.assembled_prompt, language='text')
        # In a future step, this would be the start of the chat interface.
