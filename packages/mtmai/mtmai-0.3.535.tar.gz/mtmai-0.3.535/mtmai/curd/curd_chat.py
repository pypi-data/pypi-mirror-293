import logging

# from mtmai_client.models.chat_input import ChatInput
from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.models.chat import ChatInput, ChatMessage, ChatMessageBase
from mtmai.models.models import (
    Account,
)

logger = logging.getLogger()


class ChatSubmitPublic(BaseModel):
    chat_id: str | None = None
    agent_name: str
    messages: list[ChatMessageBase]


def submit_chat_messages(
    *, db: Session, data: ChatSubmitPublic, owner_id: str
) -> Account:
    """
    存储前端聊天时用户提交的一轮消息
    1: 首次提交建自动创建 ChatInput (表示完整的消息历史),并加附加的首个消息保存。
    2: ChatInput,跟 ChatMessage 是1对多的关系

    """
    chat_input_item = ChatInput()
    chat_input_item.agent_id = data.agent_name
    chat_input_item.user_id = owner_id
    if not data.chat_id:
        # 是全新的对话
        db.add(chat_input_item)
        db.commit()
        db.refresh(chat_input_item)
        logger.info("创建了 chat input %s", chat_input_item.id)
    else:
        # 现有对话
        chat_input_item = get_chat_input(db, data.chat_id)
        if not chat_input_item:
            msg = "获取 chat input 记录出错"
            raise Exception(msg)  # noqa: TRY002

    # 添加 message
    lastest_message = data.messages[-1]
    new_message = ChatMessage(
        content=lastest_message.content,
        chat=chat_input_item,
        role=lastest_message.role,
    )
    chat_input_item.messages.append(new_message)

    # db.add(chat_input_item)
    # db.commit()
    # db.refresh(chat_input_item)

    new_message = ChatMessage(
        content=lastest_message.content,
        chat_id=data.chat_id,
        role=lastest_message.role,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    logger.info("创建新的对话记录 %s", chat_input_item.id)
    return chat_input_item


def append_chat_message(db: Session, chat_message: ChatMessage):
    """追加一个聊天历史,(未完成)"""
    db.merge(chat_message)
    db.commit()
    return chat_message


def get_chat_input(db: Session, id: str):
    statement = select(ChatInput).where(ChatInput.id == id)
    result = db.exec(statement=statement).first()
    return result
