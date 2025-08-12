<template>
    <div ref="select" :aria-label="label" class="relative">
        <span
            class="px-1 text-xs leading-none tracking-tight text-balance"
            :class="{ 'font-bold text-blue-600': !isHidden }"
        >
            {{ label }}
        </span>

        <button
            type="button"
            @click="changeIsHiddenState()"
            class="flex w-full cursor-pointer flex-row items-center justify-between rounded border bg-gray-100 px-3 py-2"
            :class="isHidden ? 'border-gray-400/60' : 'border-blue-600'"
        >
            <span ref="holder" :class="{ 'text-gray-400': !picked }">{{ placeholder }}</span>

            <ChevronUp
                class="ml-2 min-w-6 stroke-gray-900 transition-transform duration-150"
                :class="{ 'rotate-180': !isHidden }"
            />
        </button>

        <ul
            ref="dropdown"
            class="absolute top-full left-0 z-100 mt-1 w-full divide-y divide-gray-300 overflow-hidden rounded border border-gray-300 shadow-md shadow-black/20"
            :class="{ hidden: isHidden }"
        >
            <li
                v-if="options.length === 0"
                class="cursor-not-allowed bg-gray-100 p-2 text-center text-gray-400"
            >
                -
            </li>

            <li v-for="(item, index) in options" :key="index">
                <label
                    class="bg=white flex cursor-pointer flex-row items-start justify-between bg-white p-2 hover:bg-gray-200 has-checked:bg-gray-200 has-checked:[&>svg]:visible"
                >
                    <input
                        @click="updateHolder(item.identifier)"
                        type="radio"
                        :name="name"
                        :value="item.value"
                        v-model="picked"
                        class="hidden"
                        required
                    />
                    <div class="flex flex-row items-center">
                        <component
                            v-if="item.icon"
                            :is="item.icon.component"
                            class="w-6"
                            :class="item.icon.class"
                        />
                        <span class="ml-2">{{ item.identifier }}</span>
                    </div>

                    <Check class="invisible mt-1 ml-2 stroke-green-800" />
                </label>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, onMounted, onBeforeUnmount, watch } from 'vue'
import { ChevronUp, Check, LucideIcon } from 'lucide-vue-next'

defineProps<{
    label: string
    name: string
    placeholder?: string
    options: Array<{
        icon?: {
            component: LucideIcon
            class?: string
        }
        identifier: string
        value: string
    }>
}>()

const isHidden = ref(true)
const picked = defineModel()
const select = useTemplateRef<HTMLElement>('select')
const holder = useTemplateRef<HTMLElement>('holder')
const emit = defineEmits(['selectedValue'])

onMounted(() => {
    document.addEventListener('mousedown', onDocumenteMouseDown)
})

onBeforeUnmount(() => {
    document.removeEventListener('mousedown', onDocumenteMouseDown)
})

watch(picked, (value) => {
    emit('selectedValue', value)
})

function changeIsHiddenState() {
    isHidden.value = !isHidden.value
}

function updateHolder(text: string) {
    holder.value!.textContent = text
    isHidden.value = true
}

function onDocumenteMouseDown(event: MouseEvent) {
    if (isHidden.value) return

    const target = event.target as HTMLElement
    if (!select.value?.contains(target)) {
        isHidden.value = true
    }
}
</script>
