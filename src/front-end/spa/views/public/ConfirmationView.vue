<template>
    <main
        class="flex min-h-dvh flex-col items-center justify-center overflow-hidden bg-gray-100 py-6"
    >
        <div class="absolute bottom-1/2 z-0 h-dvh w-full bg-green-800/70"></div>

        <div
            class="relative z-10 mx-auto w-11/12 max-w-md items-stretch rounded bg-white p-6 shadow shadow-black/20"
        >
            <p class="text-center text-xl text-pretty">
                {{ props.message || 'Clique em continuar' }}
            </p>

            <RouterLink :to="link" class="btn btn-blue mx-auto mt-6"> Continuar </RouterLink>
        </div>
    </main>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { RouterLink, type RouteLocationRaw } from 'vue-router'
import { employeeStore } from '@/stores/employee'

const props = defineProps<{
    redirect?: string
    message?: string
}>()

const employee = employeeStore()

const link = computed<RouteLocationRaw>(() => {
    if (props.redirect) return props.redirect

    if (employee.establishment.id !== null) {
        return { name: 'dashboard', params: { establishmentId: employee.establishment.id } }
    }

    return { name: 'login' }
})
</script>
