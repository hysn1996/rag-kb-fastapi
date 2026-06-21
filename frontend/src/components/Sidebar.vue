<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h2>RAG 知识库</h2>
    </div>

    <el-menu
      :default-active="activeMenu"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/chat">
        <el-icon><ChatDotRound /></el-icon>
        <span>AI 对话</span>
      </el-menu-item>

      <el-menu-item index="/knowledge">
        <el-icon><Folder /></el-icon>
        <span>知识库管理</span>
      </el-menu-item>

      <el-menu-item index="/logs">
        <el-icon><Document /></el-icon>
        <span>对话日志</span>
      </el-menu-item>

      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <span>系统配置</span>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-footer">
      <el-button type="primary" @click="handleNewSession">
        <el-icon><Plus /></el-icon>
        新建对话
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '@/store/chat'
import { ChatDotRound, Folder, Document, Setting, Plus } from '@element-plus/icons-vue'

const router = useRouter()
const chatStore = useChatStore()

const activeMenu = computed(() => router.currentRoute.value.path)

function handleNewSession() {
  chatStore.newSession()
  router.push('/chat')
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  height: 100%;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.sidebar-header h2 {
  font-size: 18px;
  color: #303133;
  margin: 0;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e4e7ed;
}
</style>