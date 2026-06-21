/**
 * 聊天相关 API
 */

/**
 * 发送聊天消息（一次性）
 * @param {string} query - 用户问题
 * @param {string} sessionId - 会话ID（可选，用于多轮对话）
 * @returns {Promise<{response: string, source_files: string[]}>}
 */
export async function chat(query, sessionId = null) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query,
      session_id: sessionId
    })
  })
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}