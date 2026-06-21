"""
聊天 API 路由模块
提供一次性对话接口（兼容 Vercel）
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.service.rag_service import RAGService
from functools import lru_cache

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求模型"""
    query: str           # 用户问题
    session_id: str = None  # 会话ID，用于多轮对话


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    """
    获取 RAG 服务单例实例
    使用 lru_cache 确保整个应用生命周期内只创建一个实例
    避免每次请求都重新加载文档和构建检索索引
    """
    return RAGService()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    一次性聊天接口
    - 接收用户问题，通过 RAG 服务处理
    - 返回完整响应（包含回答内容和来源文件）
    - 支持多轮对话（通过 session_id 区分不同会话）
    """
    try:
        result = rag_service.chat(request.query, request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    流式聊天接口（SSE）
    - 接收用户问题，通过 RAG 服务处理
    - 返回 SSE 格式的流式响应
    - 支持多轮对话（通过 session_id 区分不同会话）
    - 注意：Vercel Serverless Functions 不支持此接口
    """
    try:
        return StreamingResponse(
            rag_service.stream_chat(request.query, request.session_id),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))