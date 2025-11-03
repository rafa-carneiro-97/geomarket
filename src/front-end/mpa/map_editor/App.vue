<template>
    <div class="map-editor">
        <textarea
            ref="textarea"
            class="hidden"
            :name="props.name"
            :isRequired="props.isRequired"
            :value="props.initialData"
        ></textarea>

        <MapEditor :initialData="props.initialData" @compressedData="updateTextarea" />
    </div>
</template>

<style>
[role='setup'] {
    .aligned label {
        background: red;
        display: flex;
    }
}
</style>

<script lang="ts" setup>
import { useTemplateRef, onMounted } from 'vue'
import MapEditor from '@/components/geojson/MapEditor.vue'

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    isRequired: {
        type: Boolean,
        required: true,
    },
    initialData: {
        type: String,
        required: true,
    },
})

const textarea = useTemplateRef<HTMLTextAreaElement>('textarea')

onMounted(() => {
    const textareaElmt = textarea.value as HTMLTextAreaElement
    // remove admin class
    textareaElmt.parentElement?.parentElement?.parentElement?.classList.remove('flex-container')
})

function updateTextarea(newValue: string) {
    const textareaElmt = textarea.value as HTMLTextAreaElement
    textareaElmt.value = newValue
}
</script>
