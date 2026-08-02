"""Temporary script to list available Google Gemini models supporting generateContent."""

from __future__ import annotations
from pathlib import Path
import sys

import google.generativeai as genai

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.config import settings


def main() -> None:
    if not settings.gemini_api_key:
        raise RuntimeError("AI_FITNESS_GEMINI_API_KEY is not configured")

    genai.configure(api_key=settings.gemini_api_key)
    print("Available Gemini models supporting generateContent:")
    for model in genai.list_models():
        model_name = getattr(model, "name", None) or getattr(model, "id", None) or str(model)
        supported_methods = getattr(model, "supported_generation_methods", None)
        if supported_methods is None:
            supported_methods = getattr(model, "supported_generation_models", None)

        if supported_methods and "generateContent" in supported_methods:
            print(model_name)


if __name__ == "__main__":
    main()
