
"""Command-line smoke test for the Multimodal Tutor Agent.

Usage:
    uv run python main.py path/to/test_image.png
"""

import argparse
from pathlib import Path

from utils.openai_utils import analyze_image


def main() -> None:
    """Analyze one image and print the result."""
    parser = argparse.ArgumentParser(
        description="Analyze a study image using OpenAI."
    )

    parser.add_argument(
        "image_path",
        type=Path,
        help="Path to a local PNG, JPG, or WEBP image.",
    )

    args = parser.parse_args()

    if not args.image_path.is_file():
        parser.error(f"File does not exist: {args.image_path}")

    # Call the same function used by the Streamlit application.
    result = analyze_image(str(args.image_path.resolve()))

    print("\n=== Tutor Analysis ===\n")
    print(result)


if __name__ == "__main__":
    main()
