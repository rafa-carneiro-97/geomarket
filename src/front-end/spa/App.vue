<template>
    <component v-if="route.meta.renderMenu !== false" :is="menuComponent" id="dynamicMenu" />

    <RouterView v-slot="{ Component, route }">
        <Transition name="content" mode="out-in">
            <component :is="Component" :key="route.path" />
        </Transition>
    </RouterView>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'

const PublicMenu = defineAsyncComponent(() => import('@/components/menu/PublicMenu.vue'))
const PrivateMenu = defineAsyncComponent(() => import('@/components/menu/PrivateMenu.vue'))
const route = useRoute()

const menuComponent = computed(() => {
    return route.meta.requiresAuth === true ? PrivateMenu : PublicMenu
})
</script>

<style lang="css">
.content-enter-active,
.content-leave-active {
    transition: opacity 0.6s;
}

.content-enter-from,
.content-leave-to {
    opacity: 0;
}
</style>
