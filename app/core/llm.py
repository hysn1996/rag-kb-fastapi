"""
LLM（大语言模型）客户端模块
封装与千问/通义千问 API 的交互
"""

import os
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIError
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    """
    LLM 客户端类
    负责与千问 API 进行交互，支持普通对话和流式对话
    """

    def __init__(self):
        """
        初始化 LLM 客户端
        """
        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

        if not api_key:
            logger.error("QWEN_API_KEY 未配置！")
            raise ValueError("QWEN_API_KEY 必须在 .env 文件中配置")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0
        )
        self.model = os.getenv("LLM_MODEL", "qwen3.7-plus")
        logger.info(f"LLM 初始化完成，模型: {self.model}, base_url: {base_url}")

    def chat(self, messages: list) -> str:
        """
        普通对话接口（非流式）

        Args:
            messages: 对话历史，格式为 [{"role": "user"/"assistant", "content": "..."}]

        Returns:
            模型生成的回复文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except APIConnectionError as e:
            logger.error(f"LLM API 连接失败: {e}")
            logger.error("请检查网络连接或 QWEN_API_KEY 是否正确")
            raise
        except APIError as e:
            logger.error(f"LLM API 错误: {e}")
            raise
        except Exception as e:
            logger.error(f"LLM 调用失败: {type(e).__name__}: {e}")
            raise

    def stream_chat(self, messages: list):
        """
        流式对话接口

        Args:
            messages: 对话历史

        Yields:
            每次 yielded 一个文本片段（chunk），实现打字机效果
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            for chunk in stream:
                # 安全检查：choices 可能为空
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield delta.content
        except APIConnectionError as e:
            logger.error(f"LLM 流式 API 连接失败: {e}")
            raise
        except APIError as e:
            logger.error(f"LLM 流式 API 错误: {e}")
            raise
        except Exception as e:
            logger.error(f"LLM 流式调用失败: {type(e).__name__}: {e}")
            raise