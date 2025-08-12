<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { computed } from 'vue'

const props = defineProps<{
    error?: string
}>()

const message = computed(() => {
    switch (props.error) {
        case 'Unauthorized':
            return 'Acesso não autorizado.'

        case 'Invalid token':
            return 'Seu token de acesso foi inválidado.'

        case 'Token expired':
            return 'Seu token de acesso expirou.'

        default:
            return ''
    }
})
</script>

<template>
    <div class="flex min-h-dvh flex-col items-center justify-center bg-orange-300 p-4">
        <h1 class="text-center">
            <span class="text-shadow text-8xl font-bold text-white">401</span>
            <span v-if="props.error" class="block text-3xl font-bold text-orange-800">
                {{ props.error }}
            </span>
        </h1>

        <p class="text-shadow my-20 max-w-lg text-center text-2xl font-bold text-pretty text-white">
            <span v-if="message" class="text-2xl font-bold">
                {{ message }}
            </span>
            Por favor, faça o login.
        </p>

        <RouterLink :to="{ name: 'login' }" class="btn btn-red"> Página de login </RouterLink>
    </div>
</template>
