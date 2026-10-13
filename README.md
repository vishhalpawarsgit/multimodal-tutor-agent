
# Multimodal Tutor Agent

An educational assistant that analyzes images and PDF documents
using OpenAI, generates structured learning material, and creates
spoken explanations. LangSmith provides application tracing.

## Features

- Upload PNG, JPG, JPEG, and PDF documents.
- Convert PDF pages into images.
- Analyze notes, diagrams, charts, and code screenshots.
- Generate detailed explanations and revision notes.
- Create important-concept lists and assignment questions.
- Generate a text-based mind map.
- Create MP3 narration using OpenAI text-to-speech.
- Trace supported OpenAI calls and application functions in LangSmith.

## Prerequisites

- macOS
- Python 3.11 or 3.12
- uv
- VS Code
- OpenAI API key
- LangSmith API key
- Homebrew, Poppler, and Tesseract if using PDF conversion
  and the optional local OCR utility

## Setup

Clone the repository and open the project directory:

    git clone https://github.com/vishhalpawarsgit/multimodal-tutor-agent.git
    cd multimodal-tutor-agent

Install uv if necessary:

    curl -LsSf https://astral.sh/uv/install.sh | sh

Create and activate a virtual environment:

    uv venv --python 3.11
    source .venv/bin/activate

Install project dependencies:

    uv sync

If you are maintaining only a requirements.txt workflow instead,
install those dependencies with:

    uv pip install -r requirements.txt

Create the environment file:

    cp .env.example .env

Edit .env and configure the required OpenAI and LangSmith keys.

Install system dependencies for PDF conversion and OCR:

    brew install poppler tesseract

## Run the Streamlit application

    uv run streamlit run app.py

Open the local URL printed by Streamlit, typically:

    http://localhost:8501

## Test image analysis directly

    uv run python main.py uploads/sample.png

Replace the example path with an actual image.

## LangSmith observability

Set these variables in .env:

    LANGSMITH_TRACING=true
    LANGSMITH_API_KEY=your_langsmith_api_key
    LANGSMITH_PROJECT=multimodal-tutor-agent
    LANGSMITH_ENDPOINT=https://api.smith.langchain.com

Open LangSmith and select the project named
multimodal-tutor-agent to inspect traces.

## Troubleshooting

- Check that OPENAI_API_KEY is valid and has API access.
- Confirm that the configured model is available to your account.
- Verify Poppler using `pdftoppm -v`.
- Verify Tesseract using `tesseract --version`.
- Run `uv run python main.py path/to/image.png` to isolate
  image-analysis failures from Streamlit UI issues.
- Confirm LangSmith tracing is enabled and the API key is valid.

## Security

Never commit .env, uploaded documents, generated audio, or API keys.
Review LangSmith data-retention and access policies before tracing
sensitive educational, personal, or enterprise documents.

## Limitations

The application analyzes PDF pages individually. It does not yet
provide persistent conversational memory, interactive quizzes,
or an interactive graphical mind map.
