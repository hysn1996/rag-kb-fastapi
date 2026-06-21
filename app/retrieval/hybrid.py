"""
混合检索模块
结合 BM25（关键词）和向量（语义）两种检索方式的优点
"""

from app.retrieval.bm25 import BM25Retriever
from app.retrieval.vector import VectorRetriever


class HybridRetriever:
    """
    混合检索器
    融合 BM25 关键词检索和向量语义检索的结果
    两种方法互补：BM25 擅长精确匹配，向量检索擅长语义理解
    """

    def __init__(self):
        self.bm25 = BM25Retriever()      # BM25 检索器
        self.vector = VectorRetriever()  # 向量检索器
        self.bm25_weight = 0.5           # BM25 结果权重
        self.vector_weight = 0.5         # 向量结果权重

    def build_index(self, documents: list):
        """
        构建混合检索索引
        同时为 BM25 和向量检索构建索引

        Args:
            documents: 文档列表
        """
        self.bm25.build_index(documents)
        self.vector.build_index(documents)

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        执行混合检索

        Args:
            query: 用户查询
            top_k: 返回的最相关文档数量

        Returns:
            融合后的相关文档列表
        """
        # 分别执行两种检索
        bm25_results = self.bm25.retrieve(query, top_k)
        vector_results = self.vector.retrieve(query, top_k)

        # 融合结果：对每种检索方式的排名给予分数
        # 排名越靠前（i 越小），得分越高 (top_k - i)
        combined = {}

        # 处理 BM25 结果
        for i, doc in enumerate(bm25_results):
            combined[doc] = combined.get(doc, 0) + (self.bm25_weight * (top_k - i))

        # 处理向量检索结果
        for i, doc in enumerate(vector_results):
            combined[doc] = combined.get(doc, 0) + (self.vector_weight * (top_k - i))

        # 按综合分数排序
        sorted_docs = sorted(combined.keys(), key=lambda x: combined[x], reverse=True)

        return sorted_docs[:top_k]
