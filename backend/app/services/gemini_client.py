import google.generativeai as genai
from typing import List
import os
import os

from app.unified_categories import CATEGORIES
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
generation_config = {
  "temperature": 0.1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 100,
}

async def classify_media_context(prev_messages: List[str], next_messages: List[str]) -> str:
    context_text = "Previous 3 messages:\n" + "\n".join(prev_messages) + "\n\nNext 3 messages:\n" + "\n".join(next_messages)
    
    prompt = f"""
    Based on the following surrounding WhatsApp messages, guess the category of the omitted media file.
    Allowed Categories: {', '.join(CATEGORIES)}.
    Only return the category name, nothing else.
    
    Context:
    {context_text}
    """
    
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        for category in CATEGORIES:
            if category.lower() in result.lower():
                return category
                
        return "Not Important"
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Not Important"
