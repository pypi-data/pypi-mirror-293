import operator
from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langgraph.channels.context import Context
from pydantic import BaseModel

# from pydantic import BaseModel
from mtmai.agents.graphchatdemo.context import AgentContext, make_agent_context


class DemoAgentConfig(BaseModelV1):
    name: str | None = None
    default_llm: str | None = None
    prompt_default: str | None = None


class ChatBotUiState(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    isOpenAgentRagView: bool | None = False
    threadId: str | None = None
    isDef: bool | None = False
    isOpenRagUi: bool | None = False


class UiCommandsItem(BaseModelV1):
    name: str
    args: dict


class UiAppendComponentItem(BaseModelV1):
    component: str


class UiDelta(BaseModelV1):
    class Config:
        arbitrary_types_allowed = True

    uiappendcomponents: list[UiAppendComponentItem] | None = None
    commands: list[UiCommandsItem] | None = None
    uiState: ChatBotUiState | None = None


class MainState(BaseModelV1):
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
