from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from sqlmodel import Session

from mtmai.models.models import User
from mtmai.mtlibs import aisdk

from .nodes import Nodes
from .state import MainState

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig


class GraphChatDemoAgent:
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(MainState)

        workflow.add_node("entry", nodes.entry_node)
        # workflow.add_node("wait_next_run", nodes.wait_next_run)
        # workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        workflow.set_entry_point("entry")
        # workflow.add_conditional_edges(
        #     "check_new_emails",
        #     nodes.new_emails,
        #     {"continue": "draft_responses", "end": "wait_next_run"},
        # )
        # workflow.add_edge("draft_responses", "wait_next_run")
        # workflow.add_edge("wait_next_run", "check_new_emails")
        self.app = workflow.compile()

    @property
    def name(self):
        return "graphcrewdemo"

    async def chat(
        self,
        db: Session,
        conversation_id: str | None = None,
        user: User | None = None,
    ):
        wf = self.app
        thread_id = "2"
        input = MainState(
            messages=[HumanMessage(content="what is the weather in sf")],
            # checked_emails_ids=["emailid123", "emailid234"]
            some_value="abcdef123",
        )
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        async for event in wf.astream_events(
            input=input,
            version="v2",
            config=config,
        ):
            kind = event["event"]
            name = event["name"]
            data = event["data"]
            if kind == "on_chat_model_stream":
                # data_chunk: AIMessageChunk = event["data"]["chunk"]
                # content = data_chunk.content
                # print(content + "|")
                # if content:
                #     yield aisdk.text(content)
                print("------")
                print(event["data"]["chunk"].dict())
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="|", flush=True)
                    yield aisdk.text(content)
            print(f"astream_event: kind: {kind}, name={name},{data}")

            if (
                kind == "on_chat_model_stream"
                and event["metadata"].get("langgraph_node") == "final"
            ):
                data = event["data"]
                if data["chunk"].content:
                    # Empty content in the context of OpenAI or Anthropic usually means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    print(data["chunk"].content, end="|", flush=True)

            if kind == "on_chain_end" and name == "LangGraph":
                # 完全结束可以拿到最终数据
                # yield f"2: {json.dumps(jsonable_encoder(data))}\n"
                yield aisdk.data(jsonable_encoder(data))

        yield aisdk.finish()
