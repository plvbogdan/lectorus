<script setup>
const route = useRoute()
const lecturesStore = useLecturesStore()

const id = computed(() => Number(route.params.slug))

const { data: lecture, pending, error } = await useAsyncData(
  () => `lecture-${id.value}`,
  () => lecturesStore.fetchLectureById(id.value)
)


useHead(() => ({
  title: lecture.value?.name ?? 'Загрузка...',
  meta: lecture.value
    ? [
        { name: 'description', content: lecture.value.name },
        { name: 'keywords', content: lecture.value.name }
      ]
    : []
}))
</script>

<template>
	<Lecture :content="lecture.lecture" :title="lecture.name"/>
</template>