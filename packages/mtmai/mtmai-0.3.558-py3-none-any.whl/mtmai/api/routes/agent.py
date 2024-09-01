from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func
from sqlmodel import Session, SQLModel, select

from mtmai.agents.agent_api import get_agent_by_name_v3
from mtmai.api.deps import OptionalUserDep, SessionDep
from mtmai.core.config import settings
from mtmai.core.db import get_session
from mtmai.curd.curd_chat import get_conversation_messages
from mtmai.models.agent import AgentChatConfig, AgentMeta
from mtmai.models.chat import MtmChatMessage, MtmChatMessageBase

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

router = APIRouter()


class AgentsPublic(SQLModel):
    data: list[AgentMeta]
    count: int


all_agents = [
    AgentMeta(
        id="joke",
        name="joke",
        label="冷笑话",
        description="笑话生成器",
        chat_url=settings.API_V1_STR + "/joke/chat",
        can_chat=False,
        agent_type="common",
        chat_agent_config=AgentChatConfig(),
    ),
    AgentMeta(
        id="joke",
        name="blogwriter",
        label="博客写手",
        description="博客写手",
        chat_url=settings.API_V1_STR + "/blogwriter/chat",
        can_chat=False,
        agent_type="graphq",
        graph_image=settings.API_V1_STR + "/blogwriter/image",
    ),
    AgentMeta(
        id="mteditor",
        name="mteditor",
        label="智能文章编辑器",
        description="智能文章编辑器",
        # chat_url=settings.API_V1_STR + "/mteditor/chat",
        can_chat=False,
        agent_type="common",
        graph_image=settings.API_V1_STR + "/mteditor/image",
    ),
    AgentMeta(
        id="simplechat",
        name="simplechat",
        label="智能文章编辑器",
        description="智能文章编辑器",
        # chat_url=settings.API_V1_STR + "/chat/chat",
        can_chat=False,
        agent_type="chat",
        chat_agent_config=AgentChatConfig(),
    ),
    AgentMeta(
        id="grephdemo",
        name="grephdemo",
        label="GraphDemo",
        description="GraphDemo",
        can_chat=False,
        agent_type="chat",
        chat_agent_config=AgentChatConfig(),
    ),
    AgentMeta(
        id="graphchatdemo",
        name="graphchatdemo",
        label="练习演示 基于 graph 的聊天机器人",
        description="练习演示 基于 graph 的聊天机器人",
        can_chat=True,
        agent_type="chat",
        chat_agent_config=AgentChatConfig(),
        is_dev=True,
    ),
]


# @router.get("", response_model=AgentsPublic)
# def items(
#     db: SessionDep,
#     user: OptionalUserDep,
#     skip: int = 0,
#     limit: int = 100,
# ):
#     return AgentsPublic(data=all_agents, count=len(all_agents))


@router.get(
    "",
    summary="获取 Agent 列表",
    description=(
        "此端点用于获取 agent 列表。支持分页功能，"
        "可以通过 `skip` 和 `limit` 参数控制返回的 agent 数量。"
    ),
    response_description="返回包含所有 agent 的列表及总数。",
    response_model=AgentsPublic,
    responses={
        200: {
            "description": "成功返回 agent 列表",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"name": "agent1", "status": "active"},
                            {"name": "agent2", "status": "inactive"},
                        ],
                        "count": 2,
                    }
                }
            },
        },
        401: {"description": "未经授权的请求"},
        500: {"description": "服务器内部错误"},
    },
)
def items(
    # db: SessionDep,
    user: OptionalUserDep,
    skip: int = 0,
    limit: int = 100,
):
    return AgentsPublic(data=all_agents, count=len(all_agents))


@router.get("/{agent_id}", response_model=AgentMeta | None)
def get_item(db: SessionDep, user: OptionalUserDep, agent_id: str):
    for agent in all_agents:
        if agent.id == agent_id:
            return agent
    return None


@router.get(
    "/{agent_id}/image",
    summary="获取工作流图像",
    description="此端点通过给定的 agent ID，生成工作流的图像并返回 PNG 格式的数据。",
    response_description="返回 PNG 格式的工作流图像。",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"description": "Agent 未找到"},
    },
)
async def get_workflow_image(user: OptionalUserDep, agent_id: str):
    agent = get_agent_by_name_v3(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 未找到")

    app = agent.build_flow().compile(
        # checkpointer=checkpointer,
        # interrupt_before=["uidelta_node"]
        # interrupt_after=["uidelta_node"],
    )

    image_data = app.get_graph(xray=1).draw_mermaid_png()
    return Response(content=image_data, media_type="image/png")


@router.get(
    "/{agent_id}/{thread_id}/state",
    summary="获取工作流状态",
    description="",
    response_description="返回工作流当前完整状态数据",
)
async def get_workflow_state(user: OptionalUserDep, agent_id: str, thread_id: str):
    agent = get_agent_by_name_v3(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent 未找到")

    thread: RunnableConfig = {"configurable": {"thread_id": thread_id}}
    state = agent.app.get_state(thread)
    return state


class AgentMessageItemPublic(MtmChatMessageBase):
    agent_id: str


class AgentMessagePublic(SQLModel):
    data: list[AgentMessageItemPublic]
    count: int


@router.get("/{agent_id}/messages", response_model=AgentMessagePublic)
async def messages(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    user: OptionalUserDep,
    agent_id: str,
):
    if not user:
        return None

    count_statement = (
        select(func.count())
        .select_from(MtmChatMessage)
        .where(MtmChatMessage.owner_id == user.id)
    )
    count = session.exec(count_statement).one()
    items = get_conversation_messages(
        db=session, offset=offset, limit=limit, conversation_id=agent_id
    )
    return AgentMessagePublic(data=items, count=count)
