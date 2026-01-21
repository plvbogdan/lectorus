<script setup>

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  closeOnOverlayClick: {
    type: Boolean,
    default: true
  },
  closeOnEsc: {
    type: Boolean,
    default: true
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const modalRef = ref(null)

// Закрытие модалки
const closeModal = () => {
  emit('update:modelValue', false)
  emit('close')
}

// // Закрытие по клику вне модалки
// onClickOutside(modalRef, () => {
//   if (props.closeOnOverlayClick && props.modelValue) {
//     closeModal()
//   }
// })

// Закрытие по Escape
const handleKeydown = (event) => {
  if (props.closeOnEsc && event.key === 'Escape' && props.modelValue) {
    closeModal()
  }
}

// Слушатель клавиатуры
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
})

// Блокировка скролла body при открытой модалке
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <teleport to="body">
    <transition name="modal">
      <div 
        v-if="modelValue" 
        class="ui-modal"
        role="dialog"
        aria-modal="true"
      >
        <div 
          class="ui-modal__overlay" 
          @click="closeOnOverlayClick ? closeModal() : null"
        />
        
        <div class="ui-modal__container">
          <div 
            ref="modalRef"
            class="ui-modal__content"
            :class="[`ui-modal__content--${size}`]"
            role="document"
          >
            <button
              v-if="showCloseButton"
              class="ui-modal__close"
              @click="closeModal"
              aria-label="Закрыть"
            >
              <Icon name="mdi:close" size="1.5rem" />
            </button>
            <div class="ui-modal__body">
              <slot />
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<style src="./__ui-modal.scss" lang="scss" />