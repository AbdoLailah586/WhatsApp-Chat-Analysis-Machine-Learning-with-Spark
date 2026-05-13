from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.db_models import Message
from app.models.schemas import AnalyticsResponse
import collections

router = APIRouter(prefix="/api", tags=["analytics"])

@router.get("/analytics/{upload_id}", response_model=AnalyticsResponse)
async def get_analytics(upload_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message).filter(Message.upload_id == upload_id))
    messages = result.scalars().all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this upload_id")
        
    total_messages = len(messages)
    categorized_count = sum(1 for m in messages if m.category)
    uncategorized_count = total_messages - categorized_count
    
    category_distribution = collections.defaultdict(int)
    urgency_breakdown = collections.defaultdict(int)
    senders = collections.defaultdict(int)
    time_series_map = collections.defaultdict(int)
    
    for m in messages:
        if m.category:
            category_distribution[m.category] += 1
            if m.category == "Urgent":
                urgency_breakdown[m.sender] += 1
        
        senders[m.sender] += 1
        date_str = m.timestamp.strftime("%Y-%m-%d")
        time_series_map[date_str] += 1
        
    category_percentages = {
        cat: round((count / total_messages) * 100, 2)
        for cat, count in category_distribution.items()
    }
    
    top_senders = [{"sender": k, "count": v} for k, v in sorted(senders.items(), key=lambda item: item[1], reverse=True)[:10]]
    time_series = [{"date": k, "count": v} for k, v in sorted(time_series_map.items())]
    
    return AnalyticsResponse(
        category_distribution=category_distribution,
        category_percentages=category_percentages,
        time_series=time_series,
        top_senders=top_senders,
        urgency_breakdown=urgency_breakdown,
        total_messages=total_messages,
        categorized_count=categorized_count,
        uncategorized_count=uncategorized_count
    )
