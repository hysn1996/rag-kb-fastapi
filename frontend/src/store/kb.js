/**
 * 知识库状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useKbStore = defineStore('kb', () => {
  // 知识库列表
  const knowledgeList = ref([])

  // 加载状态
  const loading = ref(false)

  /**
   * 获取知识库列表
   */
  async function fetchKnowledgeList() {
    loading.value = true
    try {
      // const response = await getKnowledgeList()
      // knowledgeList.value = response.data
      // 临时模拟数据
      knowledgeList.value = [
        { id: 1, name: '公司制度文档', count: 15, updateTime: '2024-01-15' },
        { id: 2, name: '产品手册', count: 8, updateTime: '2024-01-10' }
      ]
    } catch (err) {
      console.error('获取知识库列表失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 添加知识库
   */
  function addKnowledge(item) {
    knowledgeList.value.push(item)
  }

  /**
   * 删除知识库
   */
  function removeKnowledge(id) {
    const index = knowledgeList.value.findIndex(item => item.id === id)
    if (index > -1) {
      knowledgeList.value.splice(index, 1)
    }
  }

  return {
    knowledgeList,
    loading,
    fetchKnowledgeList,
    addKnowledge,
    removeKnowledge
  }
})