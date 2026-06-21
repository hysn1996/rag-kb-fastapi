/**
 * 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/chat',
    children: [
      {
        path: '/chat',
        name: 'Chat',
        component: () => import('@/views/Chat/index.vue'),
        meta: { title: 'AI 对话' }
      },
      {
        path: '/knowledge',
        name: 'Knowledge',
        component: () => import('@/views/Knowledge/index.vue'),
        meta: { title: '知识库管理' }
      },
      {
        path: '/knowledge/upload',
        name: 'KnowledgeUpload',
        component: () => import('@/views/Knowledge/upload.vue'),
        meta: { title: '上传知识库' }
      },
      {
        path: '/logs',
        name: 'Logs',
        component: () => import('@/views/Logs/index.vue'),
        meta: { title: '对话日志' }
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('@/views/Settings/index.vue'),
        meta: { title: '系统配置' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'RAG 知识库'
  next()
})

export default router