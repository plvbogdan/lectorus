<script setup>
  const rootStore = useRootStore();
  const authStore = useAuthStore();
  const route = useRoute();
  const router = useRouter();
  const isScrolled = ref(false);
  const handleScroll = () => {
    isScrolled.value = window.scrollY > 10
  }

  const isAccount = computed(() => route.path === '/me/')

  const isAuth = computed(() => authStore.getIsAuthenticated);
  const user = computed(() => authStore.getUser);

  const logout = async () => {
    authStore.clearAuth();
    await router.push('/signin/')
  }

  watch(isAuth, (val) => console.log(val));

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
    handleScroll();
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
</script>

<template>
  <div class="header" :class="{ '--scrolled': isScrolled}">
    <div class="section-wrap">
      <div class="header__inner">
        <NuxtLink to="/" class="header__home">
          <Icon class="header__logo" name="mdi:school" size="3rem" />
        </NuxtLink>
        <div class="account__wrap" v-if="isAuth && user.lastname && user.firstname">
          <div class="header__logout" v-if="isAccount" @click="logout">Выйти</div>
          <UiButton class="header__login --dark" to="/me/" v-else>
            {{ user.lastname + ' ' + user.firstname }}
          </UiButton>
        </div>
        
        <UiButton class="header__login"  v-else to="/signin/">
          Войти
        </UiButton>
      </div>
    </div>
  </div>
</template>

<style src="./__header.scss" lang="scss" />