import logging

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


# @lru_cache
# def get_agent_by_name(agent_name: str):
#     if agent_name == "simplechat":
#         from mtmai.agents.chatbot_agent import SimpleChatAgent

#         agent = SimpleChatAgent()
#         return agent
#     if agent_name == "joke":
#         from mtmai.agents.joke_agent import JokeAgent

#         agent = JokeAgent()
#         return agent
#     if agent_name == "grephdemo":
#         from mtmai.agents.graph_demo import GrapphAgent

#         return GrapphAgent
#     return None

agent_list = []


def register_agent(agent_obj):
    agent_list.append(agent_obj)


def init_agent_list():
    from mtmai.agents.simple_chat import SimpleChatAgent

    register_agent(SimpleChatAgent)


init_agent_list()


def get_agent_by_name_v2(agent_name: str):
    if agent_name == "simplechat":
        from mtmai.agents.simple_chat import SimpleChatAgent

        return SimpleChatAgent
    if agent_name == "joke":
        from mtmai.agents.joke_agent import JokeAgent

        return JokeAgent

    if agent_name == "grephdemo":
        from mtmai.agents.langgraph_crew.graph import WorkFlowCrewAgent

        return WorkFlowCrewAgent

    if agent_name == "graphchatdemo":
        from mtmai.agents.graphchatdemo.graph import GraphChatDemoAgent

        return GraphChatDemoAgent
    return None


agents = {}


def get_agent_by_name_v3(agent_name: str):
    global agents
    a = agents.get(agent_name)
    if not a:
        b = get_agent_by_name_v2(agent_name)
        agent_inst = b()
        agents[agent_name] = agent_inst
    return agents.get(agent_name)
