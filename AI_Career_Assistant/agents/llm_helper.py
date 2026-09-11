"""LangChain LLM Helper — returns a configured Gemini chat model."""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODELS_TO_TRY = ["gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]

def get_chat_model(temperature: float = 0.2, model_name: str = "gemini-3.1-flash-lite") -> ChatGoogleGenerativeAI:
    """Returns a ChatGoogleGenerativeAI model instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment or .env file.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )
