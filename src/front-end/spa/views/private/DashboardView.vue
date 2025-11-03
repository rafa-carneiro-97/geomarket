<template>
    <main>
        <section class="min-h-content bg-gray-100 py-6">
            <BreadcrumbsNav />

            <RouterLink :to="{ name: 'confirmation' }">Confirmar</RouterLink>

            <div class="mx-auto w-11/12 max-w-4xl">
                <div v-if="establishmentInfo" class="text-center">
                    <h1 class="font-serif text-5xl font-bold">{{ establishmentInfo.name }}</h1>
                    <p>{{ establishmentInfo.address }}</p>
                </div>

                <div class="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3">
                    <div class="overflow-hidden rounded bg-white shadow shadow-black/20">
                        <div class="bg-gray-800 p-3">
                            <h2
                                class="flex h-16 items-center justify-center text-center text-xl font-semibold text-balance text-white"
                            >
                                Funcionários e Administradores
                            </h2>
                        </div>

                        <div class="mx-auto max-w-2xs p-2">
                            <canvas ref="employee-canvas"></canvas>

                            <div class="mt-3 grid grid-cols-2 gap-3">
                                <RouterLink
                                    :to="{ name: 'employee-add' }"
                                    class="btn btn-green flex items-center rounded px-2 py-1"
                                >
                                    <Plus
                                        class="drop-shadow-xs drop-shadow-black/50"
                                        :stroke-width="2"
                                        :size="20"
                                    />

                                    <span class="ml-0.5 flex-1 text-center"> Adicionar </span>
                                </RouterLink>

                                <RouterLink
                                    :to="{ name: 'employee-add' }"
                                    class="btn flex items-center rounded bg-gray-700 px-2 py-1"
                                >
                                    <Search :stroke-width="2" :size="20" />

                                    <span class="ml-0.5 flex-1 text-center"> Procurar </span>
                                </RouterLink>
                            </div>
                        </div>
                    </div>

                    <div class="overflow-hidden rounded bg-white shadow shadow-black/20">
                        <div class="bg-indigo-800 p-3">
                            <h2
                                class="flex h-16 items-center justify-center text-center text-xl font-semibold text-balance text-white"
                            >
                                Produtos
                            </h2>
                        </div>

                        <div class="mx-auto max-w-2xs p-2">
                            <canvas ref="product-canvas"></canvas>

                            <div class="mt-3 grid grid-cols-2 gap-3">
                                <RouterLink
                                    :to="{ name: 'product-add' }"
                                    class="btn btn-green flex items-center rounded px-2 py-1"
                                >
                                    <Plus
                                        class="drop-shadow-xs drop-shadow-black/50"
                                        :stroke-width="2"
                                        :size="20"
                                    />

                                    <span class="ml-0.5 flex-1 text-center"> Adicionar </span>
                                </RouterLink>

                                <button
                                    type="button"
                                    class="btn flex items-center rounded bg-indigo-800 px-2 py-1 text-white"
                                >
                                    <Search
                                        class="drop-shadow-xs drop-shadow-black/50"
                                        :stroke-width="2"
                                        :size="20"
                                    />
                                    <span class="ml-0.5 flex-1 text-center"> Procurar </span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
</template>

<script lang="ts" setup>
import { ref, onBeforeMount, useTemplateRef, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Plus, Search } from 'lucide-vue-next'
import axios from 'axios'
import { Chart } from 'chart.js'
import { employeeStore } from '@/stores/employee'
import { breadcrumbsStore } from '@/stores/breadcrumbs'
import BreadcrumbsNav from '@/components/breadcrumbs/BreadcrumbsNav.vue'
import { EstablishmentInfo } from '@/types/stores/employee'

const props = defineProps<{ establishmentId: number }>()

const employee = employeeStore()
const breadcrumbs = breadcrumbsStore()
const employeeCanvas = useTemplateRef('employee-canvas')
const productCanvas = useTemplateRef('product-canvas')
const establishmentInfo = ref<EstablishmentInfo | null>()
let employeeChart = null as Chart | null
let productChart = null as Chart | null

onBeforeMount(() => {
    employee.reset()
    employee.establishment.id = Number(props.establishmentId)

    employee.getEstablishmentInfo().then((data) => {
        establishmentInfo.value = data as EstablishmentInfo

        breadcrumbs.push({
            label: establishmentInfo.value?.name,
        })

        axios
            .get(`/api/establishment/${employee.establishment.id}/dashboard/data`)
            .then((response) => {
                console.log(response.data)
            })
    })
})

onMounted(() => {
    employeeChart = new Chart(employeeCanvas.value as HTMLCanvasElement, {
        type: 'pie',
        data: {
            labels: ['Administradores', 'Funcionários'],
            datasets: [
                {
                    data: [4, 32],
                    backgroundColor: ['#1e2838', '#c77134'],
                    hoverOffset: 3,
                },
            ],
        },
    })

    productChart = new Chart(productCanvas.value as HTMLCanvasElement, {
        type: 'doughnut',
        data: {
            labels: ['nas gôndolas', 'em falta'],
            datasets: [
                {
                    data: [122, 12],
                    backgroundColor: ['#3629ab', '#d6ba3e'],
                    hoverOffset: 3,
                },
            ],
        },
    })
})

onUnmounted(() => {
    setTimeout(() => {
        employeeChart?.destroy()
        employeeChart = null
        productChart?.destroy()
        productChart = null
    }, 2000) // 2 seconds
})
</script>
