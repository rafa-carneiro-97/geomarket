<template>
    <main>
        <section class="py-6">
            <div class="mx-auto w-11/12 max-w-xl overflow-hidden rounded shadow shadow-black/30">
                <h1
                    class="text-shadow flex flex-row items-center justify-center bg-blue-600 px-4 py-6 text-center font-serif text-2xl font-bold text-pretty text-white"
                >
                    Escolha o estabeleciomento
                </h1>

                <ul class="divide-y divide-gray-300">
                    <li
                        class="p-5"
                        v-if="shops.length === 0"
                        :class="{ 'text-orange-600': isLoading, 'text-gray-700': !isLoading }"
                    >
                        <TextLoading
                            text="Não há estabelecimentos vinculados a sua conta. Contacte uma loja parceira ou entre em contato com a nossa equipe para saber mais."
                            :isLoading="isLoading"
                            class="mx-auto table text-center text-pretty"
                        />
                    </li>

                    <li
                        v-for="(item, index) in shops"
                        :key="index"
                        class="flex flex-col items-center p-5 sm:flex-row"
                    >
                        <div class="ml-5">
                            <h2 class="text-center text-2xl font-bold text-pretty sm:text-left">
                                {{ item.name }}
                            </h2>
                            <p class="line-clamp-2 break-normal hyphens-auto">
                                Lorem ipsum dolor sit amet consectetur adipisicing elit. Quia nam
                                ipsam hic odio, quidem eaque numquam molestiae ab officia, iste quos
                                molestias exercitationem dicta omnis? Quidem esse cumque soluta
                                quibusdam!
                            </p>
                        </div>

                        <RouterLink
                            :to="{ name: 'dashboard', params: { establishmentId: item.id } }"
                            class="btn btn-orange mt-3 rounded sm:mt-0 sm:ml-4"
                        >
                            Acessar
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </section>
    </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import TextLoading from '@/components/loading/TextLoading.vue'
import { breadcrumbsStore } from '@/stores/breadcrumbs'

const isLoading = ref<boolean>(true)
const shops = ref<Array<Shop>>([])
const breadcrumbs = breadcrumbsStore()

interface Shop {
    id: number
    name: string
}

breadcrumbs.reset()

axios
    .get('/api/establishments/list')
    .then((response) => {
        shops.value = response.data
    })
    .finally(() => (isLoading.value = false))
</script>
