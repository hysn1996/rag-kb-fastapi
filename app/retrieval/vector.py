"""
向量检索模块
基于语义嵌入（Embedding）的相似度检索
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.embedding.embedder import Embedder


class VectorRetriever:
    """
    向量检索器
    使用文本嵌入向量进行语义级别的相似度匹配
    """

    def __init__(self):
        self.embedder = Embedder()  # 文本向量化工具
        self.embeddings = None     # 文档嵌入向量矩阵
        self.documents = []        # 原始文档列表

    def build_index(self, documents: list):
        """
        构建向量索引
        将所有文档转换为嵌入向量并存储

        Args:
            documents: 文档列表
        """
        self.documents = documents
        # 将每个文档编码为向量
        self.embeddings = np.array([self.embedder.encode(doc) for doc in documents])

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        检索与查询语义最相似的文档

        Args:
            query: 用户查询
            top_k: 返回最相似的文档数量

        Returns:
            相似文档列表，按相似度从高到低排序
        """
        if self.embeddings is None or len(self.documents) == 0:
            return []

        # 将查询转换为向量（先转为 numpy array 再 reshape）
        query_embedding = np.array(self.embedder.encode(query)).reshape(1, -1)

        # 计算查询向量与所有文档向量的余弦相似度
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]

        # 获取相似度最高的 top_k 个文档索引
        top_n = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]

        return [self.documents[i] for i in top_n]
