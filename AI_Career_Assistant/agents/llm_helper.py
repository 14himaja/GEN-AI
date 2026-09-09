"""
Simple LangChain LLM Helper for Beginners.

This module provides a single, easy-to-use function to get the Google Gemini Chat Model.
Uses 'gemini-3.1-flash-lite' (fast, reliable, fresh quota) and falls back to 'gemini-3.5-flash'.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Ordered list of models that have active free quota
MODELS_TO_TRY = ["gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]

def get_chat_model(temperature: float = 0.2, model_name: str = "gemini-3.1-flash-lite") -> ChatGoogleGenerativeAI:
    """
    Returns a LangChain ChatGoogleGenerativeAI model instance.
    Defaults to 'gemini-3.1-flash-lite' which has active quota and instant responses.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment or .env file.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )
