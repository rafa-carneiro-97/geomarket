<template>
    <main>
        <section class="min-h-content flex flex-col items-center justify-center py-6">
            <form
                @submit.prevent="create"
                aria-label="Formulário para cadastrar uma nova conta"
                class="mx-auto flex w-11/12 max-w-4xl flex-row overflow-hidden rounded-md border border-black/20 shadow shadow-black/10"
                novalidate
            >
                <div class="flex w-full flex-col content-between p-8 md:w-7/12">
                    <h1 class="font-serif text-4xl font-bold">Criar conta</h1>

                    <BaseAlert
                        v-if="alert.message"
                        :status="BaseAlertStatus.Error"
                        :message="alert.message"
                        :key="alert.key"
                        class="mt-4"
                    />

                    <div class="flex flex-col sm:flex-row sm:gap-4">
                        <!-- First name -->
                        <div
                            class="field sm:w-5/12"
                            :class="{ 'invalid-field': formErrors.firstName }"
                        >
                            <label for="firstName">Nome:</label>

                            <input
                                id="firstName"
                                type="text"
                                placeholder=""
                                v-model="firstName"
                                @input="delete formErrors.firstName"
                                required
                            />

                            <FieldError
                                v-if="formErrors.firstName"
                                :message="formErrors.firstName[0]"
                            />
                        </div>

                        <!-- Last name -->
                        <div
                            class="field sm:w-7/12"
                            :class="{ 'invalid-field': formErrors.lastName }"
                        >
                            <label for="lastName">Sobrenome:</label>

                            <input
                                id="lastName"
                                type="text"
                                placeholder=""
                                v-model="lastName"
                                @input="delete formErrors.lastName"
                                required
                            />

                            <FieldError
                                v-if="formErrors.lastName"
                                :message="formErrors.lastName[0]"
                            />
                        </div>
                    </div>

                    <!-- Email1 -->
                    <div class="field" :class="{ 'invalid-field': formErrors.email1 }">
                        <label for="email1">Email:</label>

                        <input
                            id="email1"
                            type="text"
                            placeholder=""
                            autocomplete="email"
                            v-model="email1"
                            @input="delete formErrors.email1"
                            required
                        />

                        <FieldError v-if="formErrors.email1" :message="formErrors.email1[0]" />
                    </div>

                    <!-- Email2 -->
                    <div class="field" :class="{ 'invalid-field': formErrors.email2 }">
                        <label for="email2">Email novamente:</label>

                        <input
                            id="email2"
                            type="text"
                            placeholder=""
                            v-model="email2"
                            @input="delete formErrors.email2"
                            required
                        />

                        <FieldError v-if="formErrors.email2" :message="formErrors.email2[0]" />
                    </div>

                    <!-- Password -->
                    <div class="field" :class="{ 'invalid-field': formErrors.password1 }">
                        <label for="password">Senha:</label>

                        <input
                            id="password1"
                            type="password"
                            placeholder=""
                            autocomplete="off"
                            v-model="password1"
                            @input="delete formErrors.password1"
                            required
                        />

                        <FieldError
                            v-if="formErrors.password1"
                            :message="formErrors.password1[0]"
                        />
                    </div>

                    <!-- Password2 -->
                    <div class="field" :class="{ 'invalid-field': formErrors.password2 }">
                        <label for="password2">Senha novamente:</label>

                        <input
                            id="password2"
                            type="password"
                            placeholder=""
                            autocomplete="off"
                            v-model="password2"
                            @input="delete formErrors.password2"
                            required
                        />

                        <FieldError
                            v-if="formErrors.password2"
                            :message="formErrors.password2[0]"
                        />
                    </div>

                    <div class="mt-6 flex flex-1 items-center justify-center">
                        <button type="submit" class="btn btn-blue mx-auto rounded-full px-6 pt-2.5">
                            <TextLoading text="Criar conta" :isLoading="isLoading" />
                        </button>
                    </div>
                </div>

                <img
                    src="@/assets/public/userCreate/create.webp"
                    alt=" Ilustração vetorial sobre inserção de dados para cadastro"
                    class="hidden w-5/12 self-stretch border-l border-black/10 object-cover object-center md:block"
                />
            </form>

            <div class="relative mt-8 w-11/12 max-w-xs">
                <p class="text-center text-balance">
                    Já possui uma conta?
                    <RouterLink :to="{ name: 'login' }"> Faça o login </RouterLink>
                </p>
            </div>
        </section>
    </main>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import router from '@/router'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import FieldError from '@/components/form/FieldError.vue'
import TextLoading from '@/components/loading/TextLoading.vue'
import { BaseAlertStatus } from '@/types/components/alerts'

const firstName = defineModel<string>('firstName', { required: true })
const lastName = defineModel<string>('lastName', { required: true })
const email1 = defineModel<string>('email1', { required: true })
const email2 = defineModel<string>('email2', { required: true })
const password1 = defineModel<string>('password1', { required: true })
const password2 = defineModel<string>('password2', { required: true })

const alert = ref({
    message: '',
    key: 0,
})

const isLoading = ref<boolean>(false)

const formErrors = ref<{
    firstName?: string[]
    lastName?: string[]
    email1?: string[]
    email2?: string[]
    password1?: string[]
    password2?: string[]
}>({})

function setAlertMessage(msg: string) {
    alert.value.message = msg
    alert.value.key++
}

async function create() {
    isLoading.value = true
    formErrors.value = {}
    setAlertMessage('')

    await axios
        .post(
            '/api/user/form/create',
            {
                first_name: firstName.value,
                last_name: lastName.value,
                email: email1.value,
                email2: email2.value,
                password1: password1.value,
                password2: password2.value,
            },
            {
                withCredentials: true,
            },
        )
        .then(() => {
            router.push({
                name: 'confirmation',
                query: {
                    redirect: router.resolve({ name: 'login' }).path,
                    message:
                        'Usuário criado com sucesso. Por favor, clique abaixo para realizar o login.',
                },
            })
        })
        .catch((error) => {
            isLoading.value = false

            if (error.code === 'ERR_NETWORK') {
                setAlertMessage('Sua conexão está instável, por favor, tente mais tarde.')
                return
            }

            if (error.status === 400) {
                isLoading.value = false
                const responseErros = error.response.data.errors
                console.log(responseErros)

                if (responseErros.__all__) {
                    setAlertMessage(responseErros.__all__[0])
                }

                formErrors.value = {
                    firstName: responseErros.first_name || undefined,
                    lastName: responseErros.last_name || undefined,
                    email1: responseErros.email || undefined,
                    email2: responseErros.email2 || undefined,
                    password1: responseErros.password1 || undefined,
                    password2: responseErros.password2 || undefined,
                }

                return
            }

            setAlertMessage(
                'Erro inesperado ao enviar os dados, por favor, contacte a nossa equipe.',
            )
        })
}
</script>
