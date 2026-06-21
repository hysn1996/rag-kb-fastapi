"""
文本嵌入（Embedding）模块
将文本转换为稠密向量表示
"""

import os
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIError
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class Embedder:
    """
    文本嵌入器
    使用千问的 Embedding API 将文本转换为向量
    """

    def __init__(self):
        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        if not api_key:
            logger.error("QWEN_API_KEY 未配置！")
            raise ValueError("QWEN_API_KEY 必须在 .env 文件中配置")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0
        )
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
        logger.info(f"Embedding 初始化完成，模型: {self.model}, base_url: {base_url}")

    def encode(self, text: str) -> list:
        """
        将文本编码为向量

        Args:
            text: 输入文本（中文或英文）

        Returns:
            文本的向量表示（浮点数列表）
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except APIConnectionError as e:
            logger.error(f"Embedding API 连接失败: {e}")
            logger.error("请检查网络连接或 QWEN_API_KEY 是否正确")
            raise
        except APIError as e:
            logger.error(f"Embedding API 错误: {e}")
            raise
        except Exception as e:
            logger.error(f"Embedding 编码失败: {type(e).__name__}: {e}")
            raise