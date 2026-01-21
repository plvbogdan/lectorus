<script setup>
    const rootStore = useRootStore();
    const authStore = useAuthStore();
    const user = computed(() => authStore.getUser);
    const lectures = computed(() => user.value.lectures);
    const isAuth = computed(() => authStore.getIsAuthenticated);

    watch(user, val => console.log(val))
    
    const openModal = () => {
        rootStore.setModal('add');
    }
</script>

<template>
    <div class="account flex --direction-column --gap-32" v-if="isAuth">
        <div class="account__head flex --just-space --direction-column">
            <h1 class="account__title center-wrap">Ваш список лекций, <br>{{ user.firstname}}</h1>
            <!-- <UiButton class="account__add" @click="openModal">
                +
            </UiButton> -->
        </div>
        
        <div class="account__placeholder" v-if="lectures.length === 0">Тут ничего нет:(</div>
        <div class="account__lectures">
            <LectureCard v-for="item, index in lectures" :key="index" :item="item" may-delete/> 
            <div class="account__add" @click="openModal">
                +
            </div>
        </div>
    </div>
    <ModalCreate />
</template>

<style src="./__account.scss" lang="scss" />