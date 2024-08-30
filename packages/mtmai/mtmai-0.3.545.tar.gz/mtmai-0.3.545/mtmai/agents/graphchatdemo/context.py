from contextlib import contextmanager

import httpx
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig
from sqlalchemy import Engine

from mtmai.core.db import getdb


class AgentContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    httpx_session: httpx.Client
    db: Engine


@contextmanager
def make_agent_context(config: RunnableConfig):
    # here you could read the config values passed invoke/stream to customize the context object

    # as an example, we create an httpx session, which could then be used in your graph's nodes
    session = httpx.Client()
    db = getdb()
    try:
        yield AgentContext(
            httpx_session=session,
            db=db,
        )
    finally:
        session.close()
