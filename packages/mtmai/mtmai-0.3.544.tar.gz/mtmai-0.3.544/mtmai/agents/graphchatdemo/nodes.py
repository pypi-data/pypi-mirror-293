import logging

from langchain_core.runnables import RunnableConfig

from mtmai.agents.graphchatdemo.state import MainState
from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()


class Nodes:
    def __init__(self):
        pass

    async def entry_node(self, state: MainState, config: RunnableConfig):
        messages = state["messages"]
        llm = lcllm_openai_chat("")
        response = await llm.ainvoke(messages, config)
        return {"messages": response}
