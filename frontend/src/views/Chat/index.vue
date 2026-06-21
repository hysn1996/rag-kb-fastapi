<template>
  <div class="chat-page">
    <div class="page-header">
      <h1>AI 对话</h1>
      <p>基于知识库的智能问答系统</p>
    </div>
    <div class="chat-container">
      <ChatBox />
    </div>
  </div>
</template>

<script setup>
import ChatBox from '@/components/ChatBox.vue'
</script>

<style scoped>
.chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 16px;
  flex-shrink: 0;
}

.page-header h1 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 8px;
}

.page-header p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.chat-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>
