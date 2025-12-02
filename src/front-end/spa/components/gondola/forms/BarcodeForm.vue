<template>
    <form @submit.prevent="handleSubmit()" class="overflow-hidden">
        <BaseAlert
            v-if="alert.message"
            :status="BaseAlertStatus.Error"
            :message="alert.message"
            :key="alert.key"
            class="mt-4"
        />

        <div class="field mx-auto max-w-2xs">
            <label for="barcode">Código de barra</label>
            <div class="flex items-center justify-start">
                <input
                    id="barcode"
                    type="text"
                    placeholder=""
                    autocomplete="off"
                    v-model="barcode"
                    spellcheck="false"
                    required
                    :disabled="isLoading"
                    @keydown="barcodeInputActions($event)"
                />
                <BarcodeReader @code="setBarcode" v-if="!isLoading" />
            </div>

            <FieldError v-if="formErrors.barcode" :message="formErrors.barcode[0]" />
        </div>

        <button type="submit" class="btn btn-gray mx-auto mt-4 rounded-full px-6">
            <TextLoading text="Procurar" :isLoading="isLoading" class="stroke-white" />
        </button>
    </form>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'
import BarcodeReader from '@/components/camera/barcode/BarcodeReader.vue'
import FieldError from '@/components/form/FieldError.vue'
import TextLoading from '@/components/loading/TextLoading.vue'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import type { ProductInterface } from '@/types/entities/product'
import { BaseAlertStatus } from '@/types/components/alerts'

const emit = defineEmits<{
    (e: 'product', value: ProductInterface | null): void
    (e: 'barcode', value: string): void
}>()

const barcode = defineModel({ required: false })
const isLoading = ref<boolean>(false)
const formErrors = ref<{
    barcode?: string[]
}>({})
const alert = ref({
    message: '',
    key: 0,
})

function setAlertMessage(msg: string) {
    alert.value.message = msg
    alert.value.key++
}

function setBarcode(value: string) {
    barcode.value = value
    handleSubmit()
}

function barcodeInputActions(event: KeyboardEvent) {
    switch (event.key) {
        case 'Enter':
            event.preventDefault()
            handleSubmit()
            break
    }
}

async function handleSubmit() {
    if (isLoading.value) return

    isLoading.value = true
    const code = barcode.value as string

    await axios
        .get(`/api/product/${code}/get`)
        .then((response) => {
            emit('barcode', code)

            // It does not exist
            if (response.status === 204) {
                emit('product', null)
                return
            }

            emit('product', response.data)
        })
        .catch((error) => {
            console.log(error)

            if (error.status === 404) {
                setAlertMessage('Código de barras não identificado, por favor, contacte a equipe.')
                return
            }

            setAlertMessage(
                `Não foi possível realizar a pesquisa, por favor, entre em contato com a equipe. Erro: ${error}`,
            )
        })
}
</script>
