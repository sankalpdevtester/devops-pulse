from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
from src.models.endpoints import Endpoint
from src.utils.helpers import get_db
from src.utils.webhooks import triggerWebhook

router = APIRouter()

class Webhook(BaseModel):
    webhook_url: str
    webhook_event: str
    webhook_secret: str

@router.post("/webhooks")
async def create_webhook(webhook: Webhook, db: Session = Depends(get_db)):
    try:
        new_webhook = WebhookModel(webhook_url=webhook.webhook_url, webhook_event=webhook.webhook_event, webhook_secret=webhook.webhook_secret)
        db.add(new_webhook)
        db.commit()
        db.refresh(new_webhook)
        return {"message": "Webhook created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhooks/test")
async def test_webhook(webhook: Webhook, db: Session = Depends(get_db)):
    try:
        await triggerWebhook(webhook.webhook_url, webhook.webhook_event, webhook.webhook_secret)
        return {"message": "Webhook tested successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/webhooks")
async def get_webhooks(db: Session = Depends(get_db)):
    try:
        webhooks = db.query(WebhookModel).all()
        return [{"webhook_url": webhook.webhook_url, "webhook_event": webhook.webhook_event, "webhook_secret": webhook.webhook_secret} for webhook in webhooks]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class WebhookModel(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True)
    webhook_url = Column(String)
    webhook_event = Column(String)
    webhook_secret = Column(String)