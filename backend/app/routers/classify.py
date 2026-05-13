from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.db_models import Upload, Message
from app.models.schemas import ClassifyRequest, ClassifyResponse, MessageOut
from app.services.classifier import classify_batch

router = APIRouter(prefix="/api", tags=["classify"])

@router.post("/classify", response_model=ClassifyResponse)
async def classify_messages(request: ClassifyRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Upload).filter(Upload.id == request.upload_id))
    upload = result.scalars().first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
        
    # We ignore the messages list from request to maintain truth from DB
    db_msgs_result = await db.execute(select(Message).filter(Message.upload_id == request.upload_id).order_by(Message.timestamp))
    db_msgs = db_msgs_result.scalars().all()
    
    messages_dicts = [
        {
            "id": m.id,
            "sender": m.sender,
            "timestamp": m.timestamp,
            "content": m.content,
            "is_media": m.is_media
        } for m in db_msgs
    ]
    
    classified_messages = await classify_batch(messages_dicts)
    
    response_messages = []
    
    for i, db_m in enumerate(db_msgs):
        if i < len(classified_messages):
            c_msg = classified_messages[i]
            db_m.category = c_msg["category"]
            db_m.confidence_score = c_msg["confidence_score"]
            
            response_messages.append(
                MessageOut(
                    id=db_m.id,
                    upload_id=db_m.upload_id,
                    sender=db_m.sender,
                    timestamp=db_m.timestamp,
                    content=db_m.content,
                    is_media=db_m.is_media,
                    category=db_m.category,
                    confidence_score=db_m.confidence_score
                )
            )
            
    upload.status = "classified"
    await db.commit()
    
    return ClassifyResponse(messages=response_messages)

@router.post("/{upload_id}/reclassify", response_model=ClassifyResponse)
async def reclassify_messages(upload_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Upload).filter(Upload.id == upload_id))
    upload = result.scalars().first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
        
    db_msgs_result = await db.execute(select(Message).filter(Message.upload_id == upload_id).order_by(Message.timestamp))
    db_msgs = db_msgs_result.scalars().all()
    
    messages_dicts = [
        {
            "id": m.id,
            "sender": m.sender,
            "timestamp": m.timestamp,
            "content": m.content,
            "is_media": m.is_media
        } for m in db_msgs
    ]
    
    classified_messages = await classify_batch(messages_dicts)
    
    response_messages = []
    for i, db_m in enumerate(db_msgs):
        if i < len(classified_messages):
            c_msg = classified_messages[i]
            db_m.category = c_msg["category"]
            db_m.confidence_score = c_msg["confidence_score"]
            response_messages.append(MessageOut.model_validate(db_m))
            
    upload.status = "reclassified"
    await db.commit()
    
    return ClassifyResponse(messages=response_messages)
