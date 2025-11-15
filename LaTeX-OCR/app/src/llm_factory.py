from vllm import LLM
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
from .config import VLLM_CONFIG

def create_llm() -> LLM:
    """Instantiates and returns the VLLM model."""
    return LLM(
        **VLLM_CONFIG,
        logits_processors=[NGramPerReqLogitsProcessor],
    )
