<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>系统配置</h1>
      <p class="subtitle">当前环境：{{ isProduction ? '生产环境' : '开发环境' }}</p>
    </div>

    <el-card class="info-card">
      <template #header>
        <div class="card-header">
          <span>API 配置信息</span>
        </div>
      </template>
      
      <el-descriptions :column="1" border>
        <el-descriptions-item label="API 地址">
          {{ apiUrl }}
        </el-descriptions-item>
        <el-descriptions-item label="LLM 模型">
          {{ llmModel }}
        </el-descriptions-item>
        <el-descriptions-item label="Embedding 模型">
          {{ embeddingModel }}
        </el-descriptions-item>
      </el-descriptions>
      
      <el-alert
        v-if="isProduction"
        title="生产环境配置"
        type="info"
        :closable="false"
        style="margin-top: 16px"
      >
        <template #default>
          <p>生产环境的 API 配置由服务器端环境变量管理，前端无需额外配置。</p>
          <p>如需修改配置，请联系管理员或在 Vercel Dashboard 中设置环境变量。</p>
        </template>
      </el-alert>
      
      <el-alert
        v-else
        title="开发环境配置"
        type="warning"
        :closable="false"
        style="margin-top: 16px"
      >
        <template #default>
          <p>开发环境使用 Vite Proxy 转发 API 请求到本地服务器。</p>
          <p>确保后端服务运行在 http://localhost:8000</p>
        </template>
      </el-alert>
    </el-card>

    <el-card class="help-card">
      <template #header>
        <div class="card-header">
          <span>部署信息</span>
        </div>
      </template>
      
      <el-timeline>
        <el-timeline-item timestamp="本地开发" placement="top">
          <el-card>
            <h4>开发环境</h4>
            <p>前端：npm run dev (端口 3000)</p>
            <p>后端：python run.py (端口 8000)</p>
            <p>API 请求通过 Vite Proxy 自动转发</p>
          </el-card>
        </el-timeline-item>
        
        <el-timeline-item timestamp="Vercel 部署" placement="top">
          <el-card>
            <h4>生产环境</h4>
            <p>前后端一体化部署到 Vercel</p>
            <p>API 请求直接调用 /api 路由</p>
            <p>环境变量在 Vercel Dashboard 中配置</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const isProduction = computed(() => import.meta.env.PROD)

const apiUrl = computed(() => {
  return isProduction.value ? '/api' : 'http://localhost:8000 (通过 Proxy 转发)'
})

const llmModel = computed(() => {
  return isProduction.value ? '服务器配置' : 'qwen-max'
})

const embeddingModel = computed(() => {
  return isProduction.value ? '服务器配置' : 'text-embedding-v3'
})
</script>

<style scoped>
.settings-page {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  color: #303133;
  margin: 0 0 8px;
}

.subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.info-card, .help-card {
  margin-bottom: 24px;
}

.card-header {
  font-weight: 600;
  color: #303133;
}

.el-descriptions {
  margin-top: 16px;
}

.el-alert p {
  margin: 4px 0;
}

.el-timeline-item__content {
  padding-bottom: 20px;
}

.el-timeline-item .el-card {
  margin-top: 8px;
}

.el-timeline-item .el-card h4 {
  margin: 0 0 8px;
  color: #409EFF;
}

.el-timeline-item .el-card p {
  margin: 4px 0;
  color: #606266;
  font-size: 14px;
}
</style>