<template>
    <!-- Search for "take-picture" in admin.css -->
    <div class="take-picture">
        <input
            v-if="!props.isRequired"
            ref="clear-checkbox"
            type="checkbox"
            :name="props.checkboxName"
            class="hidden"
        />

        <input ref="input-file" type="file" accept="image/webp" class="hidden" :name="props.name" />

        <ImageCrop
            :isRequired="props.isRequired"
            :height="props.height"
            :width="props.width"
            :initialSource="props.initialSource"
            @clear="setCheckboxCheck"
            @croppedFile="setFile"
        />
    </div>
</template>

<style>
/* Fixes Django admin page */

.aligned .take-picture {
    ul {
        margin: 0 !important;
        padding: 0 !important;
    }

    label {
        display: flex !important;
        flex-wrap: wrap !important;
        padding: 8px !important;
        color: black !important;
        width: 100%;
    }

    h3 {
        font-size: 2rem;
        color: black;
    }
}
</style>

<script lang="ts" setup>
import { useTemplateRef } from 'vue'
import ImageCrop from '@/components/camera/ImageCrop.vue'

const props = defineProps({
    id: {
        type: String,
        required: false,
    },
    name: {
        type: String,
        required: true,
    },
    isRequired: {
        type: Boolean,
        required: true,
    },
    width: {
        type: Number,
        required: true,
    },
    height: {
        type: Number,
        required: true,
    },
    checkboxName: {
        type: String,
        required: false,
    },
    initialSource: {
        type: String,
        required: false,
    },
})

const inputFile = useTemplateRef<HTMLInputElement>('input-file')
const clearCheckbox = useTemplateRef<HTMLInputElement>('clear-checkbox')

function setCheckboxCheck(isChecked: boolean) {
    if (!clearCheckbox.value) return

    if (isChecked === true) {
        inputFile.value!.value = ''
    }

    clearCheckbox.value.checked = isChecked
}

function setFile(file: File | null) {
    const inputFileElmt = inputFile.value as HTMLInputElement
    inputFileElmt.value = ''

    if (file === null) return

    const dataTransfer = new DataTransfer()
    dataTransfer.items.add(file)
    inputFileElmt.files = dataTransfer.files
}
</script>
