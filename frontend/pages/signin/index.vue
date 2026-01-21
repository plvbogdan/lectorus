<script setup>
const authStore = useAuthStore();

const formData = ref({
    email: '',
    password: '',
    rememberMe: false,
})

const formErrors = ref({
    email: '',
    password: ''
})

const isFormValid = computed(() => !formErrors.value.email && !formErrors.value.password && formData.value.email && formData.value.password);

const handleSubmit = async () => {
    formErrors.value.email = validateField('email', formData.value.email)
    formErrors.value.password = validateField('password', formData.value.password)
    
    if (formErrors.value.email || formErrors.value.password) {
        return
    }

    console.log('Данные для авторизации:', formData.value);
    await authStore.login(formData.value);

}

const validateField = (field, value) => {
    switch (field) {
        case 'email':
            if (!value) return 'Email обязателен'
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Введите корректный email'
            return ''
        case 'password':
            if (!value) return 'Пароль обязателен'
            if (value.length < 6) return 'Пароль должен содержать минимум 6 символов'
            return ''
        default:
            return ''
    }
}
</script>

<template>
    <Auth title="Авторизация">
        <form
            @submit.prevent="handleSubmit"
            class="auth__form"
        >
            <!-- Email -->
            <UiTextInput
                v-model="formData.email"
                label="Email"
                type="email"
                placeholder="Введите ваш email"
                :required="true"
                :error="formErrors.email"
                @input="formErrors.email = validateField('email', formData.email)"
            />
            
            <!-- Password -->
            <UiTextInput
                v-model="formData.password"
                label="Пароль"
                type="password"
                placeholder="Введите ваш пароль"
                :required="true"
                :error="formErrors.password"
                @input="formErrors.password = validateField('password', formData.password)"
            />
            
            <!-- Дополнительные опции -->
       
            <label class="auth__remember">
                <input type="checkbox" v-model="formData.rememberMe">
                Запомнить меня
            </label>
            
            <!-- Кнопка отправки -->
            <UiButton
                type="submit"
                class="auth__submit"
                :disabled="!isFormValid"
                :class="{'disabled': !isFormValid}"
            >
                Войти
            </UiButton>
            
            <!-- Ссылка на регистрацию -->
            <div class="auth__footer">
                <p>Нет аккаунта? <NuxtLink to="/signup/" class="auth__footer-link">Зарегистрироваться</NuxtLink></p>
            </div>
        </form>
    </Auth>
</template>