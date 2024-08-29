"""
doc: https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol
"""

import json


def text(word: str):
    return f"0:{json.dumps(word)}\n"


def data(items: list[any]):
    return f"2:{json.dumps(items)}\n"


def error(error_message: str):
    return f"3:{json.dumps(error_message)}\n"


def finish(reason: str = "stop", prompt_tokens: int = 0, completion_tokens: int = 0):
    return f"d:{json.dumps({
        "finishReason":  reason,
        "usage":{
            "promptTokens":prompt_tokens,
        "completionTokens":completion_tokens}
    })}\n"
