<template>
    <div role="gondola-table-editor">
        <template v-if="props.establishmentId">
            <ProductTableEditor
                :gondolaId="props.gondolaId"
                @initialSize="(s) => (initialSize = s)"
                @result="(v) => (result = v)"
            />
        </template>
        <template v-else>
            <p class="indent-4 text-red-700">
                Para exibir a tabela dos produtos, primeiramente, crie a nova gôndola.
            </p>
        </template>

        <div class="hidden">
            <input type="text" name="gondolaproduct_set-MAX_NUM_FORMS" value="1000" />
            <input type="text" name="gondolaproduct_set-MIN_NUM_FORMS" value="0" />

            <template v-if="!result">
                <input type="text" name="gondolaproduct_set-TOTAL_FORMS" value="0" />
                <input type="text" name="gondolaproduct_set-INITIAL_FORMS" value="0" />
            </template>

            <template v-if="result">
                <input
                    type="text"
                    name="gondolaproduct_set-TOTAL_FORMS"
                    :value="result.dataset.length + result.deleted.length"
                />

                <input type="text" name="gondolaproduct_set-INITIAL_FORMS" :value="initialSize" />

                <br />
                <hr />
                <br />

                <template v-for="(item, index) in result.deleted" :key="index">
                    <input
                        v-if="item.id"
                        type="text"
                        :name="`gondolaproduct_set-${index}-id`"
                        :value="item.id"
                    />

                    <input type="checkbox" :name="`gondolaproduct_set-${index}-DELETE`" checked />

                    <br />
                    <br />
                </template>

                <template v-for="(item, index) in result.dataset" :key="index">
                    <input
                        v-if="item.id"
                        type="text"
                        :name="`gondolaproduct_set-${index + result.deleted.length}-id`"
                        :value="item.id"
                    />

                    <input
                        type="text"
                        :name="`gondolaproduct_set-${index + result.deleted.length}-product`"
                        :value="item.product.id"
                    />

                    <input
                        type="text"
                        :name="`gondolaproduct_set-${index + result.deleted.length}-gondola`"
                        :value="props.gondolaId"
                    />

                    <input
                        type="number"
                        :name="`gondolaproduct_set-${index + result.deleted.length}-gondola_x_position`"
                        :value="item.gondola.xPosition"
                    />

                    <input
                        type="number"
                        :name="`gondolaproduct_set-${index + result.deleted.length}-gondola_y_position`"
                        :value="item.gondola.yPosition"
                        data-t="gondolaproduct_set-0-DELETE"
                    />

                    <br />
                    <br />
                </template>
            </template>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { provide, ref } from 'vue'
import ProductTableEditor from '@/components/gondola/ProductTableEditor.vue'
import type { ResultEventInterface } from '@/components/gondola/ProductTableEditor.vue'

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

const initialSize = ref<number>()
const result = ref<ResultEventInterface>()
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
