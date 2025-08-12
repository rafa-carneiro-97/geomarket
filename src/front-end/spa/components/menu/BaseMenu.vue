<template>
    <div class="menu-height">
        <header
            ref="header"
            aria-label="Main menu"
            class="hover: fixed top-0 right-0 z-60 w-full border-b border-black/5 shadow shadow-black/20 transition-all duration-600 ease-in-out hover:shadow-md"
            :class="[!isOpen ? 'menu-height bg-white' : 'h-dvh bg-teal-950/30']"
            @click="handleHeader"
        >
            <button
                @click="toggle"
                type="button"
                aria-label="Hamburguer do menu"
                class="ml-auto table h-full cursor-pointer p-2"
            >
                <div class="h-full w-8">
                    <span
                        class="block h-1 shadow-black/10 transition-all duration-600"
                        :class="[isOpen ? 'mt-4 rotate-225 bg-white shadow-xs' : 'bg-slate-600']"
                    ></span>

                    <span
                        class="block h-1 bg-black shadow-black/10 transition-all duration-600"
                        :class="[
                            isOpen ? '-mt-1 -rotate-45 bg-white shadow-xs' : 'mt-2 bg-slate-700',
                        ]"
                    ></span>

                    <span
                        class="block h-1 bg-black transition-all duration-600"
                        :class="[isOpen ? '-mt-1 -rotate-45 bg-white' : 'mt-2 bg-slate-700']"
                    ></span>
                </div>
            </button>

            <nav
                class="absolute top-0 right-0 -z-1 min-h-dvh overflow-hidden bg-teal-950 pt-6 shadow-md shadow-black/15 transition-[width] duration-500"
                :class="[isOpen ? 'h-full w-64' : 'h-0 w-0']"
            >
                <div class="w-full">
                    <h2 class="py-8 text-center text-4xl text-nowrap text-white">LOGO</h2>

                    <nav class="space-y-2 pb-4">
                        <slot name="nav">
                            <MenuItem
                                v-for="(item, index) in items"
                                :key="index"
                                :text="item.text"
                                :location="item.location"
                                :icon="item.icon"
                                :class="item.addClass || 'stroke-white'"
                                @click="toggle"
                            ></MenuItem>
                        </slot>
                    </nav>
                </div>
            </nav>
        </header>
    </div>
</template>

<script lang="ts" setup>
// https://code.market/product/vue-js-tailawind-css-admin-panel-sidebar-navigation
import { ref, useTemplateRef } from 'vue'
// import { MapPinHouse } from 'lucide-vue-next'
import { RouteLocationRaw } from 'vue-router'
import { LucideIcon } from 'lucide-vue-next'
import MenuItem from '@/components/menu/MenuItem.vue'

defineProps<{
    items: Array<{
        text: string
        location: RouteLocationRaw
        icon: LucideIcon
        addClass?: string
    }>
}>()

const isOpen = ref<boolean>(false)
const header = useTemplateRef<HTMLElement>('header')

function toggle() {
    isOpen.value = !isOpen.value
}

function handleHeader(event: MouseEvent) {
    if (event.target === header.value) {
        if (isOpen.value) toggle()
    }
}
</script>
