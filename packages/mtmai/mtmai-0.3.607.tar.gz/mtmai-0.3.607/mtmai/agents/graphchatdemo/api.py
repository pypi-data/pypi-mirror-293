import logging

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.agents.graphchatdemo.graph import GraphChatDemoAgent
from mtmai.api.deps import OptionalUserDep, SessionDep

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
    thread_id: str | None = None,
    prompt: str | None = None,
    option=None,
):
    agent_inst = GraphChatDemoAgent()
    async for chunck in agent_inst.chat(
        user_id=user_id,
        prompt=prompt,
        option=option,
        thread_id=thread_id,
    ):
        yield chunck


@router.post("")
async def chat(db: SessionDep, user: OptionalUserDep, request: Request):
    # todo: 第一个聊天消息触发 工作流的启动 并且 工作流的启动带动前端界面的初始化。
    # 好处是 无需额外的api 来进行所谓的 元数据及配置项的获取，所有前端需要的配置项，将 以 uidetail 的方式将状态数据传递到前端。
    # agent_name = request.headers.get("X-Ai-Agent")
    thread_id = request.headers.get("X-Thread-Id")
    payload = await request.json()
    response = response = StreamingResponse(
        agent_chat_stream(
            user_id=user.id,
            prompt=payload.get("prompt"),
            option=payload.get("option"),
            thread_id=thread_id,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


@router.post("/editor")
async def editor(db: SessionDep, user: OptionalUserDep, request: Request):
    """前端 ai 可视化编辑器 endpoint"""
    thread_id = request.headers.get("X-Thread-Id")
    payload = await request.json()
    response = response = StreamingResponse(
        agent_chat_stream(
            user_id=user.id,
            prompt=payload.get("prompt"),
            option=payload.get("option"),
            thread_id=thread_id,
        ),
        media_type="text/event-stream",
    )
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


@router.get("/graph_image")
async def graph_image(user: OptionalUserDep):
    agent_inst = GraphChatDemoAgent()

    image_data = agent_inst.build_flow().compile().get_graph(xray=1).draw_mermaid_png()
    return Response(content=image_data, media_type="image/png")
