<script setup>
const authStore = useAuthStore();

const formData = ref({
    email: '',
    firstname: '',
    lastname: '',
    group: '',
    password: '',
    confirmPassword: ''
})

const formErrors = ref({
    email: '',
    firstname: '',
    lastname: '',
    group: '',
    password: '',
    confirmPassword: ''
})

const isFormValid = computed(() => {
    return !formErrors.value.email && 
           !formErrors.value.firstname && 
           !formErrors.value.lastname && 
           !formErrors.value.group && 
           !formErrors.value.password && 
           !formErrors.value.confirmPassword &&
           formData.value.email && 
           formData.value.firstname && 
           formData.value.lastname && 
           formData.value.group && 
           formData.value.password && 
           formData.value.confirmPassword;
});

const handleSubmit = async () => {
    formErrors.value.email = validateField('email', formData.value.email)
    formErrors.value.firstname = validateField('firstname', formData.value.firstname)
    formErrors.value.lastname = validateField('lastname', formData.value.lastname)
    formErrors.value.group = validateField('group', formData.value.group)
    formErrors.value.password = validateField('password', formData.value.password)
    formErrors.value.confirmPassword = validateField('confirmPassword', formData.value.confirmPassword)
    
    if (formData.value.password !== formData.value.confirmPassword) {
        formErrors.value.confirmPassword = 'Пароли не совпадают'
    }
    
    if (formErrors.value.email || formErrors.value.firstname || formErrors.value.lastname || formErrors.value.group || formErrors.value.password || formErrors.value.confirmPassword) {
        return
    }

    console.log('Данные для регистрации:', formData.value);
    
    const registrationData = {
        email: formData.value.email,
        firstname: formData.value.firstname,
        lastname: formData.value.lastname,
        group: formData.value.group,
        password: formData.value.password
    };
    
    try {
        await authStore.register(registrationData);
        console.log(registrationData);
    } catch (error) {
        console.error('Ошибка регистрации:', error);
    }
}

const validateField = (field, value) => {
    switch (field) {
        case 'email':
            if (!value) return 'Email обязателен'
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Введите корректный email'
            if (value.length > 100) return 'Email не должен превышать 100 символов'
            return ''
        case 'firstname':
            if (!value) return 'Имя обязательно'
            if (value.length < 1) return 'Имя должно содержать хотя бы 1 символ'
            if (value.length > 100) return 'Имя не должно превышать 100 символов'
            return ''
        case 'lastname':
            if (!value) return 'Фамилия обязательна'
            if (value.length < 1) return 'Фамилия должна содержать хотя бы 1 символ'
            if (value.length > 100) return 'Фамилия не должна превышать 100 символов'
            return ''
        case 'group':
            if (!value) return 'Группа обязательна'
            if (value.length < 1) return 'Группа должна содержать хотя бы 1 символ'
            if (value.length > 100) return 'Группа не должна превышать 100 символов'
            return ''
        case 'password':
            if (!value) return 'Пароль обязателен'
            if (value.length < 8) return 'Пароль должен содержать минимум 8 символов'
            return ''
        case 'confirmPassword':
            if (!value) return 'Подтверждение пароля обязательно'
            return ''
        default:
            return ''
    }
}
</script>

<template>
    <Auth title="Регистрация" class="signup">
        <form
            @submit.prevent="handleSubmit"
            class="auth__form "
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

            
            <!-- Группа -->
            <UiTextInput
                v-model="formData.group"
                label="Группа"
                placeholder="Введите вашу группу"
                :required="true"
                :error="formErrors.group"
                @input="formErrors.group = validateField('group', formData.group)"
            />
            
            <!-- Имя -->
            <UiTextInput
                v-model="formData.firstname"
                label="Имя"
                placeholder="Введите ваше имя"
                :required="true"
                :error="formErrors.firstname"
                @input="formErrors.firstname = validateField('firstname', formData.firstname)"
            />
            
            <!-- Фамилия -->
            <UiTextInput
                v-model="formData.lastname"
                label="Фамилия"
                placeholder="Введите вашу фамилию"
                :required="true"
                :error="formErrors.lastname"
                @input="formErrors.lastname = validateField('lastname', formData.lastname)"
            />
        
            
            <!-- Пароль -->
            <UiTextInput
                v-model="formData.password"
                label="Пароль"
                type="password"
                placeholder="Введите пароль"
                :required="true"
                :error="formErrors.password"
                @input="formErrors.password = validateField('password', formData.password)"
            />
            
            <!-- Подтверждение пароля -->
            <UiTextInput
                v-model="formData.confirmPassword"
                label="Подтверждение пароля"
                type="password"
                placeholder="Повторите пароль"
                :required="true"
                :error="formErrors.confirmPassword"
                @input="formErrors.confirmPassword = validateField('confirmPassword', formData.confirmPassword)"
            />
            
            <!-- Кнопка отправки -->
            <UiButton
                type="submit"
                class="auth__submit"
                :disabled="!isFormValid"
                :class="{'disabled': !isFormValid}"
            >
                Зарегистрироваться
            </UiButton>

            <!-- Ссылка на авторизацию -->
            <div class="auth__footer">
                <p>Уже есть аккаунт? <NuxtLink to="/signin/" class="auth__footer-link">Войти</NuxtLink></p>
            </div>

        </form>
    </Auth>
</template>