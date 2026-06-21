/**
 * 流式响应处理工具
 */

/**
 * 处理 SSE 流式响应
 * @param {Response} response - fetch Response 对象
 * @param {function} onChunk - 每个数据块的回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 */
export async function handleStream(response, onChunk, onDone, onError) {
  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') {
            onDone && onDone()
            return
          }
          onChunk && onChunk(data)
        }
      }
    }
    onDone && onDone()
  } catch (error) {
    onError && onError(error)
  }
}

/**
 * 使用 fetch 发送流式请求
 * @param {string} url - 请求地址
 * @param {object} body - 请求体
 * @param {function} onChunk - 数据块回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 */
export async function fetchStream(url, body, onChunk, onDone, onError) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    await handleStream(response, onChunk, onDone, onError)
  } catch (error) {
    onError && onError(error)
  }
}