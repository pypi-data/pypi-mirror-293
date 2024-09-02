import logging
from typing import Literal

from langchain_core.messages import ChatMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig
from sqlmodel import Session

from mtmai.agents.graphchatdemo.prompts import Prompts
from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
    UiChatItem,
    UiDelta,
)
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()


def should_continue(state: MainState) -> Literal["__end__", "tools", "continue"]:
    # messages = state["messages"]
    # last_message = messages[-1]

    if state["wait_user"]:
        return "ask_human"
    # if state.wait_user:
    #     return "chat"

    # if last_message.tool_calls:
    #     return "tools"
    # if not last_message.tool_calls:
    #     return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


class AskHuman(BaseModel):
    """Ask the human a question"""

    question: str


class Nodes:
    def __init__(self):
        pass

    async def entry(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        db = state["context"].db
        if not state["user_input"] and not state["messages"]:
            return {"error": "require user input"}

        if len(state["messages"]) == 0:
            state["messages"] = [
                ChatMessage(role="system", content=Prompts.chatbot()),
                # ChatMessage(role="user", content=state["user_input"]),
            ]

        state_ret = {
            "uidelta": UiDelta(
                uiState=ChatBotUiState(
                    threadId=thread_id,
                    # ui_messages=[UiChatItem(component="GraphFlowView", props={})],
                )
            )
        }
        # (过时) 如果没有 conversation_id, 表示新的聊天
        with Session(db) as session:
            latest_message = state["user_input"][-1]
            # conversation = submit_chat_messages(
            #     db=session,
            #     data=ChatSubmitPublic(
            #         chat_id=thread_id,
            #         agent_name=state["config"]["name"],
            #         messages=[latest_message],
            #     ),
            #     owner_id=state["user_id"],
            # )
            # state_ret["conversation_id"] = conversation.id
            state_ret["messages"] = state["messages"]
        return state_ret

    # async def load_chat_messages(self, state: MainState, config: RunnableConfig):
    #     thread_id = config.get("configurable").get("thread_id")
    #     db = state["context"].db
    #     # with Session(db) as session:
    #     #     chat_messages = get_conversation_messages(
    #     #         db=session, conversation_id=thread_id
    #     #     )
    #     #     logger.info(
    #     #         "load_chat_messages 节点加载了用户聊天历史 %s", len(chat_messages)
    #     #     )
    #     #     return {
    #     #         "messages": [
    #     #             ChatMessage(role=x.role, content=x.content) for x in chat_messages
    #     #         ]
    #     #     }

    async def chat_node(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state["user_input"]
        if user_input == "/1":
            # 命令测试
            return {
                "wait_user": True,
                "uidelta": UiDelta(
                    uiState=ChatBotUiState(
                        # threadId=thread_id,
                        ui_messages=[UiChatItem(component="GraphFlowView", props={})],
                    )
                ),
            }
        if user_input == "/dev_search":
            # 命令测试
            return {
                "wait_user": True,
                "uidelta": UiDelta(
                    uiState=ChatBotUiState(
                        # threadId=thread_id,
                        isOpenSearchView=True
                        # ui_messages=[UiChatItem(component="GraphFlowView", props={})],
                    )
                ),
            }
        # if user_input == "/rag":
        #     # 命令测试
        #     yield aisdk.data(
        #         [
        #             {
        #                 "dataType": "uistate",
        #                 "data": {
        #                     "component": "AgentRagView",
        #                     "props": {
        #                         "text": "text123",
        #                     },
        #                 },
        #             }
        #         ]
        #     )
        #     return

        messages = state["messages"]

        msgs2 = list(messages)
        new_user_message = ChatMessage(role="user", content=state["user_input"])
        msgs2.append(new_user_message)
        # tools = [search]
        tools = []
        llm = lcllm_openai_chat("")

        # llm = llm.bind_tools([*tools, AskHuman])

        ai_message = await llm.ainvoke(msgs2, config)
        # msgs2.append(response)
        state["uidelta"].update({"isOpenAgentRagView": True})
        return {
            "messages": [
                new_user_message,
                ai_message,
            ],
            # "messages":msgs2,
            "wait_user": True,
            "uidelta": state["uidelta"],
        }

    def uidelta_node(self, state: MainState, config: RunnableConfig):
        # logger.info("uidelta_node, %s", state["uidelta"])
        return {"uidelta": state["uidelta"]}

    # We define a fake node to ask the human
    # def ask_human(self, state: MainState, config: RunnableConfig):
    #     # logger.info("等待人工干预")
    #     return ({"uistateV2": {"isOpenAgentRagView222": True}},)

    async def tool_call_node(self, state: MainState, config: RunnableConfig):
        logger.info("tool_call_node, %s", state)
