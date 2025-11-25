import streamlit as st
from src.persistence import Repository
from src.domain import Pipeline

def render(repo: Repository):
    """Renders the Pipeline management UI tab."""
    st.subheader("Create New Pipeline")

    with st.form("pipeline_form", clear_on_submit=True):
        name = st.text_input("Pipeline Name")
        channel = st.selectbox("Channel", ["linkedin", "medium", "system"])
        language_avatar = st.text_area("Language Avatar (Agent Persona)", height=200)
        user_persona = st.text_area("User Persona", height=200)
        post_config = st.text_area("Post Config (Stylistic Guidelines)", height=200)

        submitted = st.form_submit_button("Create Pipeline")
        if submitted:
            if not name:
                st.error("Pipeline Name is a required field.")
            else:
                try:
                    new_pipeline = Pipeline(
                        id=None,
                        name=name,
                        channel=channel,
                        language_avatar=language_avatar,
                        user_persona=user_persona,
                        post_config=post_config
                    )
                    repo.add_pipeline(new_pipeline)
                    st.success(f"Pipeline '{name}' created successfully!")
                except Exception as e:
                    st.error(f"Failed to create pipeline: {e}")

    st.divider()

    st.subheader("Existing Pipelines")
    try:
        pipelines = repo.get_all_pipelines()
        if pipelines:
            display_data = [{
                "Name": p.name, 
                "Channel": p.channel, 
                "Post Type": "Configured"
            } for p in pipelines]
            st.dataframe(display_data)
        else:
            st.info("No pipelines found. Create one above to get started.")
    except Exception as e:
        st.error(f"Failed to load pipelines: {e}")
