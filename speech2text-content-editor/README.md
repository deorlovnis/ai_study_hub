# Speech-to-Text Content Editor with Parakeet

## AI-powered workflow to transform raw voice memos into polished social media content.

This project showcases a text transformation pipeline and a basic prompt management system that helps to create customizable prompts. 

With it you can:

- Transcribe audio recordings into raw text drafts using NVIDIA's Parakeet model.
- Define and configure multi-part AI pipelines with specific agentic personas, audience targets, and stylistic guidelines.
- Orchestrate these pipelines in a workspace to transform your raw drafts into formatted content for different channels like LinkedIn.

## Quick start on Ubuntu

As a prerequisite, you need to have uv.

1. **Install uv:** 
    ```bash
    # On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv pip install -e .
    ```
3.  **Set up the database:**
    This command will create the local SQLite database needed to store drafts and pipelines.
    ```bash
    make setup_db
    ```
4.  **Run the application:**
    ```bash
    uv run streamlit run app/app.py
    ```

## Project limitations

- This project showcases my marketing content creation pipeline and is not meant for daily usage.

- Drafts can be created only from voice input.

- It has no API integrations with LLM providers and assembles one prompt at a time, which you would need to copy and paste into chat interfaces likegGoogle studio to polish and get the final results.


## Do you have feedback?

Feel free to contact me with any questions.

