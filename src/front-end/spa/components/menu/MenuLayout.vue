<template>
    <header
        aria-label="Main menu"
        class="menu-height sticky top-0 right-0 z-60 w-full border-b border-black/5 bg-white shadow shadow-black/20 transition-all duration-600 ease-in-out hover:shadow-md"
    >
        <button
            @click="toggle"
            type="button"
            aria-label="Hamburguer do menu"
            class="menu-height absolute top-0 right-0 z-60 table cursor-pointer p-2"
        >
            <div class="h-full w-8">
                <span
                    class="block h-1 shadow-black/10 transition-all duration-600"
                    :class="[
                        isOpen
                            ? 'mt-3 rotate-225 bg-white shadow-xs'
                            : 'bg-slate-700 delay-400 sm:delay-1000',
                    ]"
                ></span>

                <span
                    class="block h-1 bg-black shadow-black/10 transition-all duration-500"
                    :class="[
                        isOpen
                            ? '-mt-1 -rotate-45 bg-white shadow-xs'
                            : 'mt-1.5 bg-slate-700 delay-400 sm:delay-1000',
                    ]"
                ></span>

                <span
                    class="block h-1 bg-black transition-all duration-600"
                    :class="[
                        isOpen
                            ? '-mt-1 -rotate-45 bg-white'
                            : 'mt-1.5 bg-slate-700 delay-400 sm:delay-1000',
                    ]"
                ></span>
            </div>
        </button>

        <div
            class="fixed top-0 right-0 flex h-dvh flex-row bg-teal-700 shadow-xl shadow-black/20 transition-all delay-200 duration-1000 will-change-[height,background]"
            :class="[isOpen ? 'sm:w-full' : 'sm:w-0']"
        >
            <div
                ref="container"
                @click="handleContainer"
                class="hidden flex-1 flex-col items-center justify-center overflow-hidden p-2 sm:flex"
            >
                <img src="@/assets/logo.svg" alt="Logo" class="w-56 min-w-56" />
                <h3 class="text-center text-4xl font-bold text-white">Geomarket</h3>
            </div>

            <div
                class="ml-auto flex h-full flex-col overflow-x-hidden overflow-y-visible bg-teal-900 pt-6 shadow-md shadow-black/20 transition-[width] duration-600"
                :class="[isOpen ? 'w-dvw sm:w-64' : 'w-0']"
            >
                <h2 class="py-6 text-center font-serif text-3xl text-nowrap text-white">MENU</h2>

                <nav class="flex-1 space-y-1">
                    <slot name="nav"></slot>
                </nav>

                <div class="mx-auto mt-12 table p-2 sm:hidden">
                    <img src="@/assets/logo.svg" alt="Logo" class="w-40 min-w-40" />
                    <h3 class="text-center text-2xl font-bold text-white">Geomarket</h3>
                </div>
            </div>
        </div>
    </header>
</template>

<script lang="ts" setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { ref, useTemplateRef } from 'vue'

const route = useRoute()
const isOpen = ref<boolean>(false)
const container = useTemplateRef<HTMLElement>('container')

watch(
    () => route.path,
    () => (isOpen.value = false),
)

function toggle() {
    isOpen.value = !isOpen.value
}

function handleContainer() {
    if (isOpen.value) isOpen.value = false
}
</script>
