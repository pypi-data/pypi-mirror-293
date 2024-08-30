from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class MainState(TypedDict):
    # checked_emails_ids: list[str]
    # emails: list[dict] | None
    # action_required_emails: dict
    some_value: str | None = None
    messages: Annotated[list, add_messages]
