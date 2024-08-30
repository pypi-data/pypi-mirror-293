import logging
from functools import lru_cache

from fastapi import APIRouter, Header
from langgraph.graph.state import CompiledStateGraph
from sqlmodel import Session, select

from mtmai.models.chat import ChatInput
from mtmai.models.models import Agent
from mtmai.mtlibs import mtutils

router = APIRouter()

logger = logging.getLogger()
graphs: dict[str, CompiledStateGraph] = {}


async def get_agent_from_headers(chat_agent: str = Header(None)):
    return chat_agent


def ensure_thread_id(input: ChatInput):
    if not input.config:
        input.config = {}

    if not input.config.get("configurable"):
        input.config["configurable"] = {}
    if not input.config["configurable"].get("thread_id"):
        input.config["configurable"]["thread_id"] = mtutils.gen_orm_id_key()
    if not input.config["configurable"].get("chat_id"):
        input.config["configurable"]["chat_id"] = input.id
    return input


def get_agent_by_id(db: Session, agent_id: str):
    return db.exec(select(Agent).where(Agent.id == agent_id)).one()


@lru_cache
def get_agent_by_name(agent_name: str):
    if agent_name == "chatbot_agent":
        from mtmai.agents.chatbot_agent import SimpleChatAgent

        agent = SimpleChatAgent()
        return agent
    if agent_name == "joke":
        from mtmai.agents.joke_agent import JokeAgent

        agent = JokeAgent()
        return agent
    return None
