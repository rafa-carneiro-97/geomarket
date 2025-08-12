<template>
    <div>
        <main>
            <section class="flex min-h-dvh flex-col items-center justify-center">
                <h1>Tittle</h1>
                <BaseAlert :status="AlertStatus.Error" message="Qualquer" class="mt-4" />
                <BaseAlert :status="AlertStatus.Info" message="Qualquer" class="mt-4" />
                <BaseAlert :status="AlertStatus.Warning" message="Qualquer" class="mt-4" />
                <BaseAlert :status="AlertStatus.Success" message="Qualquer" class="mt-4" />
            </section>
            <!-- <BarcodeReader @code="console.log" /> -->
        </main>
    </div>
</template>

<script setup lang="ts">
import env from 'env'
import BaseAlert, { AlertStatus } from '@/components/BaseAlert.vue'
// import BarcodeReader from '@/components/barcode/BarcodeReader.vue'

console.log('Node ENV: ', env.DEBUG)
console.log('Type ENV: ', typeof env.DEBUG)
</script>
