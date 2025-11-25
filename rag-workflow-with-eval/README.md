# RAG workflow with evaluation

RAG system built with LlamaIndex and llama3.2. Integrates an evaluation pipeline using Langfuse for observability and evaluation of the RAG performance.

- LlamaIndex
- llama3.2
- Langfuse

## Quick start

1. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Create a new Python environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

3. Download and run Ollama:
   ```bash
   ollama pull llama3.2
   ollama serve
   ```

4. Register on the [Langfuse platform](https://langfuse.com/) to get the needed keys. 
   Create `.env` from the example file.

   ```bash
   cp .env.example .env
   ```

5. Run the notebooks to test things out. You can run RAG separately
   or along with the evaluation. Note that the scripts will only transfer 
   necessary data to Langfuse platform. To run actual evaluation you'll need
   to set up LLM-as-a-judge.
   See the [documentation](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge).

## The workflow limitations

Langfuse has a limited amount of predefined evaluators. It's good if you need to quickly start monitoring LLM-enabled systems, but if you want to experiment with custom evaluation methods, it's probably better to look for other options.  

## Do you have feedback?

Feel free to contact me with any questions