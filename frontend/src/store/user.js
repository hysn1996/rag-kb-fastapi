/**
 * 用户状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 用户信息
  const userInfo = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isLoggedIn = ref(!!token.value)

  // 设置用户信息
  function setUserInfo(info) {
    userInfo.value = info
  }

  // 设置 token
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
    isLoggedIn.value = !!newToken
  }

  // 登出
  function logout() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('token')
    isLoggedIn.value = false
  }

  return {
    userInfo,
    token,
    isLoggedIn,
    setUserInfo,
    setToken,
    logout
  }
})