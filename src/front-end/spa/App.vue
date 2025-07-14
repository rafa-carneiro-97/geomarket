<template>
    <RouterView v-slot="{ Component, route }">
        <transition name="v" mode="out-in">
            <component :is="Component" :key="route.path" />
        </transition>
    </RouterView>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ScrollSmoother, ScrollToPlugin } from 'gsap/all'

gsap.registerPlugin(ScrollTrigger, ScrollSmoother, ScrollToPlugin)

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
    transition: opacity 1s;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
