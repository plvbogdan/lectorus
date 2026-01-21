<script setup>
    const props = defineProps({
        title: {
            type: String,
            default: ''
        }
    })
</script>

<template>
    <div class="auth">
        <div class="auth__section">
            <div class="auth__wrap">
                <h1 class="auth__title" v-html="title" />
                <slot />
            </div>
        </div>
    </div>
</template>

<style src="./__auth.scss" lang="scss" />