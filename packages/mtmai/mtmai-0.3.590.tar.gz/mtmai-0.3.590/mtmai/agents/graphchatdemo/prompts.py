from textwrap import dedent


class Prompts:
    def chatbot():
        return dedent("""
      你是专业的聊天机器人,能够跟前端进行很好的互动
      要求:
      - 必须使用中文
      ----------
      {idea}
    """)
