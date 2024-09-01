# from langchain.tools import tool
from langchain_core.tools import tool


@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder for the actual implementation
    # Don't let the LLM know this though 😊
    return [
        f"I looked up: {query}. Result: It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
    ]


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
