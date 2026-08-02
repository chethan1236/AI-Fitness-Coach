import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

print("=" * 60)
print("Available generateContent models")
print("=" * 60)

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
        print(model.supported_generation_methods)
        print("-" * 40)