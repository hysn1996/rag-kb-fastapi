<template>
  <div class="main-layout">
    <Sidebar />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.main-content {
  flex: 1;
  overflow: hidden;
  background: #f5f7fa;
}
</style>