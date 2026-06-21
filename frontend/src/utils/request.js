/**
 * Axios 二次封装（备用）
 */

import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 60000
})

export default request