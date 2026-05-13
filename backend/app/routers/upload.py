from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.services.parser import parse_whatsapp
from app.models.db_models import Upload, Message
from app.models.schemas import UploadResponse
import sqlalchemy as sa

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=UploadResponse)
async def upload_chat(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
        
    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
        
    messages_data = parse_whatsapp(decoded_content)
    
    if not messages_data:
        raise HTTPException(status_code=400, detail="No valid messages found in the file")
        
    new_upload = Upload(filename=file.filename, message_count=len(messages_data))
    db.add(new_upload)
    await db.commit()
    await db.refresh(new_upload)
    
    db_messages = [
        Message(
            upload_id=new_upload.id,
            sender=m["sender"],
            timestamp=m["timestamp"],
            content=m["content"],
            is_media=m["is_media"]
        ) for m in messages_data
    ]
    db.add_all(db_messages)
    await db.commit()
    
    return UploadResponse(upload_id=new_upload.id, message_count=len(messages_data))

@router.get("/uploads")
async def list_uploads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Upload).order_by(Upload.uploaded_at.desc()))
    return result.scalars().all()

@router.get("/uploads/{upload_id}")
async def get_upload(upload_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Upload).filter(Upload.id == upload_id))
    upload = result.scalars().first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload
