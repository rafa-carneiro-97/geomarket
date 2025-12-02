<template>
    <div>
        <ProductTableEditor
            :gondolaId="props.gondolaId"
            @initialSize="(s) => (initialSize = s)"
            @result="(v) => (result = v)"
        />

        <div class="hidden">
            <template v-if="!result">
                <input type="text" name="gondolaproduct_set-TOTAL_FORMS" value="0" />

                <input type="text" name="gondolaproduct_set-INITIAL_FORMS" value="0" />

                <input type="text" name="gondolaproduct_set-MIN_NUM_FORMS" value="0" />

                <input type="text" name="gondolaproduct_set-MAX_NUM_FORMS" value="1000" />
            </template>

            <template v-if="result">
                <input
                    type="text"
                    name="gondolaproduct_set-TOTAL_FORMS"
                    :value="result.dataset.length + result.deleted.length"
                />

                <input type="text" name="gondolaproduct_set-INITIAL_FORMS" :value="initialSize" />

                <input type="text" name="gondolaproduct_set-MIN_NUM_FORMS" value="0" />

                <input type="text" name="gondolaproduct_set-MAX_NUM_FORMS" value="1000" />

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
import { ref } from 'vue'
import ProductTableEditor from '@/components/gondola/ProductTableEditor.vue'

const props = defineProps({
    gondolaId: {
        type: String,
        required: true,
    },
})

type ProductTableEditorInstance = InstanceType<typeof ProductTableEditor>
type ResultEmit = ProductTableEditorInstance['$emit']
type ResultType = Parameters<ResultEmit>[1]

const initialSize = ref<number>()
const result = ref<ResultType>()
</script>
