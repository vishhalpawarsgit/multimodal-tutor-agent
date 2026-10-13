## Extract text through local OCR engine


"""Optional local OCR utility using Tesseract."""

from pathlib import Path

import pytesseract
from PIL import Image

from utils.tracing_utils import traced_function


@traced_function("extract_text")
def extract_text(image_path: str) -> str:
    """
    Extract text from an image using the local Tesseract engine.

    This operation does not call OpenAI.
    """
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    # Open the image and convert it to a standard RGB image.
    with Image.open(path) as image:
        normalized_image = image.convert("RGB")

        # Run OCR using the Tesseract executable installed locally.
        extracted_text = pytesseract.image_to_string(
            normalized_image
        )

    return extracted_text.strip()
