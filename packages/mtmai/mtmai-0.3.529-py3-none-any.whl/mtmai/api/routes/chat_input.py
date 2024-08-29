import logging

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from sqlmodel import Session, SQLModel, func, select

from mtmai.api.deps import (
    CurrentUser,
    OptionalUserDep,
    SessionDep,
)
from mtmai.core.db import get_session, getdb
from mtmai.models.chat import ChatInput, ChatInputBase, ChatMessage

router = APIRouter()

logger = logging.getLogger()


class ConfigModel(BaseModel):
    option1: str
    option2: int


async def get_chatinput_byid(chat_id: str):
    with Session(getdb()) as session:
        statement = (
            select(ChatInput)
            .where(ChatInput.id == chat_id)
            .options(joinedload(ChatInput.messages))
        )
        result = session.exec(statement).first()
        return result


@router.get("/chat/{chat_id}/messages", response_model=list[ChatMessage])
async def chat_messages(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    user: OptionalUserDep,
    chat_id: str,
):
    if not user:
        return None
    chat_messages = db.exec(
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return chat_messages


class ChatInputReq(BaseModel):
    chat_id: str | None = None
    messages: list[ChatMessage]


@router.put("/chat_input")
async def chat_input_put(input: ChatInput):
    with Session(getdb()) as session:
        session.merge(input)
        session.commit()
    return input


@router.patch("/chat_input/{id}")
async def chat_input_patch(id: str, item: ChatInput):
    item = get_chatinput_byid(id)
    if not item:
        return "Item not found", 404
    stored_item_model = ChatInput(**item)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    # items[item_id] = jsonable_encoder(updated_item)
    with Session(getdb()) as session:
        session.merge(updated_item)
        session.commit()

    return updated_item


@router.delete("/chat_input/{id}")
async def chat_input_delete(id: str):
    with Session(getdb()) as session:
        statement = select(ChatInput).where(ChatInput.id == id)
        results = session.exec(statement)
        item = results.one()
        session.delete(item)
        session.commit()
        return item


class ConversationPublic(ChatInputBase):
    pass


class ConversationPublic(SQLModel):
    data: list[ConversationPublic]
    count: int


@router.get("", response_model=ConversationPublic)
async def conversations(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    """获取用聊天列表"""
    count_statement = (
        select(func.count())
        .select_from(ChatInput)
        .where(ChatInput.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(ChatInput)
        .where(ChatInput.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    items = session.exec(statement).all()

    return ConversationPublic(data=items, count=count)
