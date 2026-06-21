/**
 * 格式化工具函数
 */

/**
 * 格式化日期时间
 * @param {Date|string|number} date - 日期
 * @param {string} format - 格式，默认 'YYYY-MM-DD HH:mm:ss'
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 生成唯一 ID
 */
export function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 防抖函数
 * @param {function} fn - 要防抖的函数
 * @param {number} delay - 延迟时间（毫秒）
 */
export function debounce(fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

/**
 * 节流函数
 * @param {function} fn - 要节流的函数
 * @param {number} delay - 间隔时间（毫秒）
 */
export function throttle(fn, delay = 300) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}