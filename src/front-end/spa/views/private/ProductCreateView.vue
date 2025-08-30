<template>
    <main>
        <section class="min-h-content bg-gray-100 py-6">
            <BreadcrumbsNav />

            <form
                class="mx-auto w-11/12 max-w-md overflow-hidden rounded-md border border-black/15 bg-white pb-6 shadow shadow-black/10"
            >
                <h1 class="mx-4 pt-8 text-center text-3xl font-bold text-green-950">
                    Adicionar produto
                </h1>

                <div class="px-6">
                    <!-- Barcode -->
                    <div class="field">
                        <label for="barcode">Código de barra</label>
                        <div class="flex items-center justify-start">
                            <input
                                id="barcode"
                                type="text"
                                placeholder=""
                                autocomplete="off"
                                required
                            />
                            <BarcodeReader @code="console.log" />
                        </div>
                    </div>

                    <!-- Name -->
                    <div class="field">
                        <label for="name">Nome</label>
                        <input id="name" type="text" placeholder="" autocomplete="off" required />
                    </div>
                </div>

                <button type="submit" class="btn btn-green mx-auto mt-8 rounded-full px-6">
                    <TextLoading text="Adicionar" :isLoading="isLoading" />
                </button>
            </form>
        </section>
    </main>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Cherry } from 'lucide-vue-next'
import axios from 'axios'
import { employeeStore } from '@/stores/employee'
import { breadcrumbsStore } from '@/stores/breadcrumbs'
import BreadcrumbsNav from '@/components/breadcrumbs/BreadcrumbsNav.vue'
import BarcodeReader from '@/components/barcode/BarcodeReader.vue'
import TextLoading from '@/components/loading/TextLoading.vue'

const breadcrumbs = breadcrumbsStore()

breadcrumbs.push({
    icon: Cherry,
    label: 'adicionar produto',
})

const isLoading = ref<boolean>(false)
</script>
