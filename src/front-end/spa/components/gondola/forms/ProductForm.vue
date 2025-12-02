<template>
    <form @submit.prevent="handleSubmit()">
        <BaseAlert
            :status="BaseAlertStatus.Info"
            message="Esse código de barra ainda não está cadastrado no sistema, por favor, insira os dados abaixo para iniciar o processo de análise."
            class="mt-4"
        />

        <BaseAlert
            :status="BaseAlertStatus.Warning"
            message="Lembrado que o produto só será exibido para os cliente após a finalização  do processo."
            class="mt-4"
        />

        <BaseAlert
            v-if="alert.message"
            :status="BaseAlertStatus.Error"
            :message="alert.message"
            :key="alert.key"
            class="mt-4"
        />

        <div class="px-2">
            <!-- Name -->
            <div class="field">
                <label for="name">Nome do produto:</label>

                <input
                    id="name"
                    type="text"
                    placeholder=""
                    autocomplete="nome do produto"
                    v-model="name"
                    required
                />
            </div>

            <FieldError v-if="formErrors.name" :message="formErrors.name[0]" />

            <button type="submit" class="btn btn-blue mx-auto mt-4 rounded-full px-6">
                <TextLoading text="Cadastrar" :isLoading="isLoading" class="stroke-white" />
            </button>
        </div>
    </form>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import TextLoading from '@/components/loading/TextLoading.vue'
import FieldError from '@/components/form/FieldError.vue'
import { BaseAlertStatus } from '@/types/components/alerts'
import type { ProductInterface } from '@/types/entities/product'

const props = defineProps({
    barcode: {
        type: String,
        required: true,
    },
})

const emit = defineEmits<{
    (e: 'product', value: ProductInterface): void
}>()

const isLoading = ref<boolean>(false)
const name = defineModel<string>()
const alert = ref({
    message: '',
    key: 0,
})
const formErrors = ref<{
    name?: string[]
    barcode?: string[]
}>({})

function setAlertMessage(msg: string) {
    alert.value.message = msg
    alert.value.key++
}

async function handleSubmit() {
    if (isLoading.value) return
    isLoading.value = true
    formErrors.value = {}
    setAlertMessage('')

    axios
        .post(`/api/product/create`, {
            barcode: props.barcode,
            name: name.value,
        })
        .then((response) => {
            if (response.status === 201) {
                emit('product', response.data)
                return
            }

            isLoading.value = false
            setAlertMessage(`Erro inpesperado no servidor. Por favor, contacte a equipe. `)
            console.error(response)
        })
        .catch((error) => {
            isLoading.value = false
            console.error(error)

            if (error.status === 400) {
                const responseErros = error.response.data.errors

                if (responseErros.__all__) {
                    setAlertMessage(responseErros.__all__[0])
                }

                formErrors.value = {
                    name: responseErros.name || undefined,
                    barcode: responseErros.barcode || undefined,
                }

                return
            }

            console.error(error)
            setAlertMessage(
                `Erro ao tentar criar o produto. Por favor, contacte a equipe. Erro: ${error}.`,
            )
        })
}
</script>
