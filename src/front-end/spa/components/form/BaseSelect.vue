<template>
    <div ref="select" :aria-label="label" class="relative">
        <span
            class="px-1 text-xs leading-none tracking-tight text-balance"
            :class="{ 'font-bold text-blue-400': !isHidden }"
        >
            {{ label }}
        </span>

        <button
            type="button"
            @click="changeHiddenState()"
            class="flex w-full cursor-pointer flex-row items-center justify-between rounded-sm border bg-white px-2 py-1.5"
            :class="isHidden ? 'border-gray-400/60' : 'border-blue-400'"
        >
            <span ref="holder" :class="[picked ? 'text-black' : 'text-gray-500']">
                {{ placeholder }}
            </span>

            <ChevronUp
                class="ml-2 min-w-6 stroke-gray-900 transition-transform duration-150"
                :class="{ 'rotate-180': !isHidden }"
            />
        </button>

        <ul
            ref="dropdown"
            class="absolute top-full left-0 z-100 mt-1 w-full divide-y divide-gray-300 rounded border border-gray-300 bg-white text-black shadow-md shadow-black/20"
            :class="{ hidden: isHidden }"
        >
            <li
                v-if="options.length === 0"
                class="cursor-not-allowed p-2 text-center text-gray-400"
            >
                -
            </li>

            <li v-for="(item, index) in options" :key="index">
                <label
                    class="justify-betweenhover:bg-blue-200 flex cursor-pointer flex-row items-start p-2 hover:bg-gray-100 has-checked:[&>svg]:visible"
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
                            :class="item.icon.class"
                            class="w-6"
                        />
                        <span class="ml-2">{{ item.identifier }}</span>
                    </div>

                    <Check class="invisible mt-1 ml-2 h-4 stroke-green-800" />
                </label>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, onMounted, onBeforeUnmount, watch } from 'vue'
import { ChevronUp, Check } from 'lucide-vue-next'
import type { Option } from '@/types/components/forms/select'

defineProps<{
    label: string
    name: string
    placeholder?: string
    options: Array<Option>
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

function changeHiddenState() {
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
