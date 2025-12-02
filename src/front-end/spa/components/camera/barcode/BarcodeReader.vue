<template>
    <div class="relative flex">
        <button
            type="button"
            aria-label="Abrir leitor de código de barra"
            @click="open"
            class="group cursor-pointer border border-black/10 bg-gray-100"
        >
            <Scan :size="23" class="stroke-gray-600 group-hover:stroke-gray-800" />
        </button>

        <section
            v-if="!isHidden"
            ref="container"
            class="fixed top-0 left-0 z-100 h-dvh w-dvw overflow-y-scroll bg-black/80 py-12"
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

                <BaseAlert
                    v-if="alert.message"
                    :status="BaseAlertStatus.Error"
                    :message="alert.message"
                    :key="alert.key"
                    class="mt-4"
                />

                <TextLoading
                    v-if="isLoadingPermissions"
                    :isLoading="isLoadingPermissions"
                    class="mx-auto mt-10 table stroke-blue-600"
                />

                <div v-if="selectOptions.length > 0" class="mx-auto w-11/12 max-w-lg">
                    <BaseSelect
                        @selectedValue="setDeviceID"
                        label="Câmera"
                        name="video-device"
                        placeholder="Selecione o dispositivo"
                        :options="selectOptions"
                        class="text-white"
                    />

                    <div
                        class="inset-shadow relative mt-3 aspect-video w-full overflow-hidden rounded-t-lg border border-black/10 bg-gray-200 inset-shadow-sm inset-shadow-black/10"
                    >
                        <VideoOff
                            :size="80"
                            class="absolute top-1/2 left-1/2 z-0 -translate-1/2 stroke-gray-400"
                        />

                        <video
                            v-if="stream"
                            autoplay
                            class="relative z-10 w-full border border-gray-200 object-cover object-center"
                            :srcObject="stream"
                        ></video>
                    </div>

                    <AsyncCameraControl
                        v-if="stream"
                        :videoTrack="stream.getVideoTracks()[0]"
                        class="border-t-transparent"
                    />
                </div>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, watch, onBeforeUnmount, defineAsyncComponent } from 'vue'
import { BrowserMultiFormatReader, IScannerControls, BarcodeFormat } from '@zxing/browser'
import { DecodeHintType } from '@zxing/library'
import { Video, VideoOff, Scan, X } from 'lucide-vue-next'
import gsap from 'gsap'
import BaseSelect from '@/components/form/BaseSelect.vue'
import BaseAlert from '@/components/alerts/BaseAlert.vue'
import TextLoading from '@/components/loading/TextLoading.vue'
import { BaseAlertStatus } from '@/types/components/alerts'
import type { Option } from '@/types/components/forms/select'

const AsyncCameraControl = defineAsyncComponent(
    () => import('@/components/camera/MediaTrackConfiguration.vue'),
)

const emit = defineEmits<{
    (e: 'code', value: string): void
}>()

const container = useTemplateRef('container')

const alert = ref({ message: '', key: 0 })
const isHidden = ref<boolean>(true)
const isLoadingPermissions = ref<boolean>(true)
const selectOptions = ref<Array<Option>>([])
const stream = ref<MediaStream | null>(null)
let cameras: Array<MediaDeviceInfo> = []
let deviceID: string | null = null
let reader: null | BrowserMultiFormatReader = null
let controls: IScannerControls | null = null

onBeforeUnmount(async () => {
    closeStream()
    deviceID = null
    cameras = []
    reader = null
    controls?.stop()
    controls = null
})

watch(isHidden, (newValue) => {
    if (newValue === true) {
        closeStream()
    } else {
        startStream()
    }
})

function open() {
    isHidden.value = false

    gsap.fromTo(
        container.value!,
        {
            opacity: 0,
        },
        {
            opacity: 1,
            duration: 0.5,
        },
    )

    hasCameraPermissions()
        .then((hasPermission) => {
            if (!hasPermission) return
            setCameraOptions()
        })
        .finally(() => {
            isLoadingPermissions.value = false
        })
}

function setAlertMessage(msg: string) {
    alert.value = {
        message: msg,
        key: alert.value.key + 1,
    }
}

async function hasCameraPermissions(): Promise<boolean> {
    return navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            // Stop the stream immediately – we just needed permission
            stream.getTracks().forEach((track) => track.stop())
            return true
        })
        .catch((err) => {
            console.error(err)

            if (err.name === 'NotAllowedError') {
                setAlertMessage(
                    'O acesso à câmera foi negado, por favor, habilite o acesso e recarregue a página.',
                )

                return false
            }

            if (err.name === 'NotReadableError') {
                setAlertMessage('Não há câmeras conectadas ao dispositvo.')
                return false
            }

            setAlertMessage(`Erro inesperado, por favor, contact a equipe. Erro: ${err}`)
            return false
        })
}

async function setCameraOptions() {
    navigator.mediaDevices.enumerateDevices().then((items) => {
        selectOptions.value = []
        cameras = items.filter((item) => item.kind === 'videoinput')

        cameras.forEach((item, index) => {
            selectOptions.value.push({
                icon: { component: Video, class: 'stroke-gray-700' },
                identifier: item.label,
                value: index.toString(),
            })
        })
    })
}

function setDeviceID(choice: string) {
    deviceID = cameras[parseInt(choice)].deviceId
    startStream()
}

function closeStream() {
    stream.value?.getTracks().forEach((track) => track.stop())
    stream.value = null
}

async function startStream() {
    if (!deviceID) return
    closeStream()

    const hints = new Map()
    hints.set(DecodeHintType.TRY_HARDER, true)
    hints.set(DecodeHintType.POSSIBLE_FORMATS, [
        BarcodeFormat.CODABAR,
        BarcodeFormat.CODE_39,
        BarcodeFormat.CODE_93,
        BarcodeFormat.CODE_128,
        BarcodeFormat.EAN_8,
        BarcodeFormat.EAN_13,
        BarcodeFormat.ITF,
        BarcodeFormat.UPC_A,
        BarcodeFormat.UPC_E,
        BarcodeFormat.UPC_EAN_EXTENSION,
    ])

    await navigator.mediaDevices
        .getUserMedia({
            audio: false,
            video: {
                deviceId: { exact: deviceID },
            },
        })
        .then(async (data) => {
            stream.value = data
            reader = new BrowserMultiFormatReader()
            controls = await reader.decodeFromStream(data, undefined, (result) => {
                if (result) {
                    isHidden.value = true
                    emit('code', result!.getText())
                }
            })
        })
        .catch((err) => {
            console.error(err)

            if (err.name === 'NotReadableError') {
                setAlertMessage('Não foi possível inicializar o dispositivo de captura de vídeo.')
                return
            }

            setAlertMessage(`Erro inesperado, contacte a equipe. Erro: ${err}`)
        })
}
</script>
