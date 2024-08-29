import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langsmith import traceable
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import (
    CompletionCreateParamsBase,
    CompletionCreateParamsStreaming,
)
from opentelemetry import trace
from pydantic import BaseModel
from sqlmodel import Session

from mtmai.agents.agent_api import get_agent_by_name
from mtmai.api.deps import OptionalUserDep, SessionDep
from mtmai.core.db import getdb
from mtmai.curd.curd_chat import ChatSubmitPublic, submit_chat_messages
from mtmai.models.chat import ChatMessage
from mtmai.models.models import User
from mtmai.mtlibs import aisdk

if TYPE_CHECKING:
    from langchain_core.messages import AIMessage


router = APIRouter()
logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


async def agent_chat_stream(
    *,
    db: Session,
    user: User,
    chat_messages: list[ChatCompletionMessageParam],
    agent_name: str | None = None,
    chat_id: str | None = None,
):
    chat_input = submit_chat_messages(
        db=db,
        data=ChatSubmitPublic(
            chat_id=chat_id, agent_name=agent_name, messages=chat_messages
        ),
        owner_id=user.id,
    )

    agent = get_agent_by_name(agent_name)
    if not agent:
        yield aisdk.text(f"error missing agent: {agent_name}")
        yield aisdk.finish()
        return

    agent_executor = await agent.chatbot_agent(messages=chat_messages, chat_id=chat_id)

    async for event in agent_executor.astream_events(
        {
            "chat_history": chat_messages,
        },
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if event["name"] == "Agent":
                logger.info("Starting agent %s", agent_name)
        elif kind == "on_chain_end":  # noqa: SIM102
            if event["name"] == "Agent":
                ai_content = event["data"].get("output")
                messages: list[AIMessage] = ai_content.get("messages")
                for msg in messages:
                    new_message = ChatMessage(
                        id=msg.id,
                        content=msg.content,
                        chat_id=chat_id,
                        role="assistant",
                    )
                    with Session(getdb()) as session:
                        session.add(new_message)
                        session.commit()
                        session.refresh(new_message)
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield aisdk.text(content)
        elif kind == "on_tool_start":
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            ai_content = event["data"].get("output")
            print(f"Tool output was: {ai_content}")

    data = {
        # "openDlg": True,
    }
    if not chat_id:
        data["chatId"] = chat_input.id
    yield aisdk.data(
        [
            {
                "dataType": "uistate",
                "data": data,
            }
        ]
    )

    yield aisdk.finish()


class ChatRequest(BaseModel):
    """前端 vercel ai sdk 客户端提交过来的聊天消息"""

    messages: any

    class Config:  # noqa: D106
        arbitrary_types_allowed = True


class ChatMessageRequest(BaseModel):
    chat_id: str

    agent: str
    messages: list[ChatCompletionMessageParam]


@traceable
@router.post("/chat/completions")
async def chat_completions(db: SessionDep, user: OptionalUserDep, request: Request):
    is_chat = request.headers.get("X-Is-Chat")
    agent_name = request.headers.get("X-AI-Agent")
    chat_id = request.headers.get("X-Chat-Id")

    if is_chat is None:
        # openai /vi/chat/completionss 官方兼容
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

    cc = CompletionCreateParamsStreaming(chat_id=chat_id, **await request.json())
    logger.info(
        f"收到聊天消息请求, agent_name:{agent_name},chat_id:{chat_id}"  # noqa: G004
    )
    response = response = StreamingResponse(
        agent_chat_stream(
            db=db,
            chat_messages=cc["messages"],
            agent_name=agent_name,
            chat_id=chat_id,
            user=user,
        )
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
