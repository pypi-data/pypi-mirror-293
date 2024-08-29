from datetime import datetime

from langchain_core.runnables.config import RunnableConfig
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

# from mtmai.models  chat
import mtmai
from mtmai.mtlibs import mtutils


class ChatInputBase(SQLModel):
    title: str | None = Field(default="")
    description: str | None = Field(default="")
    path: str | None = Field(default="")
    share_path: str | None = Field(default="")


class ChatInput(ChatInputBase, table=True):
    """完整对话记录,(TODO:数据结构有待完善)"""

    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    agent_id: str
    user_id: str = Field(default=None, foreign_key="user.id")
    user: "mtmai.models.models.User" = Relationship(back_populates="chats")

    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    output: str | None = Field(default="")
    config: RunnableConfig = Field(sa_column=Column(JSON))

    # status: str = Field(default=StatusEnum.NEW.value, nullable=False)
    # messages: ChatMessage = Field(sa_column=Column(JSON))

    messages: list["ChatMessage"] = Relationship(back_populates="chat")


class ChatMessageBase(SQLModel):
    content: str | None = None
    role: str | None = Field(default="user")


class ChatMessage(ChatMessageBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    chat_id: str | None = Field(default=None, foreign_key="chatinput.id")
    chat: "ChatInput" = Relationship(back_populates="messages")
