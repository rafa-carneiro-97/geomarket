<template>
    <section
        v-if="!isHidden"
        class="fixed top-0 left-0 z-90 h-dvh w-dvw overflow-auto bg-black/80 py-12"
    >
        <div class="mx-auto w-11/12 max-w-sm rounded bg-white">
            <button type="button" @click="isHidden = true" class="ml-auto block">
                <X
                    :size="36"
                    :strokeWidth="2"
                    aria-label="Fechar"
                    class="boder-l ml-auto cursor-pointer stroke-gray-400 p-1 hover:stroke-black"
                />
            </button>

            <hr class="h-px bg-gray-200" />

            <div class="p-3 pb-6">
                <h2 class="text-center font-serif text-xl font-bold text-balance">
                    Adicionar produto
                    <span v-if="barcode">#{{ barcode }}</span>
                </h2>

                <BarcodeForm
                    ref="barcode-form"
                    @product="(v) => (product = v)"
                    @barcode="(v) => (barcode = v)"
                />

                <ProductForm
                    @product="addGondolaProduct"
                    ref="product-form"
                    v-if="product === null"
                    :barcode="barcode as string"
                    class="h-0 overflow-hidden"
                />

                <div ref="product-view" v-if="product" class="relative h-0 overflow-hidden">
                    <img
                        v-if="product.photoUrl"
                        :src="product.photoUrl"
                        alt="Foto do produto"
                        class="mt-4 w-full border border-black/10"
                    />

                    <div
                        v-else
                        class="mt-4 flex aspect-square items-center justify-center border border-black/10 bg-gray-200"
                    >
                        <Image :stroke-width="1" class="size-1/2 stroke-gray-300" />
                    </div>

                    <dl>
                        <dt>Nome</dt>
                        <dd class="indent-4">{{ product.name }}</dd>

                        <dt>Palavras-chave</dt>
                        <dd>
                            <ul class="flex flex-row flex-wrap gap-2">
                                <li v-for="keyword in product.keywords" :key="keyword">
                                    <span
                                        class="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800"
                                    >
                                        {{ keyword }}
                                    </span>
                                </li>

                                <li v-if="product.keywords.length === 0">
                                    <p class="indent-4 text-gray-500">-</p>
                                </li>
                            </ul>
                        </dd>
                    </dl>

                    <p
                        v-if="!product.isActive"
                        class="mt-4 rounded border border-red-500 bg-red-100 p-2 text-center text-red-700"
                    >
                        Este produto está em processo de avaliação. Ele não será exibido para os
                        clientes enquanto o processo não é finalizado.
                    </p>

                    <button
                        type="button"
                        @click="addGondolaProduct(product)"
                        class="btn btn-blue mx-auto mt-5"
                    >
                        Adicionar
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { ref, watch, useTemplateRef, nextTick } from 'vue'
import { gsap } from 'gsap'
import { Image, X } from 'lucide-vue-next'
import ProductForm from '@/components/gondola/forms/ProductForm.vue'
import BarcodeForm from '@/components/gondola/forms/BarcodeForm.vue'
import type { ProductInterface } from '@/types/entities/product'
import type { GondolaProductInterface } from '@/types/entities/gondola'

const props = defineProps({
    xPosition: {
        type: Number,
        required: true,
    },

    yPosition: {
        type: Number,
        required: true,
    },
})

const emit = defineEmits<{
    (e: 'addGondolaProduct', value: GondolaProductInterface): void
}>()

const barcode = ref<string>('')
const product = ref<ProductInterface | undefined | null>(undefined)
const isHidden = ref<boolean>(false)
const barcodeForm = useTemplateRef('barcode-form')
const productView = useTemplateRef('product-view')
const productForm = useTemplateRef('product-form')

watch(product, (newValue) => {
    if (newValue !== undefined && newValue !== null) {
        hideBarcodeForm(showProductView)
        return
    }

    if (newValue === null) {
        hideBarcodeForm(showProductForm)
        return
    }
})

function addGondolaProduct(product: ProductInterface) {
    const gondolaProduct = {
        gondola: {
            xPosition: props.xPosition,
            yPosition: props.yPosition,
        },
        product: product,
    }

    emit('addGondolaProduct', gondolaProduct)
    isHidden.value = true
}

async function hideBarcodeForm(onComplete?: () => void) {
    await nextTick()
    gsap.to(barcodeForm.value?.$el, {
        duration: 0.5,
        opacity: 0,
        height: 0,
        marginTop: 0,
        marginBottom: 0,
        onComplete: () => {
            if (onComplete) onComplete()
        },
    })
}

function showProductView() {
    gsap.to(productView.value, {
        duration: 0.5,
        opacity: 1,
        height: 'auto',
    })
}

function showProductForm() {
    gsap.to(productForm.value?.$el, {
        duration: 0.5,
        opacity: 1,
        height: 'auto',
    })
}
</script>
