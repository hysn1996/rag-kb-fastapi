/**
 * 知识库相关 API（预留扩展）
 */

import http from './http'

/**
 * 获取知识库列表
 */
export function getKnowledgeList() {
  return http.get('/api/knowledge/list')
}

/**
 * 上传知识库文件
 */
export function uploadKnowledge(file) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post('/api/knowledge/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/**
 * 删除知识库
 */
export function deleteKnowledge(id) {
  return http.delete(`/api/knowledge/${id}`)
}