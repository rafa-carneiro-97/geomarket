<template>
    <RouterLink
        v-if="!isLast"
        :to="link"
        class="ml-1 inline-flex h-full items-center text-gray-700 no-underline transition-all hover:scale-105 hover:text-blue-700 hover:underline"
        :aria-current="isLast ? 'page' : undefined"
        @click.prevent="emit('activate')"
    >
        <component v-if="icon" :is="icon" :size="18" :stroke-width="1.6" />

        <span class="ml-1"> {{ label }} </span>

        <ChevronRight :size="20" :stroke-width="1.5" class="ml-1" />
    </RouterLink>

    <div
        v-else
        class="inline-flex h-full items-center text-black"
        :aria-current="isLast ? 'page' : undefined"
    >
        <span class="font-bold">
            {{ label }}
        </span>
    </div>
</template>

<script lang="ts" setup>
import { RouterLink, type RouteLocationRaw } from 'vue-router'
import { type LucideIcon, ChevronRight } from 'lucide-vue-next'

defineProps<{
    icon?: LucideIcon
    label: string
    link: RouteLocationRaw
    isLast: boolean
}>()

const emit = defineEmits<{
    activate: []
}>()
</script>
