import logging
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from mtmai.mtlibs import aisdk, mtutils
from mtmai.mtlibs.langgraph import get_langgraph_checkpointer

from .nodes import Nodes, should_continue
from .state import MainState

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

logger = logging.getLogger()


class GraphChatDemoAgent:
    def __init__(self):
        nodes = Nodes()
        wf = StateGraph(MainState)

        wf.add_node("entry", nodes.entry)
        wf.add_node("load_chat_messages", nodes.load_chat_messages)
        wf.add_node("chat", nodes.chat_node)
        wf.add_node("ask_human", nodes.ask_human)
        # wf.add_node("tool", nodes.call_tools)

        # workflow.add_node("wait_next_run", nodes.wait_next_run)
        # workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        wf.set_entry_point("entry")
        wf.add_edge("entry", "load_chat_messages")
        wf.add_edge("load_chat_messages", "chat")
        # wf.add_conditional_edges(
        #     "chat",
        #     nodes.call_tools,
        #     {"continue": "draft_responses", "end": "wait_next_run"},
        # )

        wf.add_conditional_edges(
            "chat",
            should_continue,
            {
                # "continue": "chat",
                "ask_human": "ask_human",
                "end": END,
            },
        )
        wf.add_edge("ask_human", "chat")

        # workflow.add_edge("draft_responses", "wait_next_run")
        # workflow.add_edge("wait_next_run", "check_new_emails")
        self.app = wf.compile(
            checkpointer=get_langgraph_checkpointer(), interrupt_before=["ask_human"]
        )

        wf_image(self.app)

    @property
    def name(self):
        return "graphcrewdemo"

    async def chat(
        self,
        user_id: str,
        user_input: str | None = None,
        thread_id: str | None = None,
    ):
        wf = self.app

        is_new_thread = not thread_id
        if not thread_id:
            thread_id = mtutils.gen_orm_id_key()
            logger.info("创建了 thread_id %s", thread_id)

        inputs = None
        if is_new_thread:
            inputs = {
                "user_id": user_id,
                "user_input": user_input,
                "agent_name": "graphchatdemo",
            }

        logger.info("graph chat %s, input: %s", thread_id, inputs)
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        async for event in wf.astream_events(
            inputs,
            version="v2",
            config=config,
        ):
            kind = event["event"]
            name = event["name"]
            data = event["data"]
            if kind == "on_chat_model_stream":
                # print(event["data"]["chunk"].dict())
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="", flush=True)
                    yield aisdk.text(content)

                if event["metadata"].get("langgraph_node") == "final":
                    # 最终节点
                    logger.info("到达终结节点")
            # print(f"astream_event: kind: {kind}, name={name},{data}")

            if kind == "on_chain_end" and name == "LangGraph":
                # finnal
                yield aisdk.data(jsonable_encoder(data))
                logger.info("流程终结")

        data = {}
        data["thread_id"] = thread_id
        yield aisdk.data(
            [
                {
                    "dataType": "uistate",
                    "data": data,
                }
            ]
        )
        yield aisdk.finish()


def wf_image(wf: CompiledStateGraph):
    # wf = get_workflow()
    image_data = wf.get_graph(xray=1).draw_mermaid_png()
    Path(".vol/graphchatdemo.jpg").write_bytes(image_data)
