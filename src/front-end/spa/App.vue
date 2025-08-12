<template>
    <component v-if="route.meta.renderMenu !== false" :is="menu" />

    <RouterView v-slot="{ Component, route }">
        <transition name="v" mode="out-in">
            <component :is="Component" :key="route.path" />
        </transition>
    </RouterView>
</template>

<script setup lang="ts">
import { ref, watch, computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import { gsap } from 'gsap'
import { ScrollTrigger, ScrollSmoother, ScrollToPlugin, MorphSVGPlugin } from 'gsap/all'

const route = useRoute()

const menu = computed(() => {
    if (route.meta.requiresAuth === true) {
        return defineAsyncComponent(() => import('@/components/menu/PrivateMenu.vue'))
    }

    return defineAsyncComponent(() => import('@/components/menu/PublicMenu.vue'))
})

gsap.registerPlugin(ScrollTrigger, ScrollSmoother, ScrollToPlugin, MorphSVGPlugin)

const previousScrollHeight = ref(document.body.scrollHeight)

watch(previousScrollHeight, () => {
    // Refresh all scroll triggers
    ScrollTrigger.getAll().forEach((item) => {
        item.refresh()
    })
})
</script>

<style lang="css">
.v-enter-active,
.v-leave-active {
    transition: opacity 0.8s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
