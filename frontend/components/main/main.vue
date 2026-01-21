<script setup>
    const authStore = useAuthStore();
    const lectureStore = useLecturesStore();
    const lectures = computed(() => lectureStore.getLectures);
    const user = computed(() => authStore.getUser);

    onMounted( async () => {
        await lectureStore.fetchLectures();
        await authStore.checkAuth();
    })

    watch(lectures, val => console.log(val))
    watch(user, val => console.log(val))
    
</script>

<template>
    <div class="main flex --direction-column --gap-32">
        <h1 class="main__title center-wrap">Список лекций</h1>
        <div class="main__placeholder" v-if="lectures.length === 0">Тут ничего нет:(</div>
        <div class="main__lectures">
            
            <LectureCard v-for="item, index in lectures" :key="index" :item="item" /> 
        </div>
    </div>
    <ModalCreate />
</template>

<style src="./__main.scss" lang="scss" />