<script setup>
  const authStore = useAuthStore()

// Проверяем авторизацию один раз при загрузке приложения
  const { data: authData } = await useAsyncData('auth', async () => {
    if (process.client) {
      await authStore.checkAuth()
    }
  });
</script>
  
  <template>
    <div>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </div>
  </template>
