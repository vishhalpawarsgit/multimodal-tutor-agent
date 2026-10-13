## analyze images with OpenAI's vision model


"""Analyze notes, diagrams, charts, and screenshots using OpenAI."""

import base64
import mimetypes
from pathlib import Path

from utils.config import OPENAI_VISION_MODEL
from utils.tracing_utils import get_openai_client, traced_function


TUTOR_INSTRUCTIONS = """
You are a precise, patient multimodal tutor.

Analyze the uploaded educational material and produce these sections:

1. DETAILED EXPLANATION
Explain the content in simple language. Define technical terms
and describe diagrams, relationships, formulas, and code where visible.

2. SUMMARY NOTES
Provide concise notes that a student can revise later.

3. IMPORTANT CONCEPTS
List the important concepts and explain why each matters.

4. ASSIGNMENT QUESTIONS
Create five questions based on the material, mixing conceptual
and application-oriented questions. Include answers separately.

5. TEXT-BASED MIND MAP
Represent the main topic and its subtopics as a readable
hierarchical outline.

6. UNCERTAINTIES
Mention anything illegible, cropped, ambiguous, or inferred.
Never invent text that cannot be read from the image.

Use clear headings and explain acronyms when they first appear.
If the input is a code screenshot, explain the code's purpose,
control flow, important statements, and likely failure cases.
"""


def image_to_data_url(image_path: str) -> str:
    """
    Convert a local image to a base64 data URL.

    The data URL lets the API receive the image content directly,
    without requiring a publicly accessible image URL.
    """
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    # Detect the MIME type from the image extension.
    mime_type, _ = mimetypes.guess_type(path.name)

    # Only allow the image formats used by this application.
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }

    if mime_type not in allowed_types:
        raise ValueError(f"Unsupported image format: {mime_type}")

    # Encode the file bytes as base64.
    image_bytes = path.read_bytes()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_image}"


@traced_function("analyze_image")
def analyze_image(image_path: str) -> str:
    """
    Send an image to OpenAI and return a tutoring explanation.
    """
    client = get_openai_client()

    # Convert the image to the format accepted by the API.
    image_url = image_to_data_url(image_path)

    # Request an explanation grounded in the supplied image.
    response = client.responses.create(
        model=OPENAI_VISION_MODEL,
        instructions=TUTOR_INSTRUCTIONS,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyze this educational material "
                            "and follow the tutoring instructions."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url,
                        "detail": "high",
                    },
                ],
            }
        ],
        max_output_tokens=3000,
    )

    # The SDK exposes the generated text through output_text.
    return response.output_text.strip()
