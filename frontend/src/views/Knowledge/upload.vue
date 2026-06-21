<template>
  <div class="upload-page">
    <div class="page-header">
      <h1>上传知识库文档</h1>
      <el-button @click="handleBack">返回</el-button>
    </div>

    <el-upload
      class="upload-area"
      drag
      action="/api/knowledge/upload"
      multiple
      :on-success="handleSuccess"
      :on-error="handleError"
      accept=".txt,.pdf,.doc,.docx,.md"
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持 txt、pdf、doc、docx、md 格式文件
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

function handleBack() {
  router.push('/knowledge')
}

function handleSuccess(response) {
  ElMessage.success('上传成功')
  router.push('/knowledge')
}

function handleError(error) {
  ElMessage.error('上传失败: ' + error.message)
}
</script>

<style scoped>
.upload-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  color: #303133;
  margin: 0;
}

.upload-area {
  width: 100%;
}
</style>