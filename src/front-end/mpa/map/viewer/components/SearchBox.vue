<template>
    <div
        class="fixed h-dvh w-full max-w-sm overflow-x-hidden bg-white shadow shadow-black/20"
        style="z-index: 500"
    >
        <div
            class="flex flex-col items-center justify-center"
            style="height: 70px; transition: box-shadow 160ms ease"
            :style="{ 'box-shadow': `0 4px 12px rgba(0,0,0,${shadowOpacity})` }"
        >
            <div
                class="flex w-11/12 max-w-xs flex-row justify-stretch rounded-full border border-black/10 shadow shadow-black/10"
            >
                <input
                    type="text"
                    maxlength="40"
                    placeholder="Pesquise aqui"
                    class="w-full py-2 pl-6"
                />

                <div class="flex items-center pr-3 pl-2">
                    <LoaderCircle
                        :size="20"
                        :stroke-width="3"
                        class="animate-spin stroke-blue-600"
                    />
                </div>

                <button type="button" aria-label="Pesquisar" class="group cursor-pointer pr-3 pl-2">
                    <Search :size="20" class="stroke-gray-400 group-hover:stroke-blue-600" />
                </button>

                <button type="button" aria-label="Fechar" class="group cursor-pointer pr-3">
                    <X :size="20" class="stroke-gray-400 group-hover:stroke-red-700" />
                </button>
            </div>
        </div>

        <div
            ref="scrollbar"
            @scroll.passive="onScroll"
            class="scrollbar overflow-y-auto"
            style="height: calc(100dvh - 70px)"
        >
            <h2 class="px-4 font-sans text-2xl font-medium">Resultados</h2>

            <ol>
                <li
                    v-for="(item, index) in searchResult"
                    :key="index"
                    class="flex cursor-pointer flex-row items-center justify-center border-b border-black/10 py-3 pr-4 pl-6 transition-all hover:bg-gray-100"
                >
                    <dl class="flex-1">
                        <dt class="text-lg font-medium text-black">Leite Grande</dt>

                        <dd class="mt-2 flex flex-row items-center">
                            <RulerDimensionLine :size="24" :stroke-width="1" />
                            <span class="ml-1 text-sm text-gray-600"> 2,3 metros </span>
                        </dd>
                    </dl>

                    <div class="size-20 rounded bg-gray-400"></div>
                </li>
            </ol>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { LoaderCircle, RulerDimensionLine, Search, X } from 'lucide-vue-next'
import axios from 'axios'
import { ref, onMounted, useTemplateRef } from 'vue'

const searchResult = ref<Array<number>>([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
const scrollbar = useTemplateRef('scrollbar')
const shadowOpacity = ref(0)

function onScroll() {
    const SHADOW_LIMIT = 120
    const MAX_OPACITY = 0.35

    const scrollbarElmt = scrollbar.value
    if (!scrollbarElmt) {
        shadowOpacity.value = 0
        return
    }

    const top = scrollbarElmt.scrollTop || 0
    const ratio = Math.min(top / SHADOW_LIMIT, 1)
    shadowOpacity.value = Math.round(ratio * MAX_OPACITY * 1000) / 1000
}

onMounted(() => {
    // initialize
    onScroll()
})
</script>

<style scoped>
.scrollbar {
    /* Firefox */
    @-moz-document url-prefix() {
        scrollbar-width: thin;
        scrollbar-color: #a7a7a7 #e7e7e7;
    }

    /* Chrome */
    &::-webkit-scrollbar-track {
        background-color: #e7e7e7;
    }

    &::-webkit-scrollbar {
        width: 8px;
        background-color: #f5f5f5;
    }

    &::-webkit-scrollbar-thumb {
        background-color: #a7a7a7;
    }
}

.scrollbar::-webkit-scrollbar-button {
    display: none;
}
</style>
