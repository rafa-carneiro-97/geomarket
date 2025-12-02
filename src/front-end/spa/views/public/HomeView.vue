<template>
    <main>
        <section class="min-h-content flex flex-col items-center justify-center py-6">
            <h1>Tittle</h1>
            <BaseAlert :status="BaseAlertStatus.Error" message="Qualquer" class="mt-4" />
            <BaseAlert :status="BaseAlertStatus.Info" message="Qualquer" class="mt-4" />
            <BaseAlert :status="BaseAlertStatus.Warning" message="Qualquer" class="mt-4" />
            <BaseAlert :status="BaseAlertStatus.Success" message="Qualquer" class="mt-4" />
        </section>
    </main>
</template>

<script setup lang="ts">
import env from 'env'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import { BaseAlertStatus } from '@/types/components/alerts'

console.log('Node ENV: ', env.DEBUG)
console.log('Type ENV: ', typeof env.DEBUG)
</script>
