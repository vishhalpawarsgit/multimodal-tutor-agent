## Generate naration using OpenAI's text-to-speech model


"""Generate spoken explanations using OpenAI text-to-speech."""

from pathlib import Path
from uuid import uuid4

from utils.config import AUDIO_DIR, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE
from utils.tracing_utils import get_openai_client, traced_function


@traced_function("generate_audio")
def generate_audio(text: str) -> str:
    """
    Convert text into speech and return the generated MP3 path.

    Args:
        text: Explanation that should be narrated.

    Returns:
        Absolute path to the saved MP3 file.
    """
    if not text or not text.strip():
        raise ValueError("Cannot generate audio from empty text.")

    client = get_openai_client()

    # Create a unique output filename for this narration.
    output_path = AUDIO_DIR / f"{uuid4().hex}.mp3"

    # The speech endpoint returns audio bytes.
    # Use a tutor-like instruction to influence delivery.
    with client.audio.speech.with_streaming_response.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text[:4000],
        instructions=(
            "Speak clearly at a moderate pace, like a tutor "
            "explaining study material to a student."
        ),
        response_format="mp3",
    ) as response:

        # Stream the response to a file instead of keeping
        # the complete audio response in memory.
        response.stream_to_file(output_path)

    return str(output_path.resolve())
