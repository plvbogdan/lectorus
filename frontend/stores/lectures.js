const config = useRuntimeConfig()
const apiBase = config.public.apiBase

export const useLecturesStore = defineStore('lectures', {
  state: () => ({
    isLoading: false,
    lectures: [],
    currentLecture: null
  }),

  getters: {
    getLectures: (state) => state.lectures,
    getCurrentLecture: (state) => state.currentLecture,
    getIsLoading: (state) => state.isLoading
  },

  actions: {
    async fetchLectures() {
      this.isLoading = true;
      try {
        const response = await fetch(`${apiBase}/lectures`)
        const data = await response.json()
        this.lectures = data
      } catch (error) {
        console.error('Ошибка при загрузке лекций:', error)
      } finally {
        this.isLoading = false
      }
    },

    async createLecture(formData) {
      this.isLoading = true
      try {
        const tokenCookie = useCookie('auth_token')
        const token = tokenCookie.value
        
        const response = await fetch(`${apiBase}/lectures/create`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })

        const newLecture = await response.json()
        this.lectures.push(newLecture.data)
        return newLecture
      } catch (error) {
        console.error('Ошибка при создании лекции:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchLectureById(id) {
      this.isLoading = true
      try {
        const response = await fetch(`${apiBase}/lectures/${id}`)

        if (!response.ok) {
          throw new Error(`Лекция с id ${id} не найдена`)
        }

        const data = await response.json()
        this.currentLecture = data

        return this.currentLecture
      } catch (error) {
        console.error('Ошибка при загрузке лекции:', error)
        this.currentLecture = null
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deleteLecture(id) {
      this.isLoading = true
      try {
        const tokenCookie = useCookie('auth_token')
        const token = tokenCookie.value
        
        const response = await fetch(`${apiBase}/lectures/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) {
          throw new Error(`Ошибка при удалении лекции: ${response.status}`)
        }

        // Удаляем лекцию из списка
        this.lectures = this.lectures.filter(lecture => lecture.id !== id)
        
        return true
      } catch (error) {
        console.error('Ошибка при удалении лекции:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    }
  }
})