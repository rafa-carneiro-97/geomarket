<template>
    <main>
        <section class="min-h-content bg-gray-100 py-6">
            <BreadcrumbsNav />

            <div
                class="shadow-blacl/20 mx-auto mt-6 w-11/12 max-w-md overflow-hidden rounded border border-black/15 bg-white px-6 py-4 shadow"
            >
                <h1 class="mt-1 mb-4 text-center text-2xl font-bold">Adicionar funcionário</h1>

                <BaseAlert
                    :status="AlertStatus.Info"
                    message="Para adicionar o funcionário, primeiramente, ele precisa ter uma conta com email verificado. Dessa forma, basta adicioná-lo através do email dele logo abaixo."
                />

                <!-- Email -->
                <div class="field mt-0">
                    <label for="email">Email:</label>
                    <input
                        id="email"
                        type="text"
                        placeholder=""
                        autocomplete="email"
                        v-model="email"
                        required
                    />
                </div>

                <button type="button" class="btn btn-green mx-auto mt-4">
                    <TextLoading text="Adicionar" :isLoading="isLoading" />
                </button>
            </div>
        </section>
    </main>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue'
import axios from 'axios'
import TextLoading from '@/components/loading/TextLoading.vue'
import { breadcrumbsStore } from '@/stores/breadcrumbs'
import { employeeStore } from '@/stores/employee'
import BreadcrumbsNav from '@/components/breadcrumbs/BreadcrumbsNav.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import { AlertStatus } from '@/types/components/alert'

const props = defineProps<{ establishmentId: number }>()
const isLoading = ref<boolean>(false)
const employee = employeeStore()
const breadcrumbs = breadcrumbsStore()
const email = defineModel<string>('email', { required: true })

onBeforeMount(() => {
    breadcrumbs.push({
        label: 'Adicionar funcionário',
    })

    employee.reset()
    employee.establishment.id = Number(props.establishmentId)
})
</script>
