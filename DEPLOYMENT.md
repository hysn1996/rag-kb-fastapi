# Vercel 部署指南

## 📋 部署前准备

### 1. 环境变量配置

在 Vercel 项目设置中配置以下环境变量：

```bash
QWEN_API_KEY=your-qwen-api-key-here
LLM_MODEL=qwen-max
EMBEDDING_MODEL=text-embedding-v3
QWEN_API_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 2. 项目文件结构

确保项目包含以下关键文件：

```
rag-kb-fastapi/
├── api/
│   └── index.py              # Vercel Serverless Function 入口
├── app/
│   ├── main.py              # FastAPI 主应用
│   ├── api/
│   ├── core/
│   ├── embedding/
│   ├── memory/
│   ├── retrieval/
│   ├── router/
│   └── service/
├── frontend/
│   ├── .env.production      # 生产环境配置
│   ├── package.json
│   └── vite.config.js
├── requirements.txt         # Python 依赖（包含 mangum）
├── vercel.json             # Vercel 配置
└── .vercelignore           # Vercel 忽略文件
```

## 🚀 部署步骤

### 方式一：通过 Vercel CLI 部署

1. **安装 Vercel CLI**
```bash
npm install -g vercel
```

2. **登录 Vercel**
```bash
vercel login
```

3. **部署项目**
```bash
cd rag-kb-fastapi
vercel
```

4. **配置环境变量**
   - 在部署过程中，Vercel 会提示配置环境变量
   - 或者在 Vercel Dashboard 中手动添加

5. **生产部署**
```bash
vercel --prod
```

### 方式二：通过 Git 集成部署

1. **推送到 Git 仓库**
```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git remote add origin your-repo-url
git push -u origin main
```

2. **在 Vercel Dashboard 导入项目**
   - 访问 https://vercel.com/new
   - 选择你的 Git 仓库
   - Vercel 会自动检测项目配置

3. **配置环境变量**
   - 在项目设置 → Environment Variables 中添加环境变量

4. **部署**
   - 点击 "Deploy" 按钮开始部署

## ⚙️ 配置说明

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/$1"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 60
    }
  }
}
```

### 路由配置

- `/api/*` → Python Serverless Function
- `/*` → 静态前端文件

### 前端配置

- 开发环境：使用 Vite proxy 转发到本地 API
- 生产环境：直接调用 `/api` 路由

## 🔧 重要注意事项

### 1. Serverless Functions 限制

- **执行时间**：最大 60 秒（已配置）
- **内存限制**：根据 Vercel 计划不同
- **冷启动**：首次请求可能有延迟

### 2. 数据持久化

Vercel Serverless Functions 是无状态的，需要考虑：

- **知识库数据**：建议使用外部存储（如 Vercel KV、MongoDB Atlas）
- **会话管理**：使用外部存储或 JWT token

### 3. 流式响应

当前项目中的 `/api/chat/stream` 接口在 Vercel 上可能不工作，因为：
- Vercel Serverless Functions 不完全支持 SSE
- 建议使用 `/api/chat` 接口代替

### 4. 文件上传

如果需要文件上传功能，需要：
- 使用 Vercel Blob Storage 或其他对象存储
- 修改前端上传逻辑

## 📊 性能优化

### 1. 减少冷启动时间

- 使用 Vercel 的 Pro 计划获得更好的性能
- 优化依赖包大小
- 考虑使用 Vercel Edge Functions（部分场景）

### 2. 前端优化

- 已配置代码分割
- 启用 CDN 缓存
- 压缩静态资源

### 3. API 优化

- 使用缓存减少重复计算
- 优化数据库查询
- 考虑使用 Vercel KV 缓存

## 🐛 故障排查

### 1. 部署失败

- 检查 `requirements.txt` 依赖是否正确
- 确认 Python 版本兼容性
- 查看部署日志

### 2. API 调用失败

- 检查环境变量是否配置正确
- 确认 API 路由配置
- 查看 Vercel 函数日志

### 3. 前端无法访问 API

- 检查 `vercel.json` 路由配置
- 确认前端 API 基础 URL 设置
- 查看浏览器控制台错误

## 📈 监控和日志

- 使用 Vercel Analytics 监控性能
- 查看 Vercel Logs 调试问题
- 设置错误告警

## 🔄 更新部署

- 代码推送到 Git 仓库会自动触发部署
- 或使用 `vercel --prod` 手动部署

## 📞 支持

如有问题，请查看：
- [Vercel 文档](https://vercel.com/docs)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- 项目 GitHub Issues