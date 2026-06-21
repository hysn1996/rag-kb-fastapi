"""
BM25 检索模块
基于传统关键词匹配的概率检索算法
"""

import jieba
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    BM25 检索器
    使用 BM25 算法进行关键词级别的文档检索
    BM25 是一种改进的 TF-IDF 算法，考虑了文档长度归一化
    """

    def __init__(self):
        self.corpus = []  # 文档集合
        self.bm25 = None  # BM25 模型实例

    def build_index(self, documents: list):
        """
        构建 BM25 索引

        Args:
            documents: 文档列表，每个文档为字符串
        """
        self.corpus = documents
        # 使用 jieba 对每篇文档进行中文分词
        tokenized_corpus = [jieba.lcut(doc) for doc in documents]
        # 创建 BM25 模型
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        检索与查询最相关的文档

        Args:
            query: 用户查询（中文）
            top_k: 返回最相关的文档数量

        Returns:
            相关文档列表，按相关性从高到低排序
        """
        if not self.bm25:
            return []

        # 对查询进行分词
        tokenized_query = jieba.lcut(query)

        # 计算每个文档与查询的 BM25 分数
        scores = self.bm25.get_scores(tokenized_query)

        # 获取分数最高的 top_k 个文档索引
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        # 返回对应文档
        return [self.corpus[i] for i in top_n]
