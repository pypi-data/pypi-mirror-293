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


class MainState(BaseModel):
    # checked_emails_ids: list[str]
    # emails: list[dict] | None
    # action_required_emails: dict
    # some_value: str | None = None
    # messages: Annotated[list, add_messages]
    thread_id: str | None = None
    error: str | None = None
    user_input: str | None = None
    wait_user: bool | None = False
    # agent_name: str | None = "graphchatdemo999"
    user_id: str | None = None
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: Annotated[AgentContext, Context(make_agent_context)]
    config: DemoAgentConfig

    # 工具结果相关状态
    # web_search_results: str | None = None
