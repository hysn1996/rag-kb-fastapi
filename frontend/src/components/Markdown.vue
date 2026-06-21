<template>
  <div class="markdown-renderer" v-html="renderedContent"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 配置 marked
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (e) {
        console.error(e)
      }
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

const renderedContent = computed(() => {
  return marked.parse(props.content)
})
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
}

.markdown-renderer :deep(h1),
.markdown-renderer :deep(h2),
.markdown-renderer :deep(h3) {
  margin: 16px 0 8px;
  font-weight: 600;
}

.markdown-renderer :deep(p) {
  margin: 8px 0;
}

.markdown-renderer :deep(code) {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', monospace;
}

.markdown-renderer :deep(pre) {
  background: #282c34;
  color: #abb2bf;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-renderer :deep(pre code) {
  background: transparent;
  padding: 0;
}

.markdown-renderer :deep(ul),
.markdown-renderer :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.markdown-renderer :deep(a) {
  color: #409eff;
}
</style>