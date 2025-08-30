<template>
    <div class="relative inline-block min-h-7 min-w-7">
        <LoaderCircle
            v-if="isLoading"
            class="absolute top-1/2 left-1/2 -translate-1/2 animate-spin drop-shadow-xs drop-shadow-black/50"
            :stroke-width="3"
        />

        <span v-if="text" class="text-center" :class="{ invisible: isLoading }">
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
