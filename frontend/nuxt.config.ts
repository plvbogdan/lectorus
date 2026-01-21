// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    'nuxt-icon'
  ],
  ssr: false,
  css: [
    '~/assets/scss/main.scss'
  ],
  app: {
    loadingIndicator: {
      name: 'default',
      color: '#3b82f6',
      background: '#ffffff'
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
      siteName: 'Lectorus'
    }
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true }
})
