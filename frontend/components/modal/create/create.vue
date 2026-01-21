<script setup>
// Store с защитой от SSR
const rootStore = ref(null)
const lecturesStore = useLecturesStore()
const authStore = useAuthStore()

onMounted(() => {
  rootStore.value = useRootStore()
  
  watch(
    () => rootStore.value?.getModal,
    (val) => {
      if (val === 'add') {
        isModalOpen.value = true
      } else {
        closeModal()
      }
    }
  )
})

// Состояние модалки
const isModalOpen = ref(false)

// Список тем для селекта
const topics = [
  { value: 'Кластеризация', label: 'Кластеризация' },
  { value: 'Классификация', label: 'Классификация' },
  { value: 'Регрессия', label: 'Регрессия' },
  { value: 'Deep Learning', label: 'Deep Learning' },
  { value: 'Машинное обучение', label: 'Машинное обучение' },
  { value: 'Анализ данных', label: 'Анализ данных' }
]

// Объект формы
const formData = ref({
  name: '',
  topic: '',
  file: null,
})

// Ошибки валидации
const formErrors = ref({
  name: '',
  topic: '',
  file: ''
})

// Обработчик ошибок файла
const handleFileError = (errorMessage) => {
  console.error('Ошибка файла:', errorMessage)
  formErrors.value.file = errorMessage
}

// Валидация
const validateField = (field, value) => {
  switch (field) {
    case 'name':
      return !value.trim() ? 'Название обязательно' : ''
    case 'topic':
      return !value ? 'Выберите тему' : ''
    case 'file':
      return !value ? 'Файл обязателен' : ''
    default:
      return ''
  }
}

// Отправка формы
const handleSubmit = async () => {
  // Валидация всех полей
  Object.keys(formData.value).forEach(field => {
    formErrors.value[field] = validateField(field, formData.value[field])
  })
  
  // Проверка есть ли ошибки
  const hasErrors = Object.values(formErrors.value).some(error => error)
  
  if (hasErrors) {
    alert('Исправьте ошибки в форме')
    return
  }
  const formDataToSend = new FormData()

  console.log(formData.value.name);
  formDataToSend.append('name', formData.value.name)
  formDataToSend.append('topic', formData.value.topic)

  // Добавляем файл
  if (formData.value.file) {
    formDataToSend.append('file', formData.value.file)
  }

  await lecturesStore.createLecture(formDataToSend);
  await authStore.checkAuth();
  await lecturesStore.fetchLectures();
  closeModal()
}

// Закрытие модалки
const closeModal = () => {
  isModalOpen.value = false
  rootStore.value?.setModal('')
  resetForm()
}

// Сброс формы
const resetForm = () => {
  formData.value = {
    name: '',
    topic: '',
    file: null,
  }
  formErrors.value = {
    name: '',
    topic: '',
    file: ''
  }
}

// Отмена
const handleCancel = () => {
  if (formData.value.file || formData.value.name || formData.value.author) {
    if (confirm('Есть несохраненные изменения. Закрыть модалку?')) {
      closeModal()
    }
  } else {
    closeModal()
  }
}
</script>

<template>
  <UiModal
    v-model="isModalOpen"
    @close="handleCancel"
    class="modal-create"
    size="md"
  >
    <!-- Заголовок модалки -->
    <div class="modal-create__header">
      <div class="modal-create__title">Создание лекции</div>
      <div class="modal-create__subtitle">
        Заполните информацию о лекции
      </div>
    </div>
    
    <!-- Форма -->
    <form
      @submit.prevent="handleSubmit"
      class="modal-create__form"
    >
      <!-- Название -->
      <UiTextInput
        v-model="formData.name"
        label="Название лекции"
        placeholder="Введите название лекции"
        :required="true"
        :error="formErrors.name"
        @blur="formErrors.name = validateField('name', formData.name)"
      />
      
      <!-- Тема -->
      <UiSelect
        v-model="formData.topic"
        label="Тема"
        :options="topics"
        placeholder="Выберите тему"
        :required="true"
        :error="formErrors.topic"
        @change="formErrors.topic = validateField('topic', formData.topic)"
      />
      
      <!-- Файл -->
      <UiFileUpload
        v-model="formData.file"
        label="Файл лекции (.ipynb)"
        :max-size-mb="50"
        :error="formErrors.file"
        @error="handleFileError"
        @update:model-value="formErrors.file = ''"
      />
      
      <!-- Кнопки -->
      <div class="modal-create__actions">
        <UiButton
          type="button"
          variant="outline"
          @click="handleCancel"
        >
          Отмена
        </UiButton>
        
        <UiButton
          type="submit"
          :disabled="!formData.file || !formData.name"
        >
          Создать лекцию
        </UiButton>
      </div>
    </form>
  </UiModal>
</template>

<style scoped lang="scss">
.modal-create {
  &__header {
    margin-bottom: 2rem;
  }
  
  &__title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--color-dark);
    margin-bottom: 0.5rem;
  }
  
  &__subtitle {
    font-size: 1rem;
    color: var(--color-dark-64);
  }
  
  &__form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  &__actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--color-border);
  }
}
</style>