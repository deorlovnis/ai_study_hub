from typing import Protocol

class OcrModel(Protocol):
    """Defines the interface for any model that can perform OCR."""
    def extract_text(self, image_bytes: bytes) -> str:
        ...
