import logging
from typing import Literal

from langchain_core.messages import ChatMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig

from mtmai.agents.mtmeditor.prompts import Prompts
from mtmai.agents.mtmeditor.state import ChatBotUiState, MainState, UiChatItem, UiDelta
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()


def should_continue(state: MainState) -> Literal["__end__", "tools", "continue"]:
    if state["wait_user"]:
        return "ask_human"

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
                # ChatMessage(role="system", content=Prompts.chatbot()),
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

        return state_ret

    async def chat_node(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state["user_input"]
        user_option = state.get("user_option")

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

        messages = state["messages"]

        msgs2 = list(messages)
        new_user_message = ChatMessage(role="user", content=state["user_input"])
        msgs2.append(new_user_message)
        tools = []
        llm = lcllm_openai_chat("")

        if user_option == "longer":
            prompt = Prompts.editor_longer(state)
        elif user_option == "ontab":
            # tab 建操作
            prompt = Prompts.editor_ontab(state)
        else:
            prompt = Prompts.editor_improve(state)

        ai_message = await llm.ainvoke(prompt, config)
        state["uidelta"].update({"isOpenAgentRagView": True})
        return {
            "messages": [
                new_user_message,
                ai_message,
            ],
            "wait_user": True,
            "uidelta": state["uidelta"],
        }

    def uidelta_node(self, state: MainState, config: RunnableConfig):
        # logger.info("uidelta_node, %s", state["uidelta"])
        return {"uidelta": state["uidelta"]}

    async def action_node(self, state: MainState, config: RunnableConfig):
        logger.info("action_node, %s", state["uidelta"])
        return {}

    async def tool_call_node(self, state: MainState, config: RunnableConfig):
        logger.info("tool_call_node, %s", state)
