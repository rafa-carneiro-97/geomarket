<template>
    <section v-if="!isHidden">
        <div class="fixed top-0 left-0 z-90 h-dvh w-full overflow-auto bg-black/80 pb-12">
            <button type="button" class="ml-auto block">
                <X
                    :size="50"
                    :strokeWidth="2"
                    @click="isHidden = true"
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
    </section>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { X } from 'lucide-vue-next'
import BaseAlert from '@/components/BaseAlert.vue'
import CameraViewer from '@/components/camera/CameraViewer.vue'
import { AlertStatus } from '@/types/components/alert'

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
            'Não é possível realizar a captura da câmera nesse navegador. Por favor, tente novamente numoutro navegador.',
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
