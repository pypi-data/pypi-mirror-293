from pydantic import BaseModel


class AgentChatConfig(BaseModel):
    chat_endpoint: str | None = None


class AgentMeta(BaseModel):
    id: str
    name: str
    chat_url: str | None = None
    can_chat: bool = (False,)
    agent_type: str | None = None
    graph_image: str | None = None
    label: str | None = None
    description: str | None = None
    chat_agent_config: AgentChatConfig | None = None
