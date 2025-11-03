<template>
    <div
        class="rounded-sm border border-gray-300 p-1"
        :style="{
            width: '100%',
            maxWidth: props.width + 'px',
        }"
    >
        <TakePicture
            v-if="takePictureKey > 0"
            :key="takePictureKey"
            @picture="(data) => (imageViewerSource = data)"
        />

        <input
            ref="input-file"
            type="file"
            accept="image/*"
            class="hidden"
            @change="updateUploadFile"
        />

        <div
            class="relative bg-gray-200"
            :style="{
                width: '100%',
                aspectRatio: props.width / props.height,
            }"
        >
            <FileImage
                v-if="!imageCroppedSource"
                :strokeWidth="1.2"
                class="absolute top-1/2 left-1/2 size-4/12 -translate-1/2 fill-gray-300 stroke-gray-400"
            />

            <img v-if="imageCroppedSource" :src="imageCroppedSource" alt="Imagem cortada" />
        </div>

        <div class="flex flex-col">
            <button
                type="button"
                aria-label="Tirar uma foto"
                @click="takePictureKey++"
                class="btn btn-gray mt-1.5 flex cursor-pointer flex-row items-center"
            >
                <Camera :strokeWidth="2.3" :size="23" class="stroke-gray-500" />

                <span class="ml-1.5">Tirar foto</span>
            </button>

            <button
                type="button"
                aria-label="Fazer upload de uma image,"
                @click="inputFile?.click()"
                class="btn btn-gray mt-2 flex cursor-pointer flex-row items-center"
            >
                <ImageUp :strokeWidth="2.3" :size="23" class="stroke-gray-500" />

                <span class="ml-1.5">Fazer upload</span>
            </button>

            <button
                v-if="!props.isRequired"
                v-show="imageCroppedSource !== null"
                type="button"
                aria-label="Remover imagem"
                @click="removeImage"
                class="btn btn-red mt-2 flex cursor-pointer flex-row items-center"
            >
                <Trash2 :strokeWidth="2.3" :size="23" class="stroke-red-800" />

                <span class="ml-1.5">Remover</span>
            </button>
        </div>

        <section
            v-show="imageViewerSource !== null"
            class="fixed top-0 left-0 z-90 h-dvh w-full overflow-auto bg-black/80 pb-12"
        >
            <button type="button" class="ml-auto block">
                <X
                    :size="50"
                    :strokeWidth="2"
                    @click="imageViewerSource = null"
                    aria-label="Fechar"
                    class="boder-l ml-auto cursor-pointer stroke-gray-300 p-1 hover:stroke-white"
                />
            </button>

            <BaseAlert
                v-if="alert.message"
                :status="AlertStatus.Error"
                :message="alert.message"
                :key="alert.key"
            />

            <div class="mx-auto w-11/12">
                <div class="mx-auto table max-w-2xl border border-gray-500">
                    <img
                        :src="imageViewerSource as string"
                        ref="image-viewer"
                        alt="Imagem para ser cortada"
                    />
                </div>

                <button
                    type="button"
                    aria-label="Cortar"
                    @click="crop"
                    class="btn btn-blue mx-auto mt-4"
                >
                    Cortar
                </button>
            </div>
        </section>
    </div>
</template>

<script lang="ts" setup>
import { ref, useTemplateRef, onBeforeUnmount, watch, nextTick } from 'vue'
import { Camera, Trash2, ImageUp, FileImage, X } from 'lucide-vue-next'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.min.css'
import TakePicture from '@/components/camera/TakePicture.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import { AlertStatus } from '@/types/components/alert'

const props = defineProps({
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
    initialSource: {
        type: String,
        required: false,
    },
})

onBeforeUnmount(() => {
    if (cropper !== null) {
        cropper.destroy()
        cropper = null
    }
})

const emit = defineEmits<{
    (e: 'clear', payload: boolean): void
    (e: 'croppedFile', payload: File | null): void
}>()

const inputFile = useTemplateRef<HTMLInputElement>('input-file')
const imageViewer = useTemplateRef<HTMLImageElement>('image-viewer')
const imageViewerSource = ref<string | null>(null)
const imageCroppedSource = ref<string | null>(props.initialSource || null)
const takePictureKey = ref<number>(0)
const alert = ref({ message: '', key: 0 })
let cropper: Cropper | null = null

watch(imageViewerSource, async (newValue) => {
    if (cropper !== null) {
        cropper.destroy()
    }

    if (newValue === null) return

    await nextTick()

    cropper = new Cropper(imageViewer.value as HTMLImageElement, {
        aspectRatio: props.width / props.height,
        viewMode: 1,
        movable: false,
        cropBoxResizable: true,
        zoomable: false,
        dragMode: 'none',
        responsive: false,
        background: false,
        minCropBoxWidth: 120,
    })
})

function setAlertMessage(msg: string) {
    alert.value = {
        message: msg,
        key: alert.value.key + 1,
    }
}

function updateUploadFile() {
    const files = inputFile.value!.files
    if (!files) return

    const file = files[0]
    if (!file.type.startsWith('image/')) {
        setAlertMessage('O arquivo selecionado não é uma imagem')
        return
    }

    const reader = new FileReader()
    reader.onload = () => {
        emit('clear', false)
        imageViewerSource.value = reader.result as string
    }
    reader.onerror = (err) => {
        console.error(err)
        setAlertMessage(`Erro ao processar a imagem. Erro: ${err}`)
    }
    reader.readAsDataURL(file)
    inputFile.value!.value = ''
}

function removeImage() {
    emit('clear', true)
    emit('croppedFile', null)
    imageCroppedSource.value = null
}

function crop() {
    if (cropper === null) return

    const data = cropper
        .getCroppedCanvas({
            width: props.width,
            height: props.height,
            fillColor: '#fff',
        })
        .toDataURL('image/webp')

    if (typeof data !== 'string') {
        setAlertMessage('Não foi possível cortar a imagem')
        return
    }

    imageCroppedSource.value = data

    const decode = data.split(',')[1]
    const enconded = atob(decode)
    let size = enconded.length
    const u8data = new Uint8Array(size)

    while (size--) {
        u8data[size] = enconded.charCodeAt(size)
    }

    const file = new File([u8data], 'image.webp', { type: 'image/webp' })
    emit('croppedFile', file)
    imageViewerSource.value = null
}
</script>
