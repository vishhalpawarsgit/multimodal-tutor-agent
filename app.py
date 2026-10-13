## Streamlit UI and workflow for the multimodal tutor agent


"""Streamlit interface for the Multimodal Tutor Agent."""

from pathlib import Path
from uuid import uuid4

import streamlit as st

from utils.audio_utils import generate_audio
from utils.config import MAX_UPLOAD_MB, UPLOAD_DIR
from utils.openai_utils import analyze_image
from utils.pdf_utils import pdf_to_images


# Configure the page before creating other Streamlit elements.
st.set_page_config(
    page_title="Multimodal Tutor Agent",
    page_icon=":mortar_board:",
    layout="wide",
)

st.title("Multimodal Tutor Agent")

st.write(
    "Upload handwritten notes, diagrams, charts, code screenshots, "
    "or PDFs to generate explanations, revision notes, questions, "
    "a text-based mind map, and an audio explanation."
)

# Restrict file types in the interface.
uploaded_file = st.file_uploader(
    "Choose an image or PDF file",
    type=["jpg", "jpeg", "png", "pdf"],
)

if uploaded_file is not None:

    # Check file size before saving or processing.
    max_bytes = MAX_UPLOAD_MB * 1024 * 1024

    if uploaded_file.size > max_bytes:
        st.error(
            f"The file exceeds the {MAX_UPLOAD_MB} MB limit."
        )
        st.stop()

    # Create a safe, application-controlled filename.
    extension = Path(uploaded_file.name).suffix.lower()
    supported_extensions = {".jpg", ".jpeg", ".png", ".pdf"}

    if extension not in supported_extensions:
        st.error("Unsupported file type.")
        st.stop()

    upload_path = UPLOAD_DIR / f"{uuid4().hex}{extension}"

    # Save the uploaded bytes locally.
    upload_path.write_bytes(uploaded_file.getvalue())

    st.success(f"Uploaded: {uploaded_file.name}")

    # Convert PDFs into images; use images directly otherwise.
    try:
        if extension == ".pdf":
            with st.spinner("Converting PDF pages into images..."):
                image_paths = pdf_to_images(str(upload_path))
        else:
            image_paths = [str(upload_path)]

        if not image_paths:
            st.error("No images were available for analysis.")
            st.stop()

    except Exception as exc:
        st.error(f"File conversion failed: {exc}")
        st.stop()

    # Analyze each image and preserve page-level results.
    analysis_sections = []

    try:
        with st.spinner("Analyzing the uploaded material..."):
            for page_number, image_path in enumerate(
                image_paths, start=1
            ):
                # Call the OpenAI-backed, LangSmith-traced function.
                result = analyze_image(image_path)

                analysis_sections.append(
                    f"## Page/Image {page_number}\n\n{result}"
                )

        # Combine all page results for display and narration.
        combined_analysis = "\n\n---\n\n".join(analysis_sections)

        st.session_state["analysis"] = combined_analysis

    except Exception as exc:
        st.error(f"AI analysis failed: {exc}")
        st.exception(exc)
        st.stop()

    # Display the full result.
    st.subheader("Learning Material")
    st.markdown(st.session_state["analysis"])

    # Generate narration only when the user requests it.
    # This avoids paying for TTS on every Streamlit rerun.
    if st.button("Generate Audio Explanation"):
        try:
            with st.spinner("Generating spoken explanation..."):
                # Use a concise portion of the combined analysis.
                narration_text = st.session_state["analysis"][:4000]
                audio_path = generate_audio(narration_text)

            # Store the path in session state so it survives reruns.
            st.session_state["audio_path"] = audio_path
            st.success("Audio explanation generated.")

        except Exception as exc:
            st.error(f"Audio generation failed: {exc}")
            st.exception(exc)

    # Display the audio player if audio has been generated.
    audio_path = st.session_state.get("audio_path")

    if audio_path and Path(audio_path).is_file():
        st.subheader("Audio Explanation")

        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
