<template>
    <div aria-label="Menu suspenso">
        <button
            aria-label="Exibir menu suspenso"
            type="button"
            class="flex w-full cursor-pointer flex-row items-center px-3 py-3 hover:text-white"
            :class="[isOpen ? 'text-white' : 'text-white/70']"
            @click="toggle"
        >
            <span class="ml-2 flex-1 text-left">
                {{ label }}
            </span>

            <ChevronRight
                class="mr-1 transition-transform duration-400"
                :class="{ 'rotate-90': isOpen }"
            />
        </button>

        <ol
            ref="dropdown"
            class="overflow-hidden bg-teal-950 transition-all duration-400"
            :style="[isOpen ? `height: ${listHeight}px` : 'height: 0px']"
        >
            <li v-for="(item, index) in props.links" :key="index">
                <RouterLink
                    v-slot="{ isExactActive }"
                    :to="item.location"
                    class="block no-underline"
                >
                    <div
                        class="group flex flex-row items-center px-6 py-2 no-underline transition-all hover:bg-black/20 hover:text-white"
                        :class="{
                            'cursor-default bg-black/20 text-white': isExactActive,
                            'cursor-pointer text-white/70': !isExactActive,
                        }"
                    >
                        <span class="ml-2 flex-1 overflow-x-hidden font-medium text-nowrap">
                            {{ item.text }}
                        </span>

                        <span v-if="isExactActive" class="size-2 rounded-full bg-yellow-300"></span>
                    </div>
                </RouterLink>
            </li>
        </ol>
    </div>
</template>

<script lang="ts" setup>
import { ref, useTemplateRef } from 'vue'
import { RouterLink, type RouteLocationRaw } from 'vue-router'
import { type LucideIcon, ChevronRight } from 'lucide-vue-next'

const props = defineProps<{
    label: string
    icon: LucideIcon
    links: Array<{ text: string; location: RouteLocationRaw }>
}>()

const dropdown = useTemplateRef('dropdown')
const isOpen = ref<boolean>(false)
const listHeight = ref(0)

function toggle() {
    isOpen.value = !isOpen.value
    listHeight.value = dropdown.value?.scrollHeight ?? 40
}
</script>

<style scoped>
div:has(a[aria-current='page']) {
    & > button svg {
        stroke: #ffff1a;
    }
}
</style>
