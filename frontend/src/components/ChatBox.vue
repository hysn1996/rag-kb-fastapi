<template>
  <div class="chat-box">
    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef">
      <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
        <div class="message-avatar">
          <el-avatar :size="36" :icon="msg.role === 'user' ? User : ChatDotRound" />
        </div>
        <div class="message-content">
          <MarkdownRenderer :content="msg.content" />
          <span v-if="streamingMessageId === msg.id" class="typing-indicator">▌</span>
          <!-- 来源文件 -->
          <div v-if="msg.source_files && msg.source_files.length > 0" class="source-files">
            <span class="source-label">📄 来源：</span>
            <span v-for="(file, index) in msg.source_files" :key="index" class="source-file">
              {{ file }}{{ index < msg.source_files.length - 1 ? '、' : '' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="2"
        placeholder="请输入您的问题..."
        @keydown.enter.ctrl="handleSend"
        :disabled="loading"
      />
      <div class="input-actions">
        <el-button type="primary" @click="handleSend" :disabled="loading">
          发送
        </el-button>
        <el-button @click="handleClear" :disabled="loading">清空</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { User, ChatDotRound } from '@element-plus/icons-vue'
import { useChatStore } from '@/store/chat'
import MarkdownRenderer from './Markdown.vue'

const chatStore = useChatStore()

const inputText = ref('')
const messageListRef = ref(null)

const messages = chatStore.messages
const loading = chatStore.loading
const streamingMessageId = chatStore.streamingMessageId

function handleSend() {
  if (!inputText.value.trim() || loading) return
  chatStore.sendMessage(inputText.value)
  inputText.value = ''
}

function handleClear() {
  chatStore.clearMessages()
}

function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

watch(
  () => chatStore.messages.length,
  scrollToBottom
)

watch(
  () => chatStore.streamingMessageId,
  () => {
    if (chatStore.streamingMessageId) {
      scrollToBottom()
    }
  }
)

watch(
  () => messages.value,
  () => {
    if (chatStore.streamingMessageId) {
      scrollToBottom()
    }
  },
  { deep: true }
)
</script>

<style scoped>
.chat-box {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f5f7fa;
}

.message-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 20px;
}

.message {
  display: flex;
  margin-bottom: 16px;
  gap: 12px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  position: relative;
}

.message.user .message-content {
  background: #409eff;
  color: #fff;
}

.typing-indicator {
  display: inline-block;
  animation: blink 1s step-end infinite;
  color: #909399;
  margin-left: 2px;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.source-files {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #e4e7ed;
  font-size: 12px;
  color: #909399;
}

.source-label {
  margin-right: 4px;
}

.source-file {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 4px;
}

.input-area {
  flex-shrink: 0;
  padding: 16px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
