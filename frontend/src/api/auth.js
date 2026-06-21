/**
 * 认证相关 API（预留扩展）
 */

import http from './http'

/**
 * 用户登录
 */
export function login(username, password) {
  return http.post('/api/auth/login', { username, password })
}

/**
 * 用户登出
 */
export function logout() {
  return http.post('/api/auth/logout')
}

/**
 * 获取当前用户信息
 */
export function getUserInfo() {
  return http.get('/api/auth/user')
}