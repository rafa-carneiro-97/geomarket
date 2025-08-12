<template>
    <div>
        <button
            type="button"
            aria-label="Abrir leitor de código de barra"
            @click="setHiddenStateFalse"
            class="cursor-pointer border border-black/10 bg-gray-100"
        >
            <Scan :size="30" class="stroke-gray-600" />
        </button>

        <section
            ref="container"
            class="fixed top-0 left-0 z-100 h-dvh w-dvw overflow-y-scroll bg-black/80 pb-6"
            :class="{ hidden: isHidden }"
        >
            <X
                :size="50"
                :strokeWidth="2"
                @click="isHidden = true"
                aria-label="Fechar"
                class="boder-l ml-auto cursor-pointer bg-white/5 stroke-gray-300 p-1 hover:stroke-white"
            />

            <BaseAlert
                v-if="alert.message"
                :status="AlertStatus.Error"
                :message="alert.message"
                :key="alert.key"
            />

            <div class="mx-auto w-11/12 max-w-lg">
                <BaseSelect
                    @selectedValue="setDeviceID"
                    label="Câmera"
                    name="video-device"
                    placeholder="Selecione o dispositivo"
                    :options="selectOptions"
                    class="[&>span]:text-white"
                />

                <div
                    class="inset-shadow relative mt-3 aspect-video w-full overflow-hidden border border-black/10 bg-gray-200 inset-shadow-sm inset-shadow-black/10"
                >
                    <VideoOff
                        :size="80"
                        class="absolute top-1/2 left-1/2 z-0 -translate-1/2 stroke-gray-400"
                    />

                    <video
                        autoplay
                        class="relative z-10 w-full object-cover object-center"
                        :srcObject="stream"
                    ></video>
                </div>

                <CameraControl
                    v-if="stream"
                    :videoTrack="stream.getVideoTracks()[0]"
                    class="border-t-transparent"
                />
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, watch, onBeforeUnmount } from 'vue'
import { BrowserMultiFormatReader, IScannerControls, BarcodeFormat } from '@zxing/browser'
import { DecodeHintType } from '@zxing/library'
import { Video, VideoOff, Scan, X, LucideIcon } from 'lucide-vue-next'
import gsap from 'gsap'
import BaseSelect from '@/components/form/BaseSelect.vue'
import BaseAlert, { AlertStatus } from '@/components/BaseAlert.vue'
import CameraControl from '@/components/barcode/CameraControl.vue'

const emit = defineEmits(['code'])

const container = useTemplateRef('container')
const alert = ref({
    message: '',
    key: 0,
})
const isHidden = ref<boolean>(true)
const selectOptions = ref<
    Array<{
        icon?: { component: LucideIcon; class?: string }
        identifier: string
        value: string
    }>
>([])
const stream = ref<MediaStream | null>(null)

let cameras: Array<MediaDeviceInfo> = []
let deviceID: string | null = null
let reader: null | BrowserMultiFormatReader = null
let controls: IScannerControls | null = null

onBeforeUnmount(async () => {
    closeStream()
    deviceID = null
    cameras = []
})

watch(isHidden, (value) => {
    if (value === true) {
        closeStream()
    } else {
        startStream()
    }
})

async function setHiddenStateFalse() {
    if (await hasCameraPermissions()) {
        if (cameras.length === 0) setCameraOptions()
    }
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
                alert.value.message =
                    'O acesso à câmera foi negado, por favor, habilite o acesso e recarregue a página.'
                alert.value.key++
                return false
            }

            if (err.name === 'NotReadableError') {
                alert.value.message = 'Não há câmeras conectadas ao dispositvo.'
                alert.value.key++
                return false
            }

            alert.value.message = `Erro inesperado, por favor, contact a equipe. Erro: ${err}`
            alert.value.key++
            return false
        })
}

async function setCameraOptions() {
    await navigator.mediaDevices.enumerateDevices().then((items) => {
        cameras = items.filter((item) => item.kind === 'videoinput')
    })

    cameras.forEach((item, index) => {
        selectOptions.value.push({
            icon: { component: Video, class: 'stroke-gray-700' },
            identifier: item.label,
            value: index.toString(),
        })
    })

    console.log(selectOptions.value)
}

function setDeviceID(choice: string) {
    deviceID = cameras[parseInt(choice)].deviceId
    startStream()
}

function closeStream() {
    stream.value?.getTracks().forEach((track) => track.stop())
    stream.value = null
    controls?.stop()
    controls = null
    reader = null
}

async function startStream() {
    if (!deviceID) return

    closeStream()

    // const hints = new Map()
    // hints.set(DecodeHintType.TRY_HARDER, true)
    // hints.set(DecodeHintType.POSSIBLE_FORMATS, [
    //     BarcodeFormat.AZTEC,
    //     BarcodeFormat.CODABAR,
    //     BarcodeFormat.CODE_39,
    //     BarcodeFormat.CODE_93,
    //     BarcodeFormat.CODE_128,
    //     BarcodeFormat.EAN_8,
    //     BarcodeFormat.EAN_13,
    //     BarcodeFormat.ITF,
    //     BarcodeFormat.UPC_A,
    //     BarcodeFormat.UPC_E,
    //     BarcodeFormat.UPC_EAN_EXTENSION,
    // ])

    await navigator.mediaDevices
        .getUserMedia({
            audio: false,
            video: {
                deviceId: { exact: deviceID },
            },
        })
        .then(async (data) => {
            stream.value = data
            // reader = new BrowserMultiFormatReader()
            // controls = await reader.decodeFromStream(data, undefined, (result) => {
            //     if (result) {
            //         isHidden.value = true
            //         emit('code', result?.getText())
            //     }
            // })
        })
        .catch((err) => {
            console.log(err)

            if (err.name === 'NotReadableError') {
                alert.value.message =
                    'Não foi possível inicializar o dispositivo de captura de vídeo.'
                alert.value.key++
                return
            }

            alert.value.message = `Erro inesperado, contacte a equipe. Erro: ${err}`
            alert.value.key++
        })
}
</script>

<style scoped></style>
