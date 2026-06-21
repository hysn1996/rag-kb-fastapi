"""
RAG KB FastAPI - 主入口文件
用于构建基于检索增强生成(RAG)的知识库问答系统
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat_stream

app = FastAPI(title="RAG KB FastAPI", version="1.0.0")

# 添加 CORS 中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_stream.router, prefix="/api", tags=["chat"])


@app.get("/")
def root():
    return {"message": "RAG Knowledge Base API"}