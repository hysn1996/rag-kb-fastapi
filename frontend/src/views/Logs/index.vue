<template>
  <div class="logs-page">
    <div class="page-header">
      <h1>对话日志</h1>
    </div>

    <el-table :data="logs" style="width: 100%">
      <el-table-column prop="time" label="时间" width="180" />
      <el-table-column prop="query" label="用户问题" />
      <el-table-column prop="response" label="AI回答" show-overflow-tooltip />
      <el-table-column prop="sessionId" label="会话ID" width="120" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const logs = ref([
  { time: '2024-01-15 10:30', query: '报销制度是什么？', response: '根据公司报销制度...', sessionId: 'abc123' },
  { time: '2024-01-15 10:35', query: '差旅费怎么报销？', response: '差旅费报销流程...', sessionId: 'abc123' }
])
</script>

<style scoped>
.logs-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  color: #303133;
  margin: 0;
}
</style>