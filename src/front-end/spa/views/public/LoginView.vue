<template>
    <main>
        <section class="min-h-content flex flex-col items-center justify-center py-6">
            <form
                @submit.prevent="login"
                aria-label="Formulário para realizar o login"
                class="mx-auto flex w-11/12 max-w-4xl flex-row overflow-hidden rounded-md border border-black/20 shadow shadow-black/10"
            >
                <div class="flex w-full flex-col content-between p-8 md:w-7/12">
                    <h1 class="font-serif text-4xl font-bold">Login</h1>

                    <BaseAlert
                        v-if="alert.message"
                        :status="BaseAlertStatus.Error"
                        :message="alert.message"
                        :key="alert.key"
                        class="mt-4"
                    />

                    <!-- Email -->
                    <div class="field" :class="{ 'invalid-field': formErrors.email }">
                        <label for="email">Email:</label>

                        <input
                            id="email"
                            type="text"
                            placeholder=""
                            autocomplete="email"
                            v-model="email"
                            @input="delete formErrors.email"
                            required
                        />

                        <FieldError v-if="formErrors.email" :message="formErrors.email[0]" />
                    </div>

                    <!-- Password -->
                    <div class="field" :class="{ 'invalid-field': formErrors.password }">
                        <label for="password">Senha:</label>

                        <input
                            id="password"
                            type="password"
                            placeholder=""
                            autocomplete="current-password"
                            v-model="password"
                            @input="delete formErrors.password"
                            required
                        />

                        <FieldError v-if="formErrors.password" :message="formErrors.password[0]" />
                    </div>

                    <!-- Stay connected -->
                    <div class="checkbox mt-6">
                        <label>
                            <input type="checkbox" v-model="stayConnected" />
                            Permanecer conectado
                        </label>
                    </div>

                    <div class="flex flex-1 items-center justify-center">
                        <button type="submit" class="btn btn-blue mx-auto mt-4 rounded-full px-6">
                            <TextLoading
                                text="Acessar"
                                :isLoading="isLoading"
                                class="stroke-white"
                            />
                        </button>
                    </div>
                </div>

                <img
                    src="@/assets/public/login/security.webp"
                    alt="Ilustração vetorial sobre dados pessoais ou cibersegurança"
                    class="hidden w-5/12 self-stretch border-l border-black/10 object-cover object-center md:block"
                />
            </form>

            <div class="relative mt-8 w-11/12 max-w-xs">
                <RouterLink :to="{ name: 'user-add' }" class="mx-auto table">
                    Esqueceu sua senha?
                </RouterLink>

                <hr class="mt-6 border border-black/20" />
                <span class="mx-auto -mt-3 table bg-white px-1 text-gray-400">OU</span>

                <RouterLink :to="{ name: 'user-add' }" class="mx-auto mt-2 mb-4 table">
                    Crie uma conta
                </RouterLink>
            </div>
        </section>
    </main>
</template>

<script lang="ts" setup>
import { ref, onBeforeMount } from 'vue'
import { RouterLink } from 'vue-router'
import router from '@/router'
import { authStore } from '@/stores/auth'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import FieldError from '@/components/form/FieldError.vue'
import TextLoading from '@/components/loading/TextLoading.vue'
import { BaseAlertStatus } from '@/types/components/alerts'

onBeforeMount(() => {
    if (auth.token != '') {
        auth.fetchInfo()
            .then((userInfo) => {
                if (userInfo?.isStaff === true) {
                    window.location.href = '/admin/'
                } else {
                    router.replace({ name: 'establishments' })
                }
            })
            .catch((error) => {
                console.error('Error fetching user info:', error)
                setAlertMessage(
                    'Erro ao obter informações do usuário. Por favor, faça login novamente. Caso o problema persista, contacte a nossa equipe.',
                )
                auth.logout()
            })
    }
})

const email = defineModel<string>('email', { default: '', required: true })
const password = defineModel<string>('password', { default: '', required: true })
const stayConnected = defineModel<boolean>('stayConnected', { default: false, required: true })

const auth = authStore()

const isLoading = ref<boolean>(false)

const alert = ref({
    message: '',
    key: 0,
})

const formErrors = ref<{
    email?: string[]
    password?: string[]
}>({})

function setAlertMessage(msg: string) {
    alert.value.message = msg
    alert.value.key++
}

function login() {
    if (isLoading.value) return
    isLoading.value = true
    formErrors.value = {}
    setAlertMessage('')

    auth.login({
        username: email.value,
        password: password.value,
        stayConnected: stayConnected.value,
    })
        .then(() => {
            console.debug('login successful')
            location.reload()
        })
        .catch((error) => {
            isLoading.value = false

            if (error.code === 'ERR_NETWORK') {
                setAlertMessage('Sua conexão está instável, por favor, tente mais tarde.')
                return
            }

            if (error.status === 400) {
                const responseErros = error.response.data.errors

                if (responseErros.__all__) {
                    setAlertMessage(responseErros.__all__[0])
                }

                formErrors.value = {
                    password: responseErros.password || undefined,
                    email: responseErros.username || undefined,
                }

                return
            }

            setAlertMessage(
                'Erro inesperado ao enviar os dados, por favor, contacte a nossa equipe.',
            )
        })
}
</script>
