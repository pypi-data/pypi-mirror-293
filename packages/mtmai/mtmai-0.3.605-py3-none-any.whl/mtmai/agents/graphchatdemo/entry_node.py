import logging

from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.prompts import Prompts
from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    ExampleInputItem,
    MainState,
    UIChatMessageItem,
    UiDelta,
)
from mtmai.core.config import settings

from .state import agent_name

logger = logging.getLogger()


def edge_entry(state: MainState):
    return "chat"


class EntryNode:
    def __init__(self):
        # self.runnable = runnable
        pass

    def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")
        db = state["context"].db
        state_ret = {
            "messages": [ChatMessage(role="system", content=Prompts.chatbot())],
            "uistate": ChatBotUiState(),
            "uidelta": UiDelta(
                uiState=ChatBotUiState(
                    threadId=thread_id,
                    agent=agent_name,
                    agent_url_base=settings.API_V1_STR + "/" + agent_name,
                    graph_image_url=f"{settings.API_V1_STR}/{agent_name}/graph_image",
                    example_input_items=[
                        ExampleInputItem(
                            title="例子1",
                            description="ai介绍",
                            content="请自我介绍,尽量详细.",
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
                    uichatitems=[
                        UIChatMessageItem(
                            compType="UserInput", props={"content": "fake-user-input"}
                        )
                    ],
                    # ui_messages=[UiChatItem(component="GraphFlowView", props={})],
                )
            ),
        }
        return state_ret
