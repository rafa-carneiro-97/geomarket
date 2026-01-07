<template>
    <div class="flex flex-col items-center justify-start pb-12">
        <div
            class="mx-w-3xl m-4 inline-flex flex-col items-stretch overflow-hidden rounded-lg border border-indigo-700 md:flex-row"
        >
            <h2
                class="text-shadow flex-1 bg-indigo-700 p-3 text-center text-2xl font-bold text-white"
            >
                {{ establishmentData?.name ?? '???' }}
                <span v-if="establishmentData?.address" class="line-clamp-2 max-w-sm text-balance">
                    {{ establishmentData.address }}
                </span>
            </h2>

            <div class="relative flex flex-1 items-center p-3 pt-4">
                <span class="absolute top-0 left-2 text-sm text-gray-500">dispositivo:</span>

                <span class="w-full text-center text-lg font-bold text-indigo-700">
                    {{ props.locatorId }}
                </span>
            </div>
        </div>

        <ol ref="ordered-list" class="mt-12 w-11/12 max-w-lg">
            <li
                v-for="(item, index) in infoList"
                :key="index"
                class="justify-st mb-4 flex flex-row items-stretch overflow-hidden rounded border border-black/20"
                :class="{
                    'text-yellow-800': item.type === InfoType.PENDING,
                    'text-green-900': item.type === InfoType.SUCCESS,
                    'text-red-800': item.type === InfoType.ERROR,
                }"
            >
                <div
                    class="flex flex-row flex-nowrap items-center justify-center border-r border-black/20 px-3"
                    :class="{
                        'bg-amber-100': item.type === InfoType.PENDING,
                        'bg-green-200': item.type === InfoType.SUCCESS,
                        'bg-red-200': item.type === InfoType.ERROR,
                    }"
                >
                    <span class="mr-4 text-2xl text-inherit">{{ index + 1 }}</span>

                    <component :is="infoIcons[item.type]" :size="26" />
                </div>

                <p class="p-4 text-lg">{{ item.text }}</p>
            </li>
        </ol>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, onBeforeUnmount, ref, useTemplateRef, nextTick } from 'vue'
import { AlertTriangle, Check, Hourglass } from 'lucide-vue-next'
import axios from 'axios'
import gsap from 'gsap'

enum InfoType {
    PENDING = 'pending',
    ERROR = 'error',
    SUCCESS = 'success',
}

interface InfoInterface {
    text: string
    type: InfoType
}

interface EstablishmentDataInterface {
    name: string
    address: string
}

let socket: null | WebSocket = null
const orderedList = useTemplateRef('ordered-list')
const establishmentData = ref<EstablishmentDataInterface | null>(null)
const infoList = ref<Array<InfoInterface>>([])
const infoIcons = {
    [InfoType.PENDING]: Hourglass,
    [InfoType.SUCCESS]: Check,
    [InfoType.ERROR]: AlertTriangle,
}

const props = defineProps({
    establishmentId: {
        type: Number,
        required: true,
    },
    locatorId: {
        type: Number,
        required: true,
    },
})

onMounted(async () => {
    await axios
        .get(`/api/establishment/${props.establishmentId}/`)
        .then((response) => {
            establishmentData.value = response.data
            // startCartLocator()
        })
        .catch((error) => {
            console.error(
                `Error on fetching the establishment "${props.establishmentId}". Error: ${error}`,
            )
        })
})

onMounted(async () => {
    startCartLocator()
})

onBeforeUnmount(() => {
    if (socket) {
        socket.close()
        socket = null
    }
})

async function addInfo(info: InfoInterface) {
    infoList.value.push(info)

    await nextTick()

    const items = orderedList.value?.children as HTMLCollection
    const el = items[items.length - 1] as HTMLElement

    gsap.from(el, {
        opacity: 0,
        y: 20,
        scale: 0.9,
        duration: 0.5,
        ease: 'power2.out',
    })
}

async function startCartLocator() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${protocol}://${window.location.host}/ws/cart-locator/${props.locatorId}/`

    addInfo({ text: `Iniciando conexão em ${url}`, type: InfoType.PENDING })

    socket = new WebSocket(url)

    socket.onopen = () => {
        addInfo({ text: 'Conexão aberta com sucesso.', type: InfoType.SUCCESS })
    }
    socket.onerror = (ev: Event) => {
        console.error('Error: ', ev)

        addInfo({ text: `Falha na conexão.`, type: InfoType.ERROR })
    }
    socket.onclose = (ev: CloseEvent) => {
        console.error('Closed: ', ev)

        addInfo({
            text: `A conexão com o servidor foi encerrada. Motivo: ${ev.reason || 'não informado.'}`,
            type: InfoType.ERROR,
        })
    }
    socket.onmessage = (ev: MessageEvent) => {
        console.info(ev)
        addInfo({
            text: `Informação recebida do servidor: ${ev.data}`,
            type: InfoType.SUCCESS,
        })
    }
}
</script>
