from typing import Set, TypedDict

class VllmConfig(TypedDict):
    model: str
    enable_prefix_caching: bool
    mm_processor_cache_gb: int
    gpu_memory_utilization: float
    max_num_seqs: int

VLLM_CONFIG: VllmConfig = {
    "model": "deepseek-ai/DeepSeek-OCR",
    "enable_prefix_caching": False,
    "mm_processor_cache_gb": 0,
    "gpu_memory_utilization": 0.8,
    "max_num_seqs": 1,
}

class ExtraArgs(TypedDict):
    ngram_size: int
    window_size: int
    whitelist_token_ids: Set[int]

class SamplingConfig(TypedDict):
    temperature: float
    max_tokens: int
    extra_args: ExtraArgs
    skip_special_tokens: bool

SAMPLING_CONFIG: SamplingConfig = {
    "temperature": 0.0,
    "max_tokens": 8192,
    "extra_args": {
        "ngram_size": 30,
        "window_size": 90,
        "whitelist_token_ids": {128821, 128822},
    },
    "skip_special_tokens": False,
}

PROMPT = "<image>\n"
MODEL_SESSION_KEY = "llm"