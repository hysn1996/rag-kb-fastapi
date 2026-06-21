"""
Vercel Serverless Function 入口文件
将 Vercel 请求转发到 FastAPI 应用
"""

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from mangum import Mangum

# 创建 ASGI 适配器
handler = Mangum(app)

# Vercel Serverless Function 入口
def lambda_handler(event, context):
    """
    Vercel Serverless Function 处理器
    将 Vercel 请求转换为 ASGI 请求并转发给 FastAPI
    """
    return handler(event, context)