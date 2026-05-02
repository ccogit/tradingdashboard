import json
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.deps import get_current_user, get_db
from app.models.user import User
from app.models.chat import ChatSession
from app.schemas.copilot import ChatRequest

router = APIRouter()


@router.get("/copilot/sessions")
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.exec(select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.last_message_at.desc()))
    sessions = result.all()
    return [{"id": str(s.id), "title": s.title, "last_message_at": s.last_message_at.isoformat(), "created_at": s.created_at.isoformat()} for s in sessions]


@router.post("/copilot/chat")
async def chat(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.copilot_service import stream_chat

    async def generate():
        async for chunk in stream_chat(user, body.account_id, body.message, body.session_id, db):
            yield f"event: {chunk['type']}\ndata: {json.dumps(chunk['data'])}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.delete("/copilot/sessions/{session_id}", status_code=204)
async def delete_session(
    session_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.exec(select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id))
    session = result.first()
    if session:
        await db.delete(session)
        await db.commit()
