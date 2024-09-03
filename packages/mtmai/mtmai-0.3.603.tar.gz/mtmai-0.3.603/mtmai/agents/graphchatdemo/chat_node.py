import logging

from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.state import (
    ChatBotUiState,
    MainState,
    UiChatItem,
    UiDelta,
)
from mtmai.mtlibs.aiutils import lcllm_openai_chat

from .tools import default_tools

logger = logging.getLogger()


class ChatNode:
    def __init__(self):
        # self.runnable = runnable
        pass

    async def __call__(self, state: MainState, config: RunnableConfig):
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
                    # "wait_user": True,
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
                    # "wait_user": True,
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
            llm = lcllm_openai_chat("")

            llm = llm.bind_tools([*default_tools])
            messages = list(state.get("messages"))
            if len(messages) < 1:
                raise Exception("消息长度不正确")  # noqa: EM101, TRY002
            if messages[-1].type == "tool":
                ai_message = await llm.ainvoke(messages, config)
                # if len(ai_message.tool_calls) > 0:
                return {
                    "messages": [
                        ai_message,
                    ],
                }
            new_user_message = ChatMessage(role="user", content=state.get("user_input"))
            messages.append(new_user_message)
            ai_message = await llm.ainvoke(messages, config)
            finnal_state = {
                "messages": [
                    new_user_message,
                    ai_message,
                ],
                # "wait_user": True,
                "uidelta": state.get("uidelta"),
            }
            return finnal_state
