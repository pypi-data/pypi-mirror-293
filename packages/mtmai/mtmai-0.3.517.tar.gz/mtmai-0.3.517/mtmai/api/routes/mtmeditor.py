import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.agents import (
    AgentExecutor,
    create_openai_tools_agent,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.llm.llm import get_fast_llm
from mtmai.mtlibs import aisdk

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
