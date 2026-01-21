<script setup>
    const lecturesStore = useLecturesStore();
    const authStore = useAuthStore();
    const props = defineProps({
        item: {
            type: Object,
            default: {}
        },
        mayDelete: {
            type: Boolean,
            default: false,
        }
    })

    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
        })
    }

    const handleDelete = async () => {
        await lecturesStore.deleteLecture(props.item.id)
        await authStore.checkAuth();
    }
</script>

<template>
    <div class="lecture-card flex --direction-column --just-space --gap-24">
        <NuxtLink :to="`/lectures/${item.id}/`" class="lecture-card__link" />
        <div class="lecture-card__head flex --just-space --gap-24">
            <div class="lecture-card__head-wrap flex --direction-column --gap-8">
                <div class="lecture-card__title" v-if="item.name" v-html="item.name"></div>
                <div class="lecture-card__author" v-if="item.author_firstname || item.author_lastname" v-html="item.author_lastname + ' ' +item.author_firstname"></div>
                <div class="lecture-card__group" v-if="item.group" v-html="item.group"></div>
            </div>
            <div class="lecture-card__delete" v-if="mayDelete" @click="handleDelete">
                <Icon name="mingcute:delete-line" size="2rem" />
            </div>
            <div class="lecture-card__btn" v-else>
                <Icon name="eva:diagonal-arrow-right-up-fill" size="2rem" />
            </div>
        </div>
        <div class="lecture-card__footer flex --just-space --gap-24">
            <div class="lecture-card__chapters" v-if="item.chapters_count">
                К-во глав: <span v-html="item.chapters_count"></span>
            </div>
            <div class="lecture-card__wrap flex --align-center --gap-8 --just-space">
                <!-- <UiTag v-if="item.group" :title="item.group" /> -->
                <UiTag v-if="item.topic" :title="item.topic" />
                <UiTag v-if="item.created_at" :title="formatDate(item.created_at)" is-date/>
            </div>
        </div>
    </div>
</template>

<style src="./__lecture-card.scss" lang="scss" />