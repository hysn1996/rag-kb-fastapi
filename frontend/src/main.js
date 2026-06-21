/**
 * 应用入口文件
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册 Pinia 状态管理
app.use(createPinia())

// 注册 Element Plus
app.use(ElementPlus)

// 注册路由
app.use(router)

app.mount('#app')