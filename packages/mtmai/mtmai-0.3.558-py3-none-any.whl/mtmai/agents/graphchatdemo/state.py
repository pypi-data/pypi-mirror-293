import operator
from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel
from langgraph.channels.context import Context

# from pydantic import BaseModel
from mtmai.agents.graphchatdemo.context import AgentContext, make_agent_context


class DemoAgentConfig(BaseModel):
    name: str | None = None
    default_llm: str | None = None
    prompt_default: str | None = None


# class UiStateItem(BaseModel):
#     comp_type: str
#     props: dict | None = None


class UiState(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # items: list[UiStateItem] | None = []
    isOpenAgentRagView: bool | None = False
    threadId: str | None = None


class UiCommandsItem(BaseModel):
    name: str
    args: dict


# class UiCommands(BaseModel):
#     class Config:
#         arbitrary_types_allowed = True

#     commands: list[UiCommandsItem]


class UiAppendComponentItem(BaseModel):
    component: str
    props: dict


# class UiAppendComponent(BaseModel):
#     items: list[UiAppendComponentItem]


class UiDelta(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # 过时 ?
    # isOpenAgentRagView: bool | None = False
    # uiStateDelta: UiStateDelta | None = None

    uiappendcomponents: list[UiAppendComponentItem] | None = None
    commands: list[UiCommandsItem] | None = None


class MainState(BaseModel):
    # emails: list[dict] | None
    # action_required_emails: dict
    # messages: Annotated[list, add_messages]
    error: str | None = None
    user_input: str | None = None
    wait_user: bool | None = False
    user_id: str | None = None
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: Annotated[AgentContext, Context(make_agent_context)]
    config: DemoAgentConfig
    # uistate: UiState | None = None
    uidelta: UiDelta | None = None

    # 工具结果相关状态
    # web_search_results: str | None = None
