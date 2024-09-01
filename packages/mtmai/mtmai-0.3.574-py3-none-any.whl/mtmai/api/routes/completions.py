import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.completion_create_params import (
    CompletionCreateParamsBase,
    CompletionCreateParamsStreaming,
)
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.agents.agent_api import get_agent_by_name_v3
from mtmai.api.deps import OptionalUserDep, SessionDep
from mtmai.mtlibs import aisdk

router = APIRouter()
logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


class ChatRequest(BaseModel):
    """前端 vercel ai sdk 客户端提交过来的聊天消息"""

    messages: any

    class Config:
        arbitrary_types_allowed = True


async def agent_chat_stream(
    *,
    user_id: str,
    agent_name: str | None = None,
    thread_id: str | None = None,
    user_input: str | None = None,
):
    agent = get_agent_by_name_v3(agent_name)
    if not agent:
        yield aisdk.text(f"error missing agent: {agent_name}")
        yield aisdk.finish()
        return

    async for chunck in agent.chat(
        user_id=user_id,
        user_input=user_input,
        thread_id=thread_id,
    ):
        yield chunck


# @traceable
@router.post("/chat/completions")
async def chat_completions(db: SessionDep, user: OptionalUserDep, request: Request):
    is_chat = request.headers.get("X-Is-Chat")
    agent_name = request.headers.get("X-AI-Agent")
    thread_id = request.headers.get("X-Chat-Id")

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

    cc = CompletionCreateParamsStreaming(chat_id=thread_id, **await request.json())
    logger.info(
        f"收到聊天消息请求, agent_name:{agent_name},chat_id:{thread_id}"  # noqa: G004
    )

    if cc["prompt"]:
        latest_message = ChatCompletionUserMessageParam(
            role="user", content=cc["prompt"]
        )
    else:
        latest_message = cc["messages"][-1]
    latest_user_input_content = latest_message["content"]
    response = response = StreamingResponse(
        agent_chat_stream(
            # db=db,
            agent_name=agent_name,
            user_id=user.id,
            user_input=latest_user_input_content,
            thread_id=thread_id,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
