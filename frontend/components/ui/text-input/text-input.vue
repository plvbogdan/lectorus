<!-- components/ui/UITextInput.vue -->
<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'tel', 'url'].includes(value)
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'focus', 'blur'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleBlur = (event) => {
  emit('blur', event)
}
</script>

<template>
  <div class="ui-text-input">
    <label v-if="label" class="ui-text-input__label">
      {{ label }}
      <span v-if="required" class="ui-text-input__required">*</span>
    </label>
    
    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      class="ui-text-input__input"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
    />
    
    <div v-if="error" class="ui-text-input__error">
      <Icon name="mdi:alert-circle" size="1rem" />
      <span>{{ error }}</span>
    </div>
    
    <div v-if="$slots.hint" class="ui-text-input__hint">
      <slot name="hint" />
    </div>
  </div>
</template>

<style lang="scss">
.ui-text-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  
  &__label {
    font-weight: 500;
    color: var(--color-dark-80);
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  
  &__required {
    color: var(--color-red);
  }
  
  &__input {
    padding: 0.75rem 1rem;
    border: 1px solid var(--color-border);
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
    background: var(--color-white);
    transition: all 0.2s ease;
    width: 100%;
    
    &:focus {
      outline: none;
      border-color: var(--color-blue);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    &:disabled {
      background: var(--color-background);
      cursor: not-allowed;
      opacity: 0.7;
    }
    
    &::placeholder {
      color: var(--color-dark-48);
    }
  }
  
  &__error {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--color-red);
    font-size: 0.875rem;
    margin-top: 0.25rem;
  }
  
  &__hint {
    font-size: 0.875rem;
    color: var(--color-dark-64);
    margin-top: 0.25rem;
  }
  
  // Размеры
  &--sm &__input {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
  
  &--lg &__input {
    padding: 1rem 1.25rem;
    font-size: 1.125rem;
  }
}

// Модификатор для состояния с ошибкой
// .ui-text-input.has-error &__input {
//   border-color: var(--color-red);
  
//   &:focus {
//     box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
//   }
// }
</style>