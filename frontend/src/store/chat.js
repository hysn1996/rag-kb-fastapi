/**
 * 聊天状态管理
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chat } from '@/api/chat'
import { generateId } from '@/utils/format'

export const useChatStore = defineStore('chat', () => {
  // 当前会话 ID
  const sessionId = ref(generateId())

  // 消息列表
  const messages = ref([])

  // 加载状态
  const loading = ref(false)

  // 错误信息
  const error = ref(null)

  // 当前正在流式输出的消息 ID
  const streamingMessageId = ref(null)

  // 消息数量
  const messageCount = computed(() => messages.value.length)

  /**
   * 发送消息（一次性获取，前端模拟流式输出）
   * @param {string} query - 用户问题
   */
  async function sendMessage(query) {
    if (!query.trim()) return

    // 添加用户消息
    messages.value.push({
      id: generateId(),
      role: 'user',
      content: query,
      timestamp: Date.now()
    })

    // 创建助手消息（初始为空，模拟流式更新）
    const assistantMessageId = generateId()
    messages.value.push({
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      source_files: [],
      timestamp: Date.now()
    })

    streamingMessageId.value = assistantMessageId
    loading.value = true
    error.value = null

    try {
      // 一次性获取完整响应
      const result = await chat(query, sessionId.value)

      // 模拟流式输出（打字机效果）
      const fullText = result.response
      const sourceFiles = result.source_files || []
      let index = 0

      const message = messages.value.find(m => m.id === assistantMessageId)
      if (message) {
        message.source_files = sourceFiles
        
        // 逐字显示，模拟打字机效果
        const typeInterval = setInterval(() => {
          if (index < fullText.length) {
            message.content += fullText[index]
            index++
          } else {
            clearInterval(typeInterval)
            streamingMessageId.value = null
            loading.value = false
          }
        }, 30) // 30ms 间隔，可调整速度
      } else {
        streamingMessageId.value = null
        loading.value = false
      }
    } catch (err) {
      error.value = err.message || '请求失败'
      streamingMessageId.value = null
      loading.value = false
      console.error('聊天请求失败:', err)
    }
  }

  /**
   * 清空消息
   */
  function clearMessages() {
    messages.value = []
    sessionId.value = generateId()
    streamingMessageId.value = null
  }

  /**
   * 新建会话
   */
  function newSession() {
    clearMessages()
  }

  return {
    sessionId,
    messages,
    loading,
    error,
    streamingMessageId,
    messageCount,
    sendMessage,
    clearMessages,
    newSession
  }
})