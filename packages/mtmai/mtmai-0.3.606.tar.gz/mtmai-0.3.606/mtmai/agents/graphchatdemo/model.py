from datetime import datetime
from typing import TYPE_CHECKING

from langchain_core.runnables import RunnableConfig
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from mtmai.mtlibs import mtutils

if TYPE_CHECKING:
    import mtmai


class AgentTaskBase(SQLModel):
    title: str | None = Field(default="")
    description: str | None = Field(default="")
    path: str | None = Field(default="")
    share_path: str | None = Field(default="")


class AgentTask(AgentTaskBase, table=True):
    """对应 langgraph 一个工作流的运行"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    thread_id: str
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="chats")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    output: str | None = Field(default="")
    config: RunnableConfig = Field(sa_column=Column(JSON))
