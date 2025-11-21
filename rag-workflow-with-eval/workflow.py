from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
from llama_index.core.workflow import Event, Context, Workflow, StartEvent, StopEvent, step
from llama_index.core.schema import NodeWithScore
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import CompactAndRefine

from config import RAGConfig

class RetrieverEvent(Event):
    """Result of running retrieval"""
    nodes: list[NodeWithScore]

class RAGWorkflow(Workflow):
    def __init__(
        self,
        model_name: str = RAGConfig.MODEL_NAME,
        embedding_model: str = RAGConfig.EMBEDDING_MODEL,
        context_window: int = RAGConfig.CONTEXT_WINDOW,
    ):
        super().__init__()
        self.llm = Ollama(
            model=model_name,
            context_window=context_window,
            additional_kwargs={
                "num_ctx": context_window,
                "num_batch": RAGConfig.NUM_BATCH,
            },
        )
        self.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
        
        # Configure global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
        self.index: VectorStoreIndex | None = None

    @step
    async def ingest(self, ctx: Context, ev: StartEvent) -> StopEvent | None:
        """Entry point to ingest documents from a directory."""
        dirname = ev.get("dirname")
        if not dirname:
            return None

        documents = SimpleDirectoryReader(dirname).load_data()
        self.index = VectorStoreIndex.from_documents(documents=documents)
        return StopEvent(result=self.index)

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrieverEvent | None:
        """Entry point for RAG retrieval."""
        query = ev.get("query")
        index = ev.get("index") or self.index

        if not query:
            return None

        if index is None:
            print("Index is empty, load some documents before querying!")
            return None

        retriever = index.as_retriever(similarity_top_k=2)
        nodes = await retriever.aretrieve(query)
        await ctx.store.set("query", query)
        return RetrieverEvent(nodes=nodes)

    @step
    async def synthesize(self, ctx: Context, ev: RetrieverEvent) -> StopEvent:
        """Generate a response using retrieved nodes."""
        summarizer = CompactAndRefine(streaming=False, verbose=True)
        query = await ctx.store.get("query", default=None)
        response = await summarizer.asynthesize(query, nodes=ev.nodes)
        response_text = response.response if hasattr(response, "response") else str(response)
        return StopEvent(result=response_text)

    async def query(self, query_text: str):
        """Helper method to perform a complete RAG query."""
        if self.index is None:
            raise ValueError("No documents have been ingested. Call ingest_documents first.")
        
        result = await self.run(query=query_text, index=self.index)
        return result

    async def ingest_documents(self, directory: str):
        """Helper method to ingest documents."""
        result = await self.run(dirname=directory)
        self.index = result
        return result 