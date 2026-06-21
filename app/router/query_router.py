# app/router/query_router.py
# 查询路由模块 - 根据用户问题类型分发到不同处理流程

from typing import Dict


class QueryRouter:
    """
    查询路由器
    将用户问题分类为：rag / chat 两种类型
    """

    def __init__(self):
        # RAG关键词（企业知识库触发）
        self.rag_keywords = [
            "报销"
        ]

    def classify(self, query: str) -> Dict:
        """
        分类用户查询（基于关键词匹配）

        Args:
            query: 用户输入的问题

        Returns:
            分类结果字典，包含 type、reason 等信息
        """
        query = query.strip()
        return self._classify_by_keywords(query)

    def _classify_by_keywords(self, query: str) -> Dict:
        """
        基于关键词的路由分类
        """
        rag_score = self._score_rag(query)

        # ===== 1. RAG判断 =====
        if rag_score > 0:
            return {
                "type": "rag",
                "use_rag": True,
                "reason": "rag keyword match"
            }

        # ===== 2. 默认闲聊 =====
        return {
            "type": "chat",
            "use_rag": False,
            "reason": "general chat"
        }

    def _score_rag(self, query: str) -> int:
        """
        RAG评分：匹配关键词数量
        """
        score = 0
        query_lower = query.lower()
        for kw in self.rag_keywords:
            if kw in query_lower:
                score += 1
        return score