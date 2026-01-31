import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.chat import ChatMessage, ChatSession


async def get_messages_by_session_id(
    db: AsyncSession,
    session_id: uuid.UUID,
    limit: int | None = None
) -> list[ChatMessage]:

    query = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.desc())
    )

    if limit:
        query = query.limit(limit)

    result = await db.execute(query)
    messages = result.scalars().all()

    return list(reversed(messages))


async def create_chat_session(
    db: AsyncSession
) -> ChatSession:
    session = ChatSession()
    db.add(session)
    return session


async def get_session_by_id(
    db: AsyncSession,
    session_id: uuid.UUID
) -> ChatSession | None:
    return await db.get(ChatSession, session_id)


async def add_messages(
    db: AsyncSession,
    messages: list[ChatMessage]
) -> None:
    if not messages:
        return

    db.add_all(messages)
    return None