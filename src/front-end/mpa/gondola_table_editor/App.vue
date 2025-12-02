<template>
    <div role="gondola-table-editor">
        <template v-if="props.establishmentId">
            <ProductGondolaFormset :gondolaId="props.gondolaId" />
        </template>
        <template v-else>
            <p class="indent-4 text-red-700">
                Para exibir a tabela dos produtos, primeiramente, cria a nova gôndola.
            </p>
        </template>
    </div>
</template>

<script lang="ts" setup>
import { provide } from 'vue'
import ProductGondolaFormset from '@/components/gondola/ProductGondolaFormset.vue'

const props = defineProps({
    gondolaId: {
        type: String,
        required: true,
    },
    establishmentId: {
        type: String,
        required: true,
    },
})
provide('establishmentId', props.establishmentId)
</script>

<style scoped>
div[role='gondola-table-editor'] {
    &:deep(h2) {
        color: black;
        font-size: var(--text-xl);
        margin: 0;
    }

    &:deep(h3) {
        margin: 0;
        color: black;
    }

    &:deep(dl) {
        margin: 0;
        color: black;
    }

    &:deep(tr) {
        background: transparent;
    }

    &:deep(td) {
        border: none;
    }

    &:deep(hr) {
        background-color: var(--color-gray-200);
    }

    &:deep(li) {
        list-style-type: none;
    }

    &:deep(.field) {
        label {
            color: var(--color-gray-600);
        }
        &:has(input:focus) {
            & > label {
                color: var(--color-sky-500);
            }
        }

        input {
            background-color: transparent;
            color: black;
            border: none;
            border-bottom: 1px solid;
            border-color: var(--color-gray-300);
            border-radius: 0;
        }
    }

    &:deep(ul) {
        list-style-type: none;
    }
}
</style>
