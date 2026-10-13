
"""Shared OpenAI client and LangSmith tracing utilities."""

from functools import lru_cache

from langsmith import traceable
from langsmith.wrappers import wrap_openai
from openai import OpenAI

from utils.config import required_env


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """
    Create one reusable OpenAI client.

    wrap_openai adds LangSmith instrumentation to supported
    OpenAI calls made through this client.
    """
    api_key = required_env("OPENAI_API_KEY")

    # Construct the standard OpenAI SDK client.
    base_client = OpenAI(api_key=api_key)

    # Instrument the client for LangSmith tracing.
    return wrap_openai(base_client)


def traced_function(name: str):
    """
    Create a named LangSmith trace decorator.

    Keeping this helper makes the trace names consistent
    throughout the application.
    """
    return traceable(
        name=name,
        run_type="chain",
    )
