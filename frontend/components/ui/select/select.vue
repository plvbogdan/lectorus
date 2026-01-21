<!-- components/ui/UISelect.vue -->
<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Выберите вариант'
  },
  options: {
    type: Array,
    default: () => []
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
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const handleChange = (event) => {
  const value = event.target.value
  emit('update:modelValue', value)
  emit('change', value)
}
</script>

<template>
  <div class="ui-select" :class="[`ui-select--${size}`]">
    <label v-if="label" class="ui-select__label">
      {{ label }}
      <span v-if="required" class="ui-select__required">*</span>
    </label>
    
    <div class="ui-select__wrapper">
      <select
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="ui-select__select"
        @change="handleChange"
      >
        <option value="" disabled>
          {{ placeholder }}
        </option>
        <option
          v-for="(option, index) in options"
          :key="index"
          :value="option.value || option.id || option"
          :selected="modelValue === (option.value || option.id || option)"
        >
          {{ option.label || option.name || option }}
        </option>
      </select>
      <Icon name="mdi:chevron-down" class="ui-select__chevron" />
    </div>
    
    <div v-if="error" class="ui-select__error">
      <Icon name="mdi:alert-circle" size="16" />
      <span>{{ error }}</span>
    </div>
    
    <div v-if="$slots.hint" class="ui-select__hint">
      <slot name="hint" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.ui-select {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  position: relative;
  
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
  
  &__wrapper {
    position: relative;
    width: 100%;
  }
  
  &__select {
    width: 100%;
    padding: 0.75rem 1rem;
    padding-right: 2.5rem;
    border: 1px solid var(--color-border);
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
    background: var(--color-white);
    transition: all 0.2s ease;
    appearance: none;
    cursor: pointer;
    
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
  }
  
  &__chevron {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
    color: var(--color-dark-64);
    font-size: 1.25rem;
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
  &--sm &__select {
    padding: 0.5rem 0.75rem;
    padding-right: 2rem;
    font-size: 0.875rem;
  }
  
  &--lg &__select {
    padding: 1rem 1.25rem;
    padding-right: 3rem;
    font-size: 1.125rem;
  }
}

// .ui-select.has-error &__select {
//   border-color: var(--color-red);
  
//   &:focus {
//     box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
//   }
// }
</style>