<script setup>
    import { NuxtLink } from '#components'
    
    const props = defineProps({
        to: String,
        href: String,
    })

    const component = computed(() => {
        if (props.to) {
            return NuxtLink;
        } else if (props.href) {
            return 'a';
        } else return 'button';
    })
</script>

<template>
    <component :is="component" :to="to" :href="href" class="ui-button">
        <div class="ui-button__inner">
            <slot name="prefix"></slot>
            <slot></slot>
            <slot name="sufix"></slot>
        </div>
    </component>
</template>

<style src="./__ui-button.scss" lang="scss" />