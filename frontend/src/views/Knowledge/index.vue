<template>
  <div class="knowledge-page">
    <div class="page-header">
      <h1>知识库管理</h1>
      <el-button type="primary" @click="handleUpload">
        <el-icon><Plus /></el-icon>
        上传文档
      </el-button>
    </div>

    <el-table :data="knowledgeList" style="width: 100%">
      <el-table-column prop="name" label="知识库名称" />
      <el-table-column prop="count" label="文档数量" />
      <el-table-column prop="updateTime" label="更新时间" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="handleView(row)">查看</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useKbStore } from '@/store/kb'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const kbStore = useKbStore()

const knowledgeList = kbStore.knowledgeList

onMounted(() => {
  kbStore.fetchKnowledgeList()
})

function handleUpload() {
  router.push('/knowledge/upload')
}

function handleView(row) {
  ElMessage.info(`查看知识库: ${row.name}`)
}

function handleDelete(row) {
  ElMessageBox.confirm('确定删除该知识库？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    kbStore.removeKnowledge(row.id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.knowledge-page {
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
</style>