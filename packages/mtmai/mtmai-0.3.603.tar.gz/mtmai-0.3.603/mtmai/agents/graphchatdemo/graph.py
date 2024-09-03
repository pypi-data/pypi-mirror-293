import logging
from typing import TYPE_CHECKING

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from mtmai.agents.graphchatdemo.chat_node import ChatNode
from mtmai.agents.graphchatdemo.entry_node import EntryNode
from mtmai.agents.graphchatdemo.nodes import Nodes
from mtmai.agents.graphchatdemo.sub_image.graph_image import SubGraphText2Image
from mtmai.core.config import settings
from mtmai.mtlibs import aisdk, mtutils

from .state import DemoAgentConfig, MainState
from .tools import default_tools

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

logger = logging.getLogger()


def should_go_mtmeditor(state: MainState):
    # messages = state["messages"]
    # last_message = messages[-1]

    if state.get("go_mtmeditor"):
        return "mtmaieditor"
    return "end"


def edge_chat_node(state: MainState):
    is_tools = tools_condition(state)
    if is_tools == "tools":
        return "tools"
    # if state.get("uidelta"):
    #     return "uidelta"
    if state.get("go_mtmeditor"):
        return "mtmeditor"
    else:
        return "uidelta"


def edge_mtmeditor(state: MainState):
    return "uidelta"


def edge_entry(state: MainState):
    return "chat"


class GraphChatDemoAgent:
    def __init__(self):
        pass

    @property
    def name(self):
        return "graphchatdemo"

    def build_flow(self):
        nodes = Nodes()

        # sub mtmeditor
        # sub_mtmeditor = SubMtmEditorAgent()
        # sub_graph = sub_mtmeditor.build_flow()

        sub_text2image_graph = SubGraphText2Image().build_flow()

        tool_node = ToolNode(tools=default_tools)
        wf = StateGraph(MainState)
        wf.add_node("entry", EntryNode())
        wf.add_node("chat", ChatNode())
        wf.add_node("tools", tool_node)
        wf.add_node("uidelta_node", nodes.uidelta_node)
        wf.add_node("finnal_node", nodes.finnal_node)

        wf.set_entry_point("entry")
        wf.add_conditional_edges(
            "entry",
            edge_entry,
            {
                "chat": "chat",
                # "uidelta": "uidelta_node",
                "end": END,
            },
        )

        # wf.add_edge("chat", "uidelta_node")
        wf.add_edge("uidelta_node", "chat")
        wf.add_edge("tools", "chat")
        wf.add_conditional_edges(
            "chat",
            edge_chat_node,
            {
                "tools": "tools",
                "mtmeditor": "mtmeditor",
                "uidelta": "uidelta_node",
                "end": END,
            },
        )

        # wf.add_node("mtmeditor", sub_graph.compile())
        wf.add_node("mtmeditor", nodes.mtmeditor_node)
        wf.add_conditional_edges(
            "mtmeditor",
            edge_mtmeditor,
            {
                "uidelta": "uidelta_node",
                "finnal": "finnal_node",
            },
        )

        # wf.add_node("sub_text2image", sub_text2image_graph.compile())
        # wf.add_edge("chat", "sub_text2image")
        # wf.add_conditional_edges(
        #     "chat",
        #     tools_condition,
        # )

        return wf

    async def chat(
        self,
        user_id: str,
        prompt: str | None = None,
        thread_id: str | None = None,
        option=None,
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

            thread: RunnableConfig = {
                "configurable": {"thread_id": thread_id, user_id: user_id}
            }

            # state1 = await app.aget_state(thread)
            inputs = None
            if is_new_thread:
                # 全新状态的情况
                logger.info("新对话 %s", thread_id)
                inputs = {
                    "user_id": user_id,
                    "user_input": prompt,
                    "user_option": option,
                    "config": DemoAgentConfig(
                        name=self.name,
                    ),
                }
            else:
                await app.aupdate_state(
                    thread,
                    {
                        "user_input": prompt,
                        "user_option": option,
                        "uidelta": None,
                    },
                    as_node="uidelta_node",
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
                logger.info("%s:node: %s", kind, node_name)
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
                    if data and (node_name == "uidelta_node" or node_name == "tools"):
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
                    final_messages = event["data"]["output"]["messages"]
                    for message in final_messages:
                        message.pretty_print()
                    logger.info("中止节点")

            yield aisdk.finish()
