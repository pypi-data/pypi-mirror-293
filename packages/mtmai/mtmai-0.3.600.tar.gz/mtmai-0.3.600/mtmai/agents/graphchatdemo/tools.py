import logging

from langchain_core.tools import tool

logger = logging.getLogger()


@tool
def search(query: str):
    """Useful to search content from web."""
    logger.info("调用 search 工具 %s", query)
    return [
        f"I looked up: {query}. Result: It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
    ]


default_tools = [search]
# class WebSearchTool:
#     @tool("Web Search")
#     def web_search(data):
#         """
#         Useful to search content from web.
#         """
#         # email, subject, message = data.split("|")
#         # gmail = GmailToolkit()
#         # draft = GmailCreateDraft(api_resource=gmail.api_resource)
#         # resutl = draft({
#         # 		'to': [email],
#         # 		'subject': subject,
#         # 		'message': message
#         # })
#         resutl = {
#             "to": "fake@email.com",
#             "subject": "fakesubject",
#             "message": "fake_message",
#         }
#         return f"\nSearch content results: {resutl}\n"
