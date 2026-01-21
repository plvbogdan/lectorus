import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoading: false,
    isAuthenticated: false
  }),

  getters: {
    getUser: (state) => state.user,
    getIsLoading: (state) => state.isLoading,
    getIsAuthenticated: (state) => state.isAuthenticated,
    getAuthToken: () => {
      const tokenCookie = useCookie('auth_token')
      return tokenCookie.value
    }
  },

  actions: {
    async login(credentials) {
      this.isLoading = true
      
      const config = useRuntimeConfig()
      const apiBase = config.public.apiBase
      const formData = new URLSearchParams()
      formData.append('email', credentials.email)
      formData.append('password', credentials.password)
    
      try {
        const response = await fetch(`${apiBase}/auth/signin`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || 'Ошибка авторизации')
        }

        this.setAuthToken(data.access_token, credentials.rememberMe)
        console.log('Авторизация успешна:', data.user)
        if (process.client) {
          const router = useRouter()
          await router.push('/')
        }
        return data
      } catch (error) {
        console.error('Ошибка при авторизации:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      
      const config = useRuntimeConfig()
      const apiBase = config.public.apiBase
      
      const formData = new URLSearchParams()
      formData.append('email', userData.email)
      formData.append('firstname', userData.firstname)
      formData.append('lastname', userData.lastname)
      formData.append('group', userData.group)
      formData.append('password', userData.password)
    
      try {
        const response = await fetch(`${apiBase}/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || 'Ошибка регистрации')
        }

        console.log('Регистрация успешна:', data)
        
        // После успешной регистрации выполняем редирект на страницу логина
        if (process.client) {
          const router = useRouter()
          await router.push('/signin/')
        }
        
        return data
      } catch (error) {
        console.error('Ошибка при регистрации:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Метод для проверки авторизации при загрузке приложения
    async checkAuth() {
      const token = this.getAuthToken
      
      if (!token) {
        this.isAuthenticated = false
        this.user = null
        return false
      }

      this.isLoading = true
      
      try {
        await this.fetchUserInfo()
        this.isAuthenticated = true
        console.log('Пользователь авторизован')
        return true
      } catch (error) {
        console.error('Ошибка при проверке авторизации:', error)
        this.clearAuth()
        return false
      } finally {
        this.isLoading = false
      }
    },

    // Метод для получения информации о пользователе
    async fetchUserInfo() {
      const token = this.getAuthToken
      
      if (!token) {
        throw new Error('Токен отсутствует')
      }

      const config = useRuntimeConfig()
      const apiBase = config.public.apiBase
      
      try {
        const response = await fetch(`${apiBase}/account/me`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          if (response.status === 401) {
            // Токен недействителен
            throw new Error('Недействительный токен')
          }
          throw new Error(`Ошибка сервера: ${response.status}`)
        }

        const userData = await response.json()
        this.isAuthenticated = true
        this.user = userData
        console.log('Информация о пользователе получена:', userData)
        return userData
      } catch (error) {
        console.error('Ошибка при получении информации о пользователе:', error)
        throw error
      }
    },

    // Метод для выхода из системы
    logout() {
      this.clearAuth()
      
      if (process.client) {
        const router = useRouter()
        router.push('/signin/')
      }
    },

    // Метод для очистки данных авторизации
    clearAuth() {
      const tokenCookie = useCookie('auth_token')
      tokenCookie.value = null
      
      this.user = null
      this.isAuthenticated = false
      console.log('Пользователь вышел из системы')
    },

    // Метод для сохранения токена в куки
    setAuthToken(token, rememberMe = false) {
      const tokenCookie = useCookie('auth_token', {
        path: '/',
        sameSite: 'strict',
        secure: process.env.NODE_ENV === 'production',
        maxAge: rememberMe ? 60 * 60 * 24 * 30 : undefined // 30 дней если rememberMe, иначе сессия
      })
      
      tokenCookie.value = token
      console.log('Токен сохранен в куки')
    }
  }
})