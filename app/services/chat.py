import os
import httpx
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import ChatMessageBase, ChatMessageCreate
from app.repositories import chat as repos_chat
from app.models.chat import ChatMessage, ChatSession
from app.models.chat import ChatRole

AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://127.0.0.1:9000/process")

async def get_messages_by_session_id(
    db: AsyncSession,
    session_id: uuid.UUID,
    limit: int | None = None
) -> list[ChatMessageBase]:

    messages = await repos_chat.get_messages_by_session_id(
        db,
        session_id,
        limit=limit
    )

    return [
        ChatMessageBase(
            role=ChatRole(msg.role),
            content=msg.content
        )
        for msg in messages
    ]




async def create_chat_session(
    db: AsyncSession
) -> ChatSession:
    session = await repos_chat.create_chat_session(db)

    await db.flush()
    await db.refresh(session)

    return session


async def get_session_by_id(
    db: AsyncSession,
    session_id: uuid.UUID
) -> ChatSession | None:
    return await repos_chat.get_session_by_id(db, session_id)


async def add_chat_messages(
    db: AsyncSession,
    messages: list[ChatMessageCreate]
) -> None:
    if not messages:
        return

    models = [
        ChatMessage(
            session_id=msg.session_id,
            role=msg.role,
            content=msg.content
        )
        for msg in messages
    ]

    await repos_chat.add_messages(db, models)
