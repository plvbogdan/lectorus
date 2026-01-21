<script setup>
import { ref, computed, onMounted } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css' // или другая тема

const props = defineProps({
  source: {
    type: [String, Array],
    default: ''
  },
  language: {
    type: String,
    default: 'text'
  },
  showLineNumbers: {
    type: Boolean,
    default: true
  },
  copyTooltip: {
    type: String,
    default: 'Копировать'
  }
})

// Реактивное состояние
const isCopied = ref(false)
const isCopying = ref(false)

// Вычисляемые свойства
const codeText = computed(() => {
  if (Array.isArray(props.source)) {
    return props.source.join('')
  }
  return String(props.source || '')
})

const linesCount = computed(() => {
  return codeText.value.split('\n').length
})

const languageClass = computed(() => {
  if (!props.language || props.language === 'text') {
    return ''
  }
  return `language-${props.language}`
})

// Функция для подсветки кода
const highlightedCode = computed(() => {
  const code = codeText.value
  
  if (!code.trim()) return ''
  
  try {
    if (props.language && props.language !== 'text') {
      return hljs.highlight(code, { 
        language: props.language,
        ignoreIllegals: true 
      }).value
    } else {
      return hljs.highlightAuto(code).value
    }
  } catch (error) {
    console.error('Ошибка подсветки кода:', error)
    return code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
  }
})

const handleCopy = async () => {
  if (!codeText.value.trim()) return
  
  isCopying.value = true
  
  try {
    await navigator.clipboard.writeText(codeText.value)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
    
  } catch (error) {
    console.error('Ошибка копирования:', error)
  } finally {
    isCopying.value = false
  }
}

</script>

<template>
  <div class="ui-code">
    <div class="ui-code__header">
      <div class="ui-code__info">
        <span v-if="language" class="ui-code__language">
          {{ language }}
        </span>
        <span v-if="showLineNumbers && linesCount > 0" class="ui-code__lines">
          {{ linesCount }} строк{{ linesCount === 1 ? 'а' : '' }}
        </span>
      </div>
      
      <button 
        class="ui-code__copy"
        @click="handleCopy"
        :title="copyTooltip"
        :disabled="isCopying || !source"
      >
        <span v-if="!isCopying && !isCopied" class="ui-code__copy-text">Копировать</span>
        <span v-if="isCopied" class="ui-code__copy-text">Скопировано</span>
      </button>
    </div>
    
    <!-- Контейнер с кодом -->
    <div class="ui-code__container">
      <!-- Номера строк -->
      <div 
        v-if="showLineNumbers" 
        class="ui-code__line-numbers"
        aria-hidden="true"
      >
        <span 
          v-for="lineNumber in linesCount" 
          :key="lineNumber"
          class="ui-code__line-number"
        >
          {{ lineNumber }}
        </span>
      </div>
      
      <!-- Сам код -->
      <pre class="ui-code__pre"><code 
        :class="languageClass"
        v-html="highlightedCode"
      /></pre>
    </div>
  </div>
</template>



<style src="./__ui-code.scss" lang="scss" />