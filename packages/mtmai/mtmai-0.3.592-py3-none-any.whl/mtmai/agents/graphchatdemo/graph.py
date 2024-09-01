import logging
from typing import TYPE_CHECKING

from langgraph.graph import END, StateGraph

from mtmai.core.config import settings
from mtmai.mtlibs import aisdk, mtutils

from .nodes import Nodes, should_continue
from .state import DemoAgentConfig, MainState

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

logger = logging.getLogger()


class GraphChatDemoAgent:
    def __init__(self):
        pass

    @property
    def name(self):
        return "graphchatdemo"

    def build_flow(self):
        nodes = Nodes()

        wf = StateGraph(MainState)
        wf.add_node("entry", nodes.entry)
        wf.add_node("chat", nodes.chat_node)
        wf.add_node("tool_call", nodes.tool_call_node)
        wf.add_node("uidelta_node", nodes.uidelta_node)
        wf.set_entry_point("entry")
        wf.add_edge("entry", "chat")
        wf.add_edge("chat", "uidelta_node")
        wf.add_edge("uidelta_node", "chat")
        wf.add_conditional_edges(
            "chat",
            should_continue,
            {
                "tool_call": "tool_call",
                "ask_human": "uidelta_node",
                "end": END,
            },
        )
        return wf

    async def chat(
        self,
        user_id: str,
        user_input: str | None = None,
        thread_id: str | None = None,
    ):
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

        async with AsyncPostgresSaver.from_conn_string(
            settings.DATABASE_URL
        ) as checkpointer:
            app = self.build_flow().compile(
                checkpointer=checkpointer,
                # interrupt_before=["uidelta_node"]
                interrupt_after=["uidelta_node"],
            )

            is_new_thread = not thread_id
            if not thread_id:
                thread_id = mtutils.gen_orm_id_key()

            thread: RunnableConfig = {"configurable": {"thread_id": thread_id}}

            # state1 = await app.aget_state(thread)
            inputs = None
            if is_new_thread:
                # 全新状态的情况
                logger.info("新对话 %s", thread_id)
                inputs = {
                    "user_id": user_id,
                    "user_input": user_input,
                    "config": DemoAgentConfig(
                        name=self.name,
                    ),
                }
            else:
                await app.aupdate_state(
                    thread, {"user_input": user_input}, as_node="uidelta_node"
                )
            async for event in app.astream_events(
                inputs,
                version="v2",
                config=thread,
            ):
                kind = event["event"]
                node_name = event["name"]
                data = event["data"]
                # tags = event.get("tags", [])
                if kind == "on_chat_model_stream":
                    # print(event["data"]["chunk"].dict())
                    content = data["chunk"].content
                    if content:
                        print(content, end="", flush=True)
                        yield aisdk.text(content)

                    if event["metadata"].get("langgraph_node") == "final":
                        # 最终节点
                        logger.info("到达终结节点")
                # print(f"astream_event: kind: {kind}, name={name},{data}")

                if kind == "on_chain_stream":
                    if data and node_name == "uidelta_node":
                        chunk_data = data.get("chunk", {})
                        picked_data = {
                            key: chunk_data[key]
                            for key in ["uidelta"]
                            if key in chunk_data
                        }

                        if picked_data:
                            yield aisdk.data(picked_data)
                if kind == "on_chain_end" and node_name == "LangGraph":
                    # yield aisdk.data(jsonable_encoder(data))
                    logger.info("流程中断")

            yield aisdk.finish()
