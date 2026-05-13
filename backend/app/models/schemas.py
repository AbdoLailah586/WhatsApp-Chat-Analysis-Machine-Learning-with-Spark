from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MessageIn(BaseModel):
    sender: str
    timestamp: datetime
    content: str
    is_media: bool

class MessageOut(MessageIn):
    id: int
    upload_id: int
    category: Optional[str] = None
    confidence_score: Optional[float] = None
    
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    upload_id: int
    message_count: int

class ClassifyRequest(BaseModel):
    upload_id: int
    messages: List[MessageIn]

class ClassifyResponse(BaseModel):
    messages: List[MessageOut]

class AnalyticsResponse(BaseModel):
    category_distribution: Dict[str, int]
    category_percentages: Dict[str, float]
    time_series: List[Dict[str, Any]]
    top_senders: List[Dict[str, Any]] # e.g. [{"sender": "Meet", "count": 100}]
    urgency_breakdown: Dict[str, int]
    total_messages: int
    categorized_count: int
    uncategorized_count: int
