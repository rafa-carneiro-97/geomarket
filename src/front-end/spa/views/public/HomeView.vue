<template>
    <main>
        <section class="min-h-content flex flex-col items-center justify-center py-6">
            <h1>Tittle</h1>
            <BaseAlert :status="AlertStatus.Error" message="Qualquer" class="mt-4" />
            <BaseAlert :status="AlertStatus.Info" message="Qualquer" class="mt-4" />
            <BaseAlert :status="AlertStatus.Warning" message="Qualquer" class="mt-4" />
            <BaseAlert :status="AlertStatus.Success" message="Qualquer" class="mt-4" />
        </section>
    </main>
</template>

<script setup lang="ts">
import env from 'env'
import BaseAlert from '@/components/BaseAlert.vue'
import { AlertStatus } from '@/types/components/alert'

console.log('Node ENV: ', env.DEBUG)
console.log('Type ENV: ', typeof env.DEBUG)
</script>
