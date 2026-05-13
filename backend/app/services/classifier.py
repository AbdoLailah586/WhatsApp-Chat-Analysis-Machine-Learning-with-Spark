import joblib
import numpy as np
from pathlib import Path
from typing import List, Dict
import sys
import os

from app.unified_categories import CATEGORIES, SAFETALK_MAPPING
from app.services.gemini_client import classify_media_context

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
MODEL_PATH = BASE_DIR / "SafeTalk-AI" / "backend" / "model" / "scam_detector.joblib"
VECTORIZER_PATH = BASE_DIR / "SafeTalk-AI" / "backend" / "model" / "vectorizer.joblib"

try:
    model = joblib.load(str(MODEL_PATH))
    vectorizer = joblib.load(str(VECTORIZER_PATH))
except Exception as e:
    print(f"Failed to load model from {MODEL_PATH}: {e}")
    model = None
    vectorizer = None

def classify_text_message(text: str) -> dict:
    if not model or not vectorizer:
        return {"category": "Not Important", "confidence_score": 0.0}
    
    vectorized = vectorizer.transform([text])
    prediction = model.predict(vectorized)[0]
    proba = np.max(model.predict_proba(vectorized))
    
    predicted_risk = prediction.lower()
    category = SAFETALK_MAPPING.get(predicted_risk, "Not Important")
    
    return {"category": category, "confidence_score": round(float(proba), 2)}

from app.services.keyword_classifier import classify_with_context

async def classify_batch(messages: List[Dict]) -> List[Dict]:
    results = []
    sender_stats = {}
    
    for i, msg in enumerate(messages):
        if msg.get("is_media"):
            prev_msgs = [m.get("content", "") for m in messages[max(0, i-3):i]]
            next_msgs = [m.get("content", "") for m in messages[i+1:min(len(messages), i+4)]]
            category = await classify_media_context(prev_msgs, next_msgs)
            results.append({
                **msg,
                "category": category,
                "confidence_score": 0.8
            })
            sender = msg.get("sender")
            if sender not in sender_stats:
                sender_stats[sender] = {}
            sender_stats[sender][category] = sender_stats[sender].get(category, 0) + 1
        else:
            text = msg.get("content", "")
            sender = msg.get("sender", "")
            timestamp = msg.get("timestamp")
            
            kw_res = classify_with_context(text, sender, timestamp, sender_stats)
            
            final_cat = kw_res["category"]
            final_conf = kw_res["confidence"]
            
            if final_conf < 50.0:
                ml_res = classify_text_message(text)
                if ml_res["category"] == "Spam":
                    final_cat = "Spam"
                    final_conf = ml_res["confidence_score"] * 100
                elif ml_res["confidence_score"] > 0.6 and ml_res["category"] != "Not Important":
                    final_cat = ml_res["category"]
                    final_conf = ml_res["confidence_score"] * 100
                    
            results.append({
                **msg,
                "category": final_cat,
                "confidence_score": round(final_conf / 100.0, 2)
            })
            
            if sender not in sender_stats:
                sender_stats[sender] = {}
            sender_stats[sender][final_cat] = sender_stats[sender].get(final_cat, 0) + 1
            
    return results
