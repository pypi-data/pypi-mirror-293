import logging
from collections.abc import Iterable

from fastapi import APIRouter
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from mtmai.mtlibs.aiutils import lcllm_openai_chat

logger = logging.getLogger()

router = APIRouter()


async def chatbot_agent(
    messages: Iterable[ChatCompletionMessageParam], chat_id: str | None = None
):
    # tools = [get_flows]
    tools = []
    llm = lcllm_openai_chat("")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            MessagesPlaceholder("chat_history", optional=True),
            # ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_openai_tools_agent(
        llm.with_config({"tags": ["agent_llm"]}), tools, prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools).with_config(
        {"run_name": "Agent"}
    )

    return agent_executor


# class ChatMessageSubmitReq(BaseModel):
#     pass
# @router.post("/chat")
# async def chat(messages: list[ChatMessage]):
#     logger.info("JokeAgent handle Message %s", messages)

#     latest_message = messages[-1]
#     wf = get_workflow()

#     state = JokeAgentState(
#         messages=[{"role": "user", "content": latest_message.content}]
#     )

#     thread_id = mtutils.gen_orm_id_key()

#     response = response = StreamingResponse(
#         flow_events(wf=wf, state=state, thread_id=thread_id)
#     )
#     response.headers["x-vercel-ai-data-stream"] = "v1"
#     return response
