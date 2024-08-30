import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langsmith import traceable
from openai.types.chat.completion_create_params import (
    CompletionCreateParamsBase,
    CompletionCreateParamsStreaming,
)
from opentelemetry import trace
from pydantic import BaseModel
from sqlmodel import Session

from mtmai.agents.agent_api import get_agent_by_name_v2
from mtmai.api.deps import OptionalUserDep, SessionDep
from mtmai.curd.curd_chat import ChatSubmitPublic, submit_chat_messages
from mtmai.models.models import User
from mtmai.mtlibs import aisdk

router = APIRouter()
logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


class ChatRequest(BaseModel):
    """前端 vercel ai sdk 客户端提交过来的聊天消息"""

    messages: any

    class Config:  # noqa: D106
        arbitrary_types_allowed = True


async def agent_chat_stream(
    *,
    db: Session,
    user: User | None = None,
    # chat_messages: list[ChatCompletionMessageParam],
    agent_name: str | None = None,
    conversation_id: str | None = None,
):
    agent = get_agent_by_name_v2(agent_name)
    if not agent:
        yield aisdk.text(f"error missing agent: {agent_name}")
        yield aisdk.finish()
        return

    async for chunck in agent().chat(
        # messages=chat_messages,
        conversation_id=conversation_id,
        db=db,
        user=user,
    ):
        yield chunck


@traceable
@router.post("/chat/completions")
async def chat_completions(db: SessionDep, user: OptionalUserDep, request: Request):
    is_chat = request.headers.get("X-Is-Chat")
    agent_name = request.headers.get("X-AI-Agent")
    conversation_id = request.headers.get("X-Chat-Id")

    if is_chat is None:
        # 这里的功能未 完全实现, 以后慢慢修改
        try:
            req = await request.json()
            logger.info("api completions %s", req)
            chat_id = "75ced3bca3794f86"
            cc: CompletionCreateParamsBase = None
            cc = CompletionCreateParamsStreaming(**req)
            return StreamingResponse(
                agent_chat_stream(cc["messages"], "demo", chat_id),
                media_type="text/event-stream",
            )
        except Exception as e:
            logger.exception("get_response_openai Error: %s", e)  # noqa: TRY401
            raise HTTPException(503)

    cc = CompletionCreateParamsStreaming(
        chat_id=conversation_id, **await request.json()
    )
    logger.info(
        f"收到聊天消息请求, agent_name:{agent_name},chat_id:{conversation_id}"  # noqa: G004
    )

    # a =cc["messages"][-1]
    # user_message = ChatMessage(
    #     role="user",
    #     content=a.content,
    #     chat_id=conversation_id
    # )
    conversation = submit_chat_messages(
        db=db,
        data=ChatSubmitPublic(
            chat_id=conversation_id, agent_name=agent_name, messages=cc["messages"]
        ),
        owner_id=user.id,
    )
    response = response = StreamingResponse(
        agent_chat_stream(
            db=db,
            # chat_messages=cc["messages"],
            agent_name=agent_name,
            conversation_id=conversation.id,
            user=user,
        )
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
