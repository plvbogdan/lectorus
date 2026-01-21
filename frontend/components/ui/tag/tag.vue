<script setup>
    const props = defineProps({
        title: {
            type: String,
            default: ''
        },
        isDate: {
            type: Boolean,
            default: false
        }
    })
</script>

<template>
    <div class="ui-tag">
        {{ !isDate ? '#' : '' }}
        <Icon v-if="isDate" name="solar:calendar-bold" size="1.2rem" />
        {{ title }}
    </div>
</template>

<style src="./__ui-tag.scss" lang="scss" />