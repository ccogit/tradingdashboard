import time
from typing import AsyncGenerator, Optional
from uuid import UUID
import anthropic
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.config import get_settings
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage, ToolCall
from app.ai.tools import TOOLS
from app.ai.prompts import SYSTEM_PROMPT
from app.utils.ids import new_uuid
from app.utils.time import utcnow
import logging

logger = logging.getLogger(__name__)


async def stream_chat(
    user: User,
    account_id: str,
    message: str,
    session_id: Optional[UUID],
    db: AsyncSession,
) -> AsyncGenerator[dict, None]:
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    # Get or create session
    if session_id:
        result = await db.exec(select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id))
        session = result.first()
    else:
        session = None

    if not session:
        session = ChatSession(
            id=new_uuid(),
            user_id=user.id,
            account_id=UUID(account_id),
            title=message[:50],
        )
        db.add(session)
        await db.commit()

    # Persist user message
    user_msg = ChatMessage(
        id=new_uuid(),
        session_id=session.id,
        role="user",
        content_json=[{"type": "text", "text": message}],
    )
    db.add(user_msg)
    await db.commit()

    # Load history
    result = await db.exec(
        select(ChatMessage).where(ChatMessage.session_id == session.id).order_by(ChatMessage.created_at)
    )
    history = result.all()
    messages = [{"role": m.role, "content": m.content_json} for m in history if m.role in ("user", "assistant")]

    ctx = {"user": user, "account_id": account_id, "db": db, "session_id": str(session.id)}

    # Agentic loop
    while True:
        response = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        assistant_content = []
        for block in response.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
                yield {"type": "text_delta", "data": {"session_id": str(session.id), "text": block.text}}
            elif block.type == "tool_use":
                tool_call_id = block.id
                assistant_content.append({"type": "tool_use", "id": tool_call_id, "name": block.name, "input": block.input})
                yield {"type": "tool_use", "data": {"session_id": str(session.id), "tool_call_id": tool_call_id, "name": block.name, "input": block.input}}

        # Persist assistant message
        asst_msg = ChatMessage(
            id=new_uuid(),
            session_id=session.id,
            role="assistant",
            content_json=assistant_content,
            model=settings.anthropic_model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        db.add(asst_msg)
        await db.commit()

        if response.stop_reason != "tool_use":
            yield {"type": "message_complete", "data": {"session_id": str(session.id), "message_id": str(asst_msg.id)}}
            break

        # Process tool calls
        messages.append({"role": "assistant", "content": assistant_content})
        tool_results = []

        from app.ai.handlers import HANDLERS
        for block in response.content:
            if block.type != "tool_use":
                continue
            start = time.monotonic()
            is_error = False
            try:
                handler = HANDLERS.get(block.name)
                if handler:
                    result = await handler(block.input, ctx)
                else:
                    result = {"error": f"Unknown tool: {block.name}"}
                    is_error = True
            except Exception as e:
                result = {"error": str(e)}
                is_error = True

            duration_ms = int((time.monotonic() - start) * 1000)

            tc = ToolCall(
                id=new_uuid(),
                message_id=asst_msg.id,
                tool_use_id=block.id,
                name=block.name,
                input_json=block.input,
                output_json=result,
                is_error=is_error,
                duration_ms=duration_ms,
            )
            db.add(tc)
            await db.commit()

            yield {"type": "tool_result", "data": {"session_id": str(session.id), "tool_call_id": block.id, "output": result, "is_error": is_error}}

            if block.name == "stage_order":
                yield {"type": "staged_order", "data": {"session_id": str(session.id), "staged_order_id": block.id, "order": result.get("order", {})}}

            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(result)})

        messages.append({"role": "user", "content": tool_results})

    session.last_message_at = utcnow()
    db.add(session)
    await db.commit()
    yield {"type": "done", "data": {"session_id": str(session.id)}}
