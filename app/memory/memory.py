"""
对话记忆模块
管理多轮对话的上下文历史
"""

from collections import defaultdict


class ChatMemory:
    """
    对话记忆类
    为每个会话（session）独立维护对话历史
    支持多轮对话的上下文累积
    """

    def __init__(self, max_history: int = 10):
        """
        Args:
            max_history: 每个会话保留的最大对话轮数（每轮包含用户问题和助手回答）
        """
        self.memory = defaultdict(list)  # session_id -> 对话历史列表
        self.max_history = max_history

    def get_history(self, session_id: str = None) -> list:
        """
        获取指定会话的对话历史

        Args:
            session_id: 会话ID，None 表示不使用历史

        Returns:
            对话历史列表，格式为 [{"role": "user"/"assistant", "content": "..."}]
        """
        if not session_id:
            return []
        return self.memory.get(session_id, [])

    def add_message(self, session_id: str, user_query: str, assistant_response: str):
        """
        添加一轮对话到历史记录

        Args:
            session_id: 会话ID
            user_query: 用户问题
            assistant_response: 助手回答
        """
        if not session_id:
            return

        history = self.memory[session_id]
        # 添加用户消息和助手回复
        history.append({"role": "user", "content": user_query})
        history.append({"role": "assistant", "content": assistant_response})

        # 如果历史超过限制，截断最早的对话
        # max_history * 2 因为每轮有两条消息（user + assistant）
        if len(history) > self.max_history * 2:
            self.memory[session_id] = history[-self.max_history * 2:]

    def clear_history(self, session_id: str):
        """
        清除指定会话的历史记录

        Args:
            session_id: 会话ID
        """
        if session_id in self.memory:
            del self.memory[session_id]
