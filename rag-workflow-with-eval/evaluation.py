import json
import pandas as pd
from tqdm.asyncio import tqdm_asyncio
from llama_index.core.base.response.schema import Response
from langfuse import Langfuse, propagate_attributes
import uuid

from workflow import RAGWorkflow

class DatasetLoader:
    def load(self, filepath: str) -> pd.DataFrame:
        data = []
        with open(filepath, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        golden_df = pd.DataFrame(data)
        print(f"Loaded {len(golden_df)} questions for evaluation.")
        return golden_df


class PipelineRunner:
    def __init__(self, workflow: RAGWorkflow, langfuse: Langfuse):
        self.workflow = workflow
        self.langfuse = langfuse

    async def _run_rag_for_question(self, question: str) -> dict:
        with self.langfuse.start_as_current_span(
            name="rag-query",
            input={"question": question},
        ) as trace:
            response = await self.workflow.query(question)

            if isinstance(response, Response):
                response_text = response.response
                contexts = [node.get_content() for node in response.source_nodes]
            else:
                response_text = str(response)
                contexts = []

            trace.update(
                output=response_text,
                metadata={"contexts": contexts},
            )

        return {
            "question": question,
            "answer": response_text,
            "contexts": contexts,
            "trace_id": trace.id,
        }

    async def run(self, golden_df: pd.DataFrame) -> pd.DataFrame:
        results = await tqdm_asyncio.gather(*(self._run_rag_for_question(q) for q in golden_df['question']))
        return pd.DataFrame(results)


class EvaluationPipeline:
    def __init__(self, workflow: RAGWorkflow, langfuse: Langfuse):
        self.workflow = workflow
        self.langfuse = langfuse
        self.dataset_loader = DatasetLoader()
        self.pipeline_runner = PipelineRunner(workflow, langfuse)

    async def run(self, dataset_filepath: str):
        session_id = str(uuid.uuid4())
        print(f"Starting session: {session_id}")

        with propagate_attributes(session_id=session_id):
            golden_df = self.dataset_loader.load(dataset_filepath)
            await self.pipeline_runner.run(golden_df)
            print("Pipeline run complete. Results are available in Langfuse for evaluation.")
        
        print(f"Finished session: {session_id}")
