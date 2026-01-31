import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.models.chat import ChatRole

class ChatMessageBase(BaseModel):
    role: ChatRole
    content: str

    model_config = ConfigDict(frozen=True)

class ChatMessageCreate(ChatMessageBase):
    session_id: uuid.UUID

class ChatMessageRead(ChatMessageBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    query: str
    session_id: uuid.UUID | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: uuid.UUID

class ChatSessionRead(BaseModel):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
