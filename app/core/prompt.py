"""
Prompt 模板模块
构建用于 RAG 的提示词模板
"""


class PromptTemplate:
    """
    Prompt 模板类
    提供构建 RAG 对话提示词的方法
    """

    @staticmethod
    def build_rag_prompt(query: str, context: str, history: list = None) -> list:
        """
        构建带有检索上下文的对话消息列表

        Args:
            query: 用户当前问题
            context: 从知识库检索到的相关文档（作为上下文）
            history: 之前的对话历史（用于多轮对话）

        Returns:
            格式化的消息列表，可直接传给 LLM
        """
        # 系统提示词：定义 AI 助手的角色和行为规则
        # 注意：千问 API 不支持 system role，需要合并到 user 消息中
        system_prompt = """你是一个专业的知识库问答助手。请根据提供的上下文信息回答用户的问题。
如果上下文信息不足以回答问题，请明确说明。不要编造信息。

上下文信息：
{context}

请回答用户的问题。"""

        messages = []

        # 如果有历史对话，追加到消息列表中
        if history:
            messages.extend(history)

        # 构建用户消息：将系统提示词和用户问题合并
        if context:
            user_content = system_prompt.format(context=context) + "\n\n用户问题：" + query
        else:
            # 无上下文时，只使用简单的提示
            user_content = f"请回答以下问题：\n{query}"

        messages.append({"role": "user", "content": user_content})

        return messages
