import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.agents import (
    AgentExecutor,
    create_openai_tools_agent,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph
from mtmlib import mtutils
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.agents.mtmeditor.state import MainState
from mtmai.core.config import settings

from .nodes import Nodes, should_continue

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig


from mtmai.llm.llm import get_fast_llm
from mtmai.mtlibs import aisdk

logger = logging.getLogger()

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()


class MtmEditorReq(BaseModel):
    option: str
    prompt: str
    command: str | None = None


async def exec_mtmeditor_agent(req: MtmEditorReq):
    if req.option == "continue":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI writing assistant that continues existing text based on context from prior text."
                    + "Give more weight/priority to the later characters than the beginning ones. "
                    + "Limit your response to no more than 200 characters, but make sure to construct complete sentences."
                    + "Use Markdown formatting when appropriate."
                    + "必须跟随用户提交文字的语言.不要任何解释,仅给出结果.",
                ),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{prompt}"),
                # MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    elif req.option == "improve":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI writing assistant that improves existing text. "
                    + "Limit your response to no more than 200 characters, but make sure to construct complete sentences."
                    + "Use Markdown formatting when appropriate."
                    + "必须跟随用户提交文字的语言.不要任何解释,仅给出结果.",
                ),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "The existing text is: {prompt}"),
                # MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    elif req.option == "shorter":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI writing assistant that shortens existing text. "
                    + "Use Markdown formatting when appropriate.",
                    +"必须跟随用户提交文字的语言.不要任何解释,仅给出结果.",
                ),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "The existing text is: {prompt}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    elif req.option == "longer":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI writing assistant that lengthens existing text. "
                    + "Use Markdown formatting when appropriate.",
                    +"必须跟随用户提交文字的语言.不要任何解释,仅给出结果.",
                ),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "The existing text is: {prompt}"),
                # MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    if req.option == "fix":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    # "You are an AI writing assistant that fixes grammar and spelling errors in existing text. "
                    "你是专业的中文文章编辑员，辅助用户在所见即所得编辑器完成用户的语法修正和文字润色.回复必须是中文。 "
                    + "返回的文字限制最大值是1000字符。"
                    + "编辑器的UI是 markdown 界面，你可以根据实际需要使用markdown语法。"
                    + "必须跟随用户提交文字的语言.不要任何解释和啰嗦,仅给出修正好的结果.",
                ),
                ("human", "{prompt}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    elif req.option == "zap":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You area an AI writing assistant that generates text based on a prompt. "
                    + "You take an input from the user and a command for manipulating the text"
                    + "Use Markdown formatting when appropriate.",
                    +"必须跟随用户提交文字的语言.不要任何解释,仅给出结果.",
                ),
                # MessagesPlaceholder("chat_history", optional=True),
                (
                    "human",
                    "For this text: {prompt}. You have to respect the command: ${command}",
                ),
                # MessagesPlaceholder("agent_scratchpad"),
            ]
        )
    else:
        msg = f"mtmeditor 未知的动作命令 {req.option }"
        raise Exception(msg)  # noqa: TRY002
    llm = get_fast_llm()
    tools = []
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async for event in agent_executor.astream_events(
        req.model_dump(),
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":  # noqa: SIM102
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="|")
                yield aisdk.text(content)
        elif kind == "on_tool_start":
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        # elif kind == "on_tool_end":
        #     print(f"Done tool: {event['name']}")
        #     print(f"Tool output was: {event['data'].get('output')}")
        #     print("--")
    yield aisdk.finish()


@router.post("")
async def input(req: MtmEditorReq):
    return StreamingResponse(
        exec_mtmeditor_agent(req),
        media_type="text/event-stream",
    )


class MtmEditorAgent:
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

            thread: RunnableConfig = {"configurable": {"thread_id": thread_id}}

            # state1 = await app.aget_state(thread)
            inputs = None
            if is_new_thread:
                # 全新状态的情况
                logger.info("新对话 %s", thread_id)
                inputs = {
                    "user_id": user_id,
                    "user_input": prompt,
                    "user_option": option,
                }
            else:
                await app.aupdate_state(
                    thread,
                    {"user_input": prompt, "user_option": option},
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
