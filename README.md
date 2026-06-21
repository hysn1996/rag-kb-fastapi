# RAG-KB-FastAPI

基于 FastAPI 的 RAG（检索增强生成）知识库系统，集成阿里云千问大模型，支持流式对话和多轮对话记忆。

## 功能特性

- ✅ 流式对话接口（SSE）
- ✅ 混合检索（BM25 + 向量检索）
- ✅ 多轮对话记忆
- ✅ 查询路由分类（RAG / Chat）
- ✅ 知识库来源文件展示
- ✅ 完整前端界面（Vue 3 + Element Plus）
- ✅ Docker 容器化部署
- ✅ Vercel 一键部署

## 技术栈

### 后端
- **框架**: FastAPI 0.115
- **语言**: Python 3.13
- **LLM**: 阿里云千问 API
- **向量检索**: scikit-learn cosine similarity
- **关键词检索**: BM25 + jieba 分词

### 前端
- **框架**: Vue 3 + Vite
- **UI**: Element Plus
- **状态管理**: Pinia
- **流式处理**: SSE (Server-Sent Events)

## 快速开始

### 环境要求

- Python >= 3.13
- Node.js >= 18 (前端)
- 阿里云千问 API Key

### 后端安装

```bash
# 克隆项目
git clone <repository-url>
cd rag-kb-fastapi

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 前端安装

```bash
cd frontend
npm install
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并填写：

```env
# .env 文件
QWEN_API_KEY=your-qwen-api-key-here
LLM_MODEL=qwen-max
EMBEDDING_MODEL=text-embedding-v3
```

**可用模型：**

| 类型 | 模型名称 | 说明 |
|------|---------|------|
| LLM | `qwen-max` | 最强模型，适合复杂推理 |
| LLM | `qwen-plus` | 中等规模，平衡速度和性能 |
| LLM | `qwen-turbo` | 快速模型，适合简单问答 |
| Embedding | `text-embedding-v3` | 千问向量化模型 |

### 启动服务

#### 开发模式

**后端：**
```bash
python run.py
```

**前端：**
```bash
cd frontend
npm run dev
```

#### Docker 部署

```bash
# 编辑 docker-compose.yml，替换 QWEN_API_KEY
# 启动服务
docker-compose up -d
```

## API 接口

### 流式聊天

```bash
POST /api/chat/stream
Content-Type: application/json

{
    "query": "报销流程是什么？",
    "session_id": "abc123"
}
```

**响应格式（SSE）：**
```
data: [SOURCE_FILES]["docs.txt"]

data: 根据

data: 公司

data: 报销

data: 制度...

data: [DONE]
```

### 健康检查

```bash
GET /api/health
```

## 项目结构

```
rag-kb-fastapi/
├── app/                    # 后端核心代码
│   ├── main.py             # FastAPI入口
│   ├── api/                # API路由
│   │   └── chat_stream.py  # 流式聊天接口
│   ├── core/               # 核心组件
│   │   ├── llm.py          # LLM客户端（千问）
│   │   └── prompt.py       # Prompt模板
│   ├── retrieval/          # 检索模块
│   │   ├── bm25.py         # BM25关键词检索
│   │   ├── vector.py       # 向量相似度检索
│   │   └── hybrid.py       # 混合检索
│   ├── embedding/          # 嵌入模块
│   │   └── embedder.py     # 文本向量化（千问）
│   ├── service/            # 业务逻辑
│   │   └── rag_service.py  # RAG核心服务
│   ├── memory/             # 对话记忆
│   │   └── memory.py       # 多轮对话管理
│   └── router/             # 查询路由
│       └── query_router.py # 问题分类路由
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── api/            # API接口
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── store/          # Pinia状态管理
│   │   └── router/         # Vue路由
│   └── package.json
├── data/                   # 知识库文档
│   └── docs.txt            # 企业知识库（文本版）
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python依赖
├── run.py                  # 启动脚本
├── .env.example            # 环境变量示例
└── .gitignore              # Git忽略规则
```

## 路由分类规则

QueryRouter 根据关键词将问题分类：

| 类型 | 触发关键词 | 处理方式 |
|------|-----------|---------|
| RAG | 报销、请假、工资、制度、流程、考勤等 | 检索知识库 + LLM回答 |
| Chat | 其他问题 | 仅 LLM 回答 |

## 知识库文档格式

在 `data/docs.txt` 中添加企业知识库内容，系统会自动分块并构建检索索引。

```
报销制度：
- 报销时间：提交申请后3-7个工作日
- 所需材料：发票原件、报销申请单、审批记录

请假流程：
- 年假：提前3天申请
- 病假：需提供医院证明
```

## 部署建议

### 🚀 Vercel 一键部署（推荐）

**最快部署方式，无需服务器配置**

#### 前置要求
- GitHub 账号
- Vercel 账号（可使用 GitHub 登录）
- 阿里云千问 API Key

#### 部署步骤

1. **推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/rag-kb-fastapi.git
   git push -u origin main
   ```

2. **导入到 Vercel**
   - 访问 https://vercel.com/new
   - 选择你的 GitHub 仓库
   - Vercel 会自动检测项目配置

3. **配置环境变量**
   
   在 Vercel 项目设置中添加：
   ```bash
   QWEN_API_KEY=your-qwen-api-key-here
   LLM_MODEL=qwen-max
   EMBEDDING_MODEL=text-embedding-v3
   QWEN_API_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   ```

4. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成（通常 2-3 分钟）
   - 访问你的 Vercel URL

#### 部署特点
- ✅ 前后端一体化部署
- ✅ 自动 HTTPS
- ✅ 全球 CDN 加速
- ✅ 自动扩缩容
- ✅ 免费额度充足

**注意**: 流式接口 `/api/chat/stream` 在 Vercel 上可能不稳定，建议使用 `/api/chat` 接口。

详细部署指南请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

### 🐳 Docker 部署

**适合需要完整控制的生产环境**

```bash
# 编辑 docker-compose.yml，替换 QWEN_API_KEY
# 启动服务
docker-compose up -d
```

### 本地开发部署

1. 使用 Docker 部署
2. 配置 Nginx 反向代理
3. 使用 HTTPS（Let's Encrypt）
4. 限制 CORS 来源

### 安全注意事项

- ✅ 不要将 `.env` 提交到代码仓库
- ✅ 使用环境变量管理敏感信息
- ✅ 限制 API 访问频率
- ✅ 开启 HTTPS

## License

MIT License