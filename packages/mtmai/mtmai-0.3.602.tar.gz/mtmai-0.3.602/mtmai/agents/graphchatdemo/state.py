import operator
from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage

# from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langgraph.channels.context import Context
from typing_extensions import TypedDict

# from pydantic import BaseModel
from mtmai.agents.graphchatdemo.context import AgentContext, make_agent_context


class DemoAgentConfig(TypedDict):
    name: str | None = None
    default_llm: str | None = None
    prompt_default: str | None = None


class UiChatItem(TypedDict, total=False):
    id: str | None = None
    component: str | None = None
    props: dict | None = None


class UiCommandsItem(TypedDict):
    name: str
    args: dict


class ExampleInputItem(TypedDict):
    title: str
    description: str
    content: str


class UIChatMessageItem(TypedDict):
    compType: str
    props: dict


class ChatBotUiState(TypedDict, total=False):
    agent: str | None = None
    isOpenAgentRagView: bool | None = False
    threadId: str | None = None
    agent_url_base: str | None = None
    graph_image_url: str | None = None
    isDev: bool | None = False
    isOpenRagUi: bool | None = False
    isOpenSearchView: bool | None = False
    isOpenMtmEditor: bool | None = False
    uichatitems: list[UIChatMessageItem] | None = None

    ui_messages: list[UiChatItem] | None = None
    example_input_items: list[ExampleInputItem]


class UiDelta(TypedDict):
    class Config:
        arbitrary_types_allowed = True

    commands: list[UiCommandsItem] | None = None
    uiState: ChatBotUiState | None = None


class MainState(TypedDict):
    # emails: list[dict] | None
    # action_required_emails: dict
    # messages: Annotated[list, add_messages]
    error: str | None = None
    user_input: str | None = None
    user_option: str | None = None
    # wait_user: bool | None = False
    user_id: str | None = None
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: Annotated[AgentContext, Context(make_agent_context)]
    config: DemoAgentConfig
    # uistate: UiState | None = None
    uidelta: UiDelta | None = None

    wait_editor_content: bool = False
    go_mtmeditor: bool = False

    # 工具结果相关状态
    # web_search_results: str | None = None
