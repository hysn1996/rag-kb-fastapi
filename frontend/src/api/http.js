/**
 * Axios 请求封装
 * 统一处理请求拦截、响应拦截、错误处理
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 60000, // 请求超时时间 60s
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    // 可在此添加 token 等认证信息
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 统一错误处理
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

export default http