## Convert PDF files to images


"""Convert PDF documents into image files."""

from pathlib import Path
from uuid import uuid4

from pdf2image import convert_from_path

from utils.config import UPLOAD_DIR
from utils.tracing_utils import traced_function


@traced_function("pdf_to_images")
def pdf_to_images(pdf_path: str) -> list[str]:
    """
    Convert every page of a PDF into a PNG image.

    Args:
        pdf_path: Path to the uploaded PDF.

    Returns:
        List of generated image paths, ordered by page.
    """
    source = Path(pdf_path)

    if not source.exists():
        raise FileNotFoundError(f"PDF not found: {source}")

    # Render pages at 180 DPI, a practical starting point
    # for readable notes without unnecessarily huge images.
    pages = convert_from_path(
        str(source),
        dpi=180,
    )

    image_paths = []

    # Use unique names to avoid overwriting another document.
    for page_number, page_image in enumerate(pages, start=1):
        output_path = UPLOAD_DIR / (
            f"{uuid4().hex}_page_{page_number}.png"
        )

        # Save the rendered page in PNG format.
        page_image.save(output_path, format="PNG")
        image_paths.append(str(output_path))

    return image_paths
