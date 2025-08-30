<template>
    <RouterLink
        v-slot="{ isExactActive }"
        :to="location"
        :aria-current="isCurrent() ? 'page' : null"
        class="block no-underline"
    >
        <div
            class="group mx-3 flex flex-row items-center rounded-md px-3 py-2 transition-all hover:bg-white/10 hover:text-white"
            :class="{
                'cursor-default bg-white/10 text-white': isExactActive,
                'cursor-pointer text-white/70': !isExactActive,
            }"
        >
            <component
                :is="icon"
                :size="24"
                :stroke-width="1.5"
                class="stroke-inherit group-hover:opacity-100"
                :class="{ 'opacity-70': !isExactActive }"
            />
            <span class="ml-2 flex-1 overflow-x-hidden font-medium text-nowrap"> {{ label }} </span>

            <span v-if="isExactActive" class="size-2 rounded-full bg-yellow-300"></span>
        </div>
    </RouterLink>
</template>

<script setup lang="ts">
import { useRoute, RouterLink, type RouteLocationRaw } from 'vue-router'
import { type LucideIcon } from 'lucide-vue-next'

const route = useRoute()
const isCurrent = () => route.path === location.pathname

defineProps<{
    label: string
    location: RouteLocationRaw
    icon: LucideIcon
}>()
</script>
