"""
RAG 核心服务模块
整合检索、生成、多轮对话的完整 RAG 流程
"""

from app.retrieval.hybrid import HybridRetriever  # 混合检索器
from app.core.llm import LLMClient               # LLM 客户端
from app.core.prompt import PromptTemplate        # Prompt 模板
from app.memory.memory import ChatMemory         # 对话记忆
from app.router.query_router import QueryRouter  # 查询路由
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG 服务类
    核心业务逻辑：接收用户查询 -> 路由分类 -> 执行不同分支 -> LLM 生成
    """

    def __init__(self):
        self.retriever = HybridRetriever()  # 混合检索器
        self.llm = LLMClient()              # LLM 客户端
        self.memory = ChatMemory()          # 对话记忆
        self.router = QueryRouter()         # 查询路由器

        logger.info(f"RAGService 初始化完成，LLM 模型: {self.llm.model}")

        # 初始化时加载文档并构建索引
        self._load_documents()

    def _load_documents(self):
        """
        加载知识库文档并构建检索索引
        """
        docs_path = os.path.join(os.path.dirname(__file__), "../../data/docs.txt")
        try:
            with open(docs_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents = self._split_text(content)
            self.retriever.build_index(documents)
            logger.info(f"Loaded {len(documents)} documents from {docs_path}")
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")

    def _split_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
        """
        将长文档分割为较小的文本块
        """
        chunks = []
        sentences = text.split("\n")
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence[:chunk_size]

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def get_context(self, query: str) -> tuple:
        """
        获取与查询相关的上下文和来源文件

        Returns:
            (context, source_files): 上下文内容和来源文件名列表
        """
        retrieved_docs = self.retriever.retrieve(query)
        context = "\n\n".join(retrieved_docs)

        # 获取来源文件（从配置中读取，当前只支持 docs.txt）
        docs_path = os.path.join(os.path.dirname(__file__), "../../data/docs.txt")
        source_files = [os.path.basename(docs_path)] if retrieved_docs else []

        return context, source_files

    def chat(self, query: str, session_id: str = None) -> dict:
        """
        普通对话接口（非流式）

        路由逻辑：
        1. rag: RAG 检索 + LLM 回答
        2. chat: 仅 LLM 回答（无 RAG 上下文）

        Returns:
            dict: {response, source_files}
        """
        # 路由分类
        decision = self.router.classify(query)
        logger.info(f"Query routing: {decision}")

        # 获取对话历史
        history = self.memory.get_history(session_id)

        source_files = []

        # ===== 1. RAG =====
        if decision["type"] == "rag":
            context, source_files = self.get_context(query)
            messages = PromptTemplate.build_rag_prompt(query, context, history)
        else:
            # ===== 2. chat =====
            context = ""
            messages = PromptTemplate.build_rag_prompt(query, "", history)

        # 调用 LLM
        response = self.llm.chat(messages)

        # 保存对话历史
        self.memory.add_message(session_id, query, response)

        return {"response": response, "source_files": source_files}

    def stream_chat(self, query: str, session_id: str = None):
        """
        流式对话接口

        路由逻辑同上，但支持流式输出
        """
        # 路由分类
        decision = self.router.classify(query)
        logger.info(f"Query routing: {decision}")

        # 获取对话历史
        history = self.memory.get_history(session_id)

        source_files = []

        # ===== 1. RAG =====
        if decision["type"] == "rag":
            context, source_files = self.get_context(query)
            messages = PromptTemplate.build_rag_prompt(query, context, history)
        else:
            # ===== 2. chat =====
            context = ""
            messages = PromptTemplate.build_rag_prompt(query, "", history)

        # 先发送来源文件信息（使用特殊标记）
        if source_files:
            import json
            yield f"data: [SOURCE_FILES]{json.dumps(source_files)}\n\n"

        # 流式调用 LLM
        full_response = ""
        for chunk in self.llm.stream_chat(messages):
            full_response += chunk
            yield f"data: {chunk}\n\n"

        # 保存对话历史
        self.memory.add_message(session_id, query, full_response)

        # 发送结束标识
        yield "data: [DONE]\n\n"