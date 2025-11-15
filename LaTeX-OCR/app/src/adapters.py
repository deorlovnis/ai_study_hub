import io

from PIL import Image
from vllm import LLM, SamplingParams

from .abstractions import OcrModel
from .config import PROMPT, SAMPLING_CONFIG


class VllmOcrLatexAdapter(OcrModel):
    """Adapter that uses a VLLM model to satisfy the OcrModel interface."""

    def __init__(self, llm: LLM):
        self.llm = llm
        self.sampling_params = SamplingParams(**SAMPLING_CONFIG)

    def extract_text(self, image_bytes: bytes) -> str:
        """Run the OCR pipeline and return the extracted text."""

        if not image_bytes:
            raise ValueError("Image bytes are empty or invalid.")
        
        image_buffer = io.BytesIO(image_bytes)
        image_buffer.seek(0)
        
        try:
            image: Image.Image = Image.open(image_buffer)
            if image.mode != "RGB":
                image = image.convert("RGB")
        except Exception as e:
            raise ValueError(f"Failed to open image: {e}") from e

        model_input = [
            {
                "prompt": PROMPT,
                "multi_modal_data": {"image": image},
            }
        ]

        model_outputs = self.llm.generate(model_input, self.sampling_params)
        if not model_outputs or not model_outputs[0].outputs:
            raise ValueError("The model did not return any output.")

        result = model_outputs[0].outputs[0].text.strip()

        if not result:
            raise ValueError("The model returned an empty result.")

        return result
