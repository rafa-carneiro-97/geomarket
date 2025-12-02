<template>
    <section
        v-if="!isHidden"
        class="fixed top-0 left-0 z-100 h-dvh w-dvw overflow-auto bg-black/80 py-12"
    >
        <div class="mx-auto w-11/12 max-w-xl rounded bg-white pb-12">
            <button type="button" @click="isHidden = true" class="ml-auto block">
                <X
                    :size="36"
                    :strokeWidth="2"
                    aria-label="Fechar"
                    class="boder-l ml-auto cursor-pointer stroke-gray-400 p-1 hover:stroke-black"
                />
            </button>

            <hr class="h-px bg-gray-200" />

            <div class="mx-auto w-11/12 pt-2">
                <BaseAlert
                    v-if="alert.message"
                    :status="BaseAlertStatus.Error"
                    :message="alert.message"
                    :key="alert.key"
                />

                <div class="relative">
                    <CameraViewer @getStream="setStream" />

                    <button
                        v-if="stream"
                        @click="takePicture"
                        type="button"
                        class="btn btn-blue absolute bottom-6 left-1/2 z-10 -translate-x-1/2"
                    >
                        Tirar foto
                    </button>
                </div>

                <AsyncTrackConfiguration v-if="stream" :videoTrack="stream.getVideoTracks()[0]" />
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { X } from 'lucide-vue-next'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import CameraViewer from '@/components/camera/CameraViewer.vue'
import { BaseAlertStatus } from '@/types/components/alerts'

const AsyncTrackConfiguration = defineAsyncComponent(
    () => import('@/components/camera/MediaTrackConfiguration.vue'),
)

const emit = defineEmits<{
    (e: 'picture', payload: string): void
}>()

const alert = ref({ message: '', key: 0 })
const isHidden = ref<boolean>(false)
const stream = ref<MediaStream | null>(null)

function setStream(data: MediaStream) {
    stream.value = data
}

function setAlertMessage(msg: string) {
    alert.value = {
        message: msg,
        key: alert.value.key + 1,
    }
}

function takePicture() {
    if (stream.value === null) return

    if (!('ImageCapture' in window)) {
        setAlertMessage(
            'Não é possível realizar a captura da câmera nesse navegador. Por favor, tente novamente em outro navegador.',
        )
        return
    }

    const track = stream.value.getVideoTracks()[0]
    const capture = new window.ImageCapture(track)

    capture.takePhoto().then((blob: Blob) => {
        const reader = new FileReader()

        reader.onload = () => {
            emit('picture', reader.result as string)
            isHidden.value = true
        }

        reader.onerror = (err) => {
            console.error(err)
            setAlertMessage(`Erro ao processar a imagem. Erro: ${err}`)
        }

        reader.readAsDataURL(blob)
    })
}
</script>
