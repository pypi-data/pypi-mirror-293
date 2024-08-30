import logging
from typing import Literal

from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from sqlmodel import Session

from mtmai.agents.graphchatdemo.state import MainState
from mtmai.curd.curd_chat import (
    ChatSubmitPublic,
    get_conversation_messages,
    submit_chat_messages,
)
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()


def should_continue(state: MainState) -> Literal["__end__", "tools", "continue"]:
    messages = state.messages
    last_message = messages[-1]

    if state.wait_user:
        return "ask_human"
    # if state.wait_user:
    #     return "chat"

    if last_message.tool_calls:
        return "tools"
    # if not last_message.tool_calls:
    #     return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


class Nodes:
    def __init__(self):
        pass

    async def entry(self, state: MainState, config: RunnableConfig):
        db = state.context.db
        if not state.user_input and not state.message:
            return {"error": "require user input"}

        if len(state.messages) == 0:
            state.messages = [ChatMessage(role="user", content=state.user_input)]
        # 如果没有 conversation_id, 表示新的聊天
        with Session(db) as session:
            latest_message = state.messages[-1]
            conversation = submit_chat_messages(
                db=session,
                data=ChatSubmitPublic(
                    chat_id=state.conversation_id,
                    agent_name=state.agent_name,
                    messages=[latest_message],
                ),
                owner_id=state.user_id,
            )
            return {"conversation_id": conversation.id, "messages": state.messages}

    async def load_chat_messages(self, state: MainState, config: RunnableConfig):
        db = state.context.db
        with Session(db) as session:
            chat_messages = get_conversation_messages(
                db=session, conversation_id=state.conversation_id
            )
            logger.info(
                "load_chat_messages 节点加载了用户聊天历史 %s", len(chat_messages)
            )
            return {
                "messages": [
                    ChatMessage(role=x.role, content=x.content) for x in chat_messages
                ]
            }

    async def chat_node(self, state: MainState, config: RunnableConfig):
        messages = state.messages
        llm = lcllm_openai_chat("")
        response = await llm.ainvoke(messages, config)
        return {
            "messages": [response],
            "wait_user": True,
        }

    # We define a fake node to ask the human
    def ask_human(self, state: MainState, config: RunnableConfig):
        logger.info("等待人工干预")

    async def call_tools():
        logger.info("TODO: call tools")
