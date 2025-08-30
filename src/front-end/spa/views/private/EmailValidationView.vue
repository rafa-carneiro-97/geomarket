<template>
    <main class="flex min-h-dvh flex-col items-center justify-center bg-gray-100">
        <div
            class="mx-auto w-11/12 max-w-md overflow-hidden rounded bg-white p-6 shadow shadow-black/20"
        >
            <div class="mx-auto table rounded-full border border-black/10 bg-yellow-100 p-4">
                <MailQuestionMark :size="36" class="stroke-yellow-700" />
            </div>

            <h1 class="mt-4 text-center text-xl font-semibold">Vericação de email</h1>

            <p class="mt-4 text-center text-gray-600">
                Por favor, insira o código de verificação que enviamos para
                <strong class="font-bold text-gray-800">{{ userInfo?.email }}</strong>
            </p>

            <BaseAlert
                v-if="alert.message"
                :status="alert.status"
                :message="alert.message"
                :key="alert.key"
                class="mt-4"
            />

            <div class="mx-auto mt-4 flex flex-row items-center justify-center gap-2">
                <input
                    v-for="(digit, index) in code"
                    :key="index"
                    type="text"
                    maxlength="1"
                    class="h-10 w-7 rounded-md border border-gray-400 text-center focus:ring-2 focus:ring-sky-500"
                    v-model="code[index]"
                    @input="handleInput(index, $event)"
                    @keydown="handleKeyboard(index, $event)"
                />
            </div>

            <button
                disabled
                type="button"
                ref="confirmButton"
                class="btn btn-blue mx-auto mt-6 rounded-full px-6"
                @click="submit()"
            >
                <TextLoading text="Confirmar" :isLoading="isLoadingConfirm" />
            </button>
        </div>

        <div class="relative mt-8 w-11/12 max-w-xs">
            <p>
                Clique
                <TextLoading
                    text="aqui"
                    :isLoading="isLoadingSendEmail"
                    class="cursor-pointer text-blue-700 underline"
                    @click="sendEmail()"
                />
                para enviar o email novamente
            </p>

            <hr class="mt-6 border border-black/20" />
            <span class="mx-auto -mt-3 table bg-gray-100 px-1 text-gray-400">OU</span>

            <RouterLink :to="{ name: 'logout' }" class="mx-auto mt-2 mb-4 table"> Sair </RouterLink>
        </div>
    </main>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref, useTemplateRef } from 'vue'
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { MailQuestionMark } from 'lucide-vue-next'
import { authStore } from '@/stores/auth'
import router from '@/router'
import TextLoading from '@/components/loading/TextLoading.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import { AlertStatus } from '@/types/components/alert'

onBeforeMount(async () => {
    await auth.fetchInfo()
    if (auth.userInfo?.isEmailVerified === true) {
        router.push({ name: 'establishments' })
    }
})

const auth = authStore()

const { userInfo } = storeToRefs(auth)
const code = ref<Array<string>>(['', '', '', '', '', ''])
const isLoadingSendEmail = ref<boolean>(false)
const isLoadingConfirm = ref<boolean>(false)
const confirmButton = useTemplateRef<HTMLButtonElement>('confirmButton')

const alert = ref({
    message: '',
    key: 0,
    status: AlertStatus.Error,
})

function setAlertMessage(msg: string, status: AlertStatus) {
    alert.value = {
        message: msg,
        key: alert.value.key++,
        status: status,
    }
}

function handleInput(index: number, event: Event) {
    const input = event.target as HTMLInputElement
    const nextInput = input.nextElementSibling as HTMLInputElement | null
    nextInput?.focus()

    const joinedCode = code.value.join('')
    if (!confirmButton.value) return

    confirmButton.value.disabled = joinedCode.length !== 6
}

function handleKeyboard(index: number, event: KeyboardEvent) {
    const input = event.target as HTMLInputElement

    switch (event.key) {
        case 'Backspace': {
            event.preventDefault()

            if (input.value !== '') {
                code.value[index] = ''
            } else {
                if (index > 0) code.value[index - 1] = ''
                const prevInput = input.previousElementSibling as HTMLInputElement | null
                prevInput?.focus()
            }
            break
        }

        case 'Delete': {
            event.preventDefault()
            code.value[index] = ''
            const nextInput = input.nextElementSibling as HTMLInputElement | null
            nextInput?.focus()
            break
        }

        case 'ArrowRight': {
            event.preventDefault()
            const nextInput = input.nextElementSibling as HTMLInputElement | null
            nextInput?.focus()
            break
        }

        case 'ArrowLeft': {
            event.preventDefault()
            const prevInput = input.previousElementSibling as HTMLInputElement | null
            prevInput?.focus()
            break
        }

        default: {
            code.value[index] = ''
        }
    }
}

async function submit() {
    if (isLoadingConfirm.value === true) return

    isLoadingConfirm.value = true
    axios
        .post('/api/email/verify', {
            code: code.value.join(''),
        })
        .then((response) => {
            if (response.status === 209) {
                setAlertMessage('Código inválido, tente novamente.', AlertStatus.Error)
                isLoadingConfirm.value = false
                return
            }

            auth.userInfo = null
            router.push({ name: 'establishments' })
        })
}

async function sendEmail() {
    if (isLoadingSendEmail.value === true) return
    isLoadingSendEmail.value = true

    axios
        .get('/api/email/verification/send')
        .then((response) => {
            if (response.status === 409) {
                router.push({ name: 'establishments' })
            }

            if (response.status === 204) {
                setAlertMessage(
                    'Você alcançou o limite de envios de email, aguarde 24 horas para terntar novamente. Recomendamos entrar em contato com a nossa equipe.',
                    AlertStatus.Error,
                )
                isLoadingSendEmail.value = false
                return
            }
        })
        .finally(() => (isLoadingSendEmail.value = false))
}
sendEmail()
</script>
