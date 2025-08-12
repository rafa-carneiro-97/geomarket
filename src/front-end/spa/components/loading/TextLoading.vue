<template>
    <div class="relative inline-flex min-h-7 min-w-7 items-center justify-center">
        <LoaderCircle
            v-if="isLoading"
            class="absolute top-1/2 left-1/2 -translate-1/2 animate-spin"
            :stroke-width="3"
        />

        <span v-if="text" :class="{ invisible: isLoading }">
            {{ text }}
        </span>
    </div>
</template>

<script lang="ts" setup>
import { LoaderCircle } from 'lucide-vue-next'

defineProps<{
    text?: string
    isLoading: boolean
}>()
</script>
