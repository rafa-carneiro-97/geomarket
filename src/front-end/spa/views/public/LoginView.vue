<template>
    <div>
        <main>
            <section class="flex min-h-dvh flex-col items-center justify-center pb-4">
                <form
                    @submit.prevent="login"
                    aria-label="Formulário para realizar o login"
                    class="mx-auto mt-4 flex w-11/12 max-w-4xl flex-row overflow-hidden rounded-md border border-black/20 shadow shadow-black/10"
                    novalidate
                >
                    <div class="flex w-full flex-col content-between p-8">
                        <h1 class="font-serif text-4xl font-bold">Login</h1>

                        <BaseAlert
                            v-if="alert.message"
                            :status="AlertStatus.Error"
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
                                v-model="formData.email"
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
                                v-model="formData.password"
                                @input="delete formErrors.password"
                                required
                            />

                            <FieldError
                                v-if="formErrors.password"
                                :message="formErrors.password[0]"
                            />
                        </div>

                        <!-- Stay connected -->
                        <div class="checkbox mt-6">
                            <label>
                                <input type="checkbox" v-model="formData.stayConnected" />
                                Permanecer conectado
                            </label>
                        </div>

                        <div class="flex flex-1 items-center justify-center">
                            <button type="submit" class="btn btn-blue mx-auto mt-8">
                                <TextLoading text="Acessar" :isLoading="isLoading" />
                            </button>
                        </div>
                    </div>

                    <img
                        src="@/assets/public/login/security.webp"
                        alt=" Ilustração vetorial sobre dados pessoais ou cibersegurança"
                        class="hidden w-5/12 self-stretch border-l border-black/10 object-cover object-center md:block"
                    />
                </form>

                <a href="#" class="mt-8">Esqueceu sua senha?</a>
            </section>
        </main>
    </div>
</template>

<script lang="ts" setup>
import { ref, onBeforeMount } from 'vue'
import { authStore } from '@/stores/auth'
import router from '@/router'
import BaseAlert, { AlertStatus } from '@/components/BaseAlert.vue'
import FieldError from '@/components/form/FieldError.vue'
import TextLoading from '@/components/loading/TextLoading.vue'

const auth = authStore()

const isLoading = ref<boolean>(false)

const alert = ref({
    message: '',
    key: 0,
})

const formData = ref({
    email: 'funcionario@gmail.com',
    password: '1234asdf1',
    stayConnected: false,
})

const formErrors = ref<{
    email?: string[]
    password?: string[]
}>({})

onBeforeMount(() => {
    if (auth.token != '') {
        router.replace({ name: 'dashboard' })
    }
})

function login() {
    isLoading.value = true
    formErrors.value = {}
    alert.value.message = ''
    alert.value.key++

    auth.login({
        username: formData.value.email,
        password: formData.value.password,
        stayConnected: formData.value.stayConnected,
    })
        .then(() => {
            console.clear()
            location.reload()
        })
        .catch((error) => {
            isLoading.value = false

            if (error.code === 'ERR_NETWORK') {
                alert.value.message = 'Sua conexão não está estável, por favor, tente mais tarde.'
                alert.value.key++
                return
            }

            if (error.status === 400) {
                const responseErros = error.response.data.errors

                if (responseErros.__all__) {
                    alert.value.message = responseErros.__all__[0]
                    alert.value.key++
                }

                formErrors.value = {
                    password: responseErros.password || undefined,
                    email: responseErros.username || undefined,
                }

                return
            }

            alert.value.message =
                'Erro inesperado ao enviar os dados, por favor, contacte a nossa equipe.'
            alert.value.key++
        })
}
</script>
