<!-- components/ui/UIFileUpload.vue -->
<script setup>
import { ref } from 'vue'

const props = defineProps({
  // Текстовая метка
  label: {
    type: String,
    default: 'Файл лекции (.ipynb)'
  },
  // Максимальный размер в MB
  maxSizeMB: {
    type: Number,
    default: 5
  },
  // Уже загруженный файл (для редактирования)
  modelValue: {
    type: File,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'error'])

// Состояния
const uploadedFile = ref(props.modelValue)
const fileInput = ref(null)
const isDragging = ref(false)

// Конфигурация
const ALLOWED_TYPES = ['.ipynb']

// Проверка файла
const validateFile = (file) => {
  // Проверка расширения
  if (!file.name.toLowerCase().endsWith('.ipynb')) {
    emitError('Только файлы .ipynb (Jupyter Notebook) разрешены')
    return false
  }
  
  // Проверка размера
  const maxSizeBytes = props.maxSizeMB * 1024 * 1024
  if (file.size > maxSizeBytes) {
    emitError(`Файл слишком большой. Максимум ${props.maxSizeMB}MB`)
    return false
  }
  
  return true
}

// Отправка ошибки
const emitError = (message) => {
  emit('error', message)
  alert(message) // Показываем alert как просили
}

// Обработчики
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && validateFile(file)) {
    uploadedFile.value = file
    emit('update:modelValue', file)
  } else {
    resetFileInput()
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  
  const file = event.dataTransfer.files[0]
  if (file && validateFile(file)) {
    uploadedFile.value = file
    emit('update:modelValue', file)
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = (event) => {
  if (!event.currentTarget.contains(event.relatedTarget)) {
    isDragging.value = false
  }
}

const removeFile = () => {
  uploadedFile.value = null
  emit('update:modelValue', null)
  resetFileInput()
}

const resetFileInput = () => {
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const openFileDialog = () => {
  fileInput.value?.click()
}

// Форматирование размера файла
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Watch для обновления внешнего значения
watch(() => props.modelValue, (newFile) => {
  uploadedFile.value = newFile
})
</script>

<template>
  <div class="ui-file-upload">
    <!-- Метка -->
    <label v-if="label" class="ui-file-upload__label">
      {{ label }}
    </label>
    
    <!-- Drag & Drop область -->
    <div
      class="ui-file-upload__dropzone"
      :class="{ 'ui-file-upload__dropzone--dragging': isDragging }"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      @click="openFileDialog"
    >
      <div class="ui-file-upload__content">
        <Icon 
          name="mdi:notebook" 
          class="ui-file-upload__icon"
          :class="{ 'ui-file-upload__icon--dragging': isDragging }"
        />
        
        <p class="ui-file-upload__text">
          <template v-if="isDragging">
            Отпустите файл здесь
          </template>
          <template v-else>
            Перетащите файл <strong>.ipynb</strong> сюда или
            <span class="ui-file-upload__browse">выберите через обзор</span>
          </template>
        </p>
        
        <p class="ui-file-upload__hint">
          Только Jupyter Notebook (.ipynb), максимум {{ maxSizeMB }}MB
        </p>
      </div>
      
      <!-- Скрытый input -->
      <input
        ref="fileInput"
        type="file"
        class="ui-file-upload__input"
        @change="handleFileSelect"
        accept=".ipynb"
      />
    </div>
    
    <!-- Загруженный файл -->
    <div v-if="uploadedFile" class="ui-file-upload__preview">
      <div class="ui-file-upload__file-info">
        <Icon name="mdi:check-circle" class="ui-file-upload__file-icon" />
        
        <div class="ui-file-upload__file-details">
          <span class="ui-file-upload__file-name">
            {{ uploadedFile.name }}
          </span>
          <span class="ui-file-upload__file-size">
            {{ formatFileSize(uploadedFile.size) }}
          </span>
        </div>
        
        <button
          type="button"
          class="ui-file-upload__remove-btn"
          @click.stop="removeFile"
          aria-label="Удалить файл"
        >
          <Icon name="mdi:close" />
        </button>
      </div>
      
      <!-- Кнопка удаления -->
      <button
        type="button"
        class="ui-file-upload__delete-btn"
        @click="removeFile"
      >
        <Icon name="mdi:trash-can-outline" />
        Удалить файл
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.ui-file-upload {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  
  &__label {
    font-weight: 500;
    color: var(--color-dark-80);
    font-size: 0.95rem;
  }
  
  // Drag & Drop зона
  &__dropzone {
    border: 2px dashed var(--color-border, #ddd);
    border-radius: 0.75rem;
    padding: 2.5rem 1.5rem;
    text-align: center;
    cursor: pointer;
    background: var(--color-background, #f8fafc);
    transition: all 0.25s ease;
    position: relative;
    
    &--dragging {
      border-color: var(--color-blue, #3b82f6);
      background: rgba(59, 130, 246, 0.05);
      transform: translateY(-2px);
    }
    
    &:hover:not(&--dragging) {
      border-color: var(--color-blue-light, #93c5fd);
      background: rgba(59, 130, 246, 0.02);
    }
  }
  
  &__content {
    pointer-events: none;
  }
  
  &__icon {
    font-size: 3.5rem;
    color: var(--color-blue, #3b82f6);
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    
    &--dragging {
      color: var(--color-green, #10b981);
      transform: scale(1.1);
    }
  }
  
  &__text {
    color: var(--color-dark-80);
    margin-bottom: 0.5rem;
    font-size: 1.05rem;
    
    strong {
      color: var(--color-blue, #3b82f6);
      font-weight: 600;
    }
  }
  
  &__browse {
    color: var(--color-blue, #3b82f6);
    text-decoration: underline;
    cursor: pointer;
  }
  
  &__hint {
    font-size: 0.875rem;
    color: var(--color-dark-64);
  }
  
  &__input {
    position: absolute;
    width: 0;
    height: 0;
    opacity: 0;
  }
  
  // Предпросмотр файла
  &__preview {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    animation: slideIn 0.3s ease;
  }
  
  &__file-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(34, 197, 94, 0.05);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-radius: 0.75rem;
    padding: 1rem 1.25rem;
  }
  
  &__file-icon {
    font-size: 1.75rem;
    color: var(--color-green, #10b981);
    flex-shrink: 0;
  }
  
  &__file-details {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    flex: 1;
    min-width: 0;
  }
  
  &__file-name {
    font-weight: 500;
    color: var(--color-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  &__file-size {
    font-size: 0.875rem;
    color: var(--color-dark-64);
  }
  
  &__remove-btn {
    background: none;
    border: none;
    color: var(--color-dark-64);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(239, 68, 68, 0.1);
      color: var(--color-red, #ef4444);
    }
    
    svg {
      font-size: 1.25rem;
    }
  }
  
  // Кнопка удаления
  &__delete-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: none;
    border: 1px solid var(--color-border, #ddd);
    border-radius: 0.5rem;
    padding: 0.75rem;
    color: var(--color-dark-64);
    cursor: pointer;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(239, 68, 68, 0.05);
      border-color: var(--color-red, #ef4444);
      color: var(--color-red, #ef4444);
    }
    
    svg {
      font-size: 1.25rem;
    }
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>