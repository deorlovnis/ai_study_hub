from .abstractions import OcrModel


class OcrService:
    """Encapsulates the business logic for OCR."""

    def __init__(self, model: OcrModel):
        self.model = model

    def extract_latex_from_image(self, image_bytes: bytes) -> str:
        return self.model.extract_text(image_bytes)
