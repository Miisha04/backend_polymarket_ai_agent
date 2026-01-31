from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.chat import ChatRole
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageCreate
from app.services import chat as chat_service
from app.services import agent as agent_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/invoke", response_model=ChatResponse)
async def invoke_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_session)
):

    # 1️⃣ session
    session = (
        await chat_service.get_session_by_id(db, request.session_id)
        if request.session_id
        else None
    )

    if not session:
        session = await chat_service.create_chat_session(db)

    # 2️⃣ history
    history = await chat_service.get_messages_by_session_id(
        db,
        session.id,
        limit=50
    )

    history_payload = [
        {"role": m.role.value, "content": m.content}
        for m in history
    ]

    # 3️⃣ agent call
    try:
        assistant_answer = await agent_service.invoke_agent(
            query=request.query,
            history=history_payload
        )
    except agent_service.AgentServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # 4️⃣ persist
    await chat_service.add_chat_messages(
        db,
        [
            ChatMessageCreate(
                session_id=session.id,
                role=ChatRole.user,
                content=request.query
            ),
            ChatMessageCreate(
                session_id=session.id,
                role=ChatRole.assistant,
                content=assistant_answer
            ),
        ]
    )

    await db.commit()

    return ChatResponse(
        response=assistant_answer,
        session_id=session.id
    )
