import logging

from langchain_core.messages import ChatMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.prompts import Prompts
from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    ExampleInputItem,
    MainState,
    UiChatItem,
    UiDelta,
)
from mtmai.core.config import settings
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()


class AskHuman(BaseModel):
    """Ask the human a question"""

    question: str


def edge_entry_chat(state: MainState):
    user_input = state.get("user_input")
    if len(user_input) > 0:
        return "chat"
    return "uidelta"


agent_name = "mtmaibot"


class Nodes:
    def __init__(self):
        pass

    async def entry(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        db = state["context"].db

        if len(state["messages"]) == 0:
            state["messages"] = [
                ChatMessage(role="system", content=Prompts.chatbot()),
            ]

        state_ret = {
            "uidelta": UiDelta(
                uiState=ChatBotUiState(
                    threadId=thread_id,
                    agent=agent_name,
                    agent_url_base=settings.API_V1_STR + "/" + agent_name,
                    graph_image_url=f"{settings.API_V1_STR}/{agent_name}/graph_image",
                    example_input_items=[
                        ExampleInputItem(
                            title="例子1", description="例子1描述", content="hello"
                        ),
                        ExampleInputItem(
                            title="例子2", description="例子2描述", content="hello"
                        ),
                        ExampleInputItem(
                            title="例子3", description="例子3描述", content="hello"
                        ),
                        ExampleInputItem(
                            title="例子4", description="例子4描述", content="hello"
                        ),
                    ],
                    # ui_messages=[UiChatItem(component="GraphFlowView", props={})],
                )
            )
        }
        return state_ret

    async def chat_node(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state.get("user_input")
        user_option = state.get("user_option")
        if user_option:
            # 是可视化编辑器的指令
            return {"go_mtmeditor": True}
        else:
            if user_input == "":
                logger.info("前端页面刷新后重新获取状态")

            elif user_input == "/1":
                # 命令测试
                return {
                    "wait_user": True,
                    "uidelta": UiDelta(
                        uiState=ChatBotUiState(
                            ui_messages=[
                                UiChatItem(component="GraphFlowView", props={})
                            ],
                        )
                    ),
                }
            elif user_input == "/mtmeditor":
                logger.info("打开所见即所得编辑器")
                return {
                    "wait_user": True,
                    "uidelta": UiDelta(uiState=ChatBotUiState(isOpenMtmEditor=True)),
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
            messages = list(state.get("messages"))

            new_user_message = ChatMessage(role="user", content=state.get("user_input"))
            messages.append(new_user_message)
            # tools = [search]
            tools = []
            llm = lcllm_openai_chat("")

            # llm = llm.bind_tools([*tools, AskHuman])

            ai_message = await llm.ainvoke(messages, config)
            # state["uidelta"].update({"isOpenAgentRagView": True})
            return {
                "messages": [
                    new_user_message,
                    ai_message,
                ],
                # "messages":msgs2,
                "wait_user": True,
                "uidelta": state.get("uidelta"),
            }

    def uidelta_node(self, state: MainState, config: RunnableConfig):
        uidelta_update = state.get("uidelta")
        return {"uidelta": uidelta_update}

    async def tool_call_node(self, state: MainState, config: RunnableConfig):
        logger.info("tool_call_node, %s", state)

    async def mtmeditor_node(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state.get("user_input")
        user_option = state.get("user_option")
        messages = list(state.get("messages"))

        new_user_message = ChatMessage(role="user", content=user_input)
        messages.append(new_user_message)
        llm = lcllm_openai_chat("")

        if user_option == "longer":
            prompt = Prompts.editor_longer(state)
        elif user_option == "ontab":
            # tab 建操作
            prompt = Prompts.editor_ontab(state)
        elif user_option == "conver_image":
            # 封面图片生成
            pass
        else:
            prompt = Prompts.editor_improve(state)

        ai_message = await llm.ainvoke(prompt, config)
        # state["uidelta"].update({"isOpenAgentRagView": True})
        return {
            "messages": [
                new_user_message,
                ai_message,
            ],
            "wait_user": True,
            # "uidelta": state.get("uidelta"),
        }
