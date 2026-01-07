<template>
    <div class="relative h-dvh w-full bg-slate-100">
        <AsyncSearchBox v-if="cartPosition !== null" style="z-index: 500" />

        <AlertBox v-if="alertBox.message" :message="alertBox.message" :key="alertBox.key" />

        <Transition>
            <div
                v-if="geojsonObject === undefined"
                class="absolute top-1/2 left-1/2 -translate-1/2"
            >
                <img src="./assets/invalid-map.svg" />

                <p class="text-bold mt-2 text-center font-sans text-2xl font-bold text-slate-600">
                    Mapa inválido
                </p>
            </div>
        </Transition>

        <Transition>
            <div v-if="!isCartValid" class="absolute top-1/2 left-1/2 -translate-1/2">
                <img src="./assets/invalid-cart.svg" class="mx-auto" />

                <p class="text-bold mt-2 text-center font-sans text-2xl font-bold text-slate-600">
                    Carrinho não encontrado
                </p>
            </div>
        </Transition>

        <MapViewer
            v-if="isConnectionOpen"
            :geojsonObject="geojsonObject"
            :isFullscreen="true"
            @map="(v) => (map = v)"
        />

        <Transition>
            <div
                v-if="isConnectionOpen && cartPosition === null"
                class="fixed top-0 left-0 h-dvh w-full bg-black/80"
                style="z-index: 2000"
            >
                <div
                    class="absolute top-1/2 left-1/2 flex -translate-1/2 flex-row flex-nowrap items-center justify-center rounded bg-white px-3 py-2"
                >
                    <p class="text-bold text-center font-sans text-2xl font-bold text-slate-600">
                        Conectando
                    </p>

                    <div class="loader ml-2"></div>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { onMounted, onBeforeUnmount, ref, watch, defineAsyncComponent } from 'vue'
import type { Map, Marker } from 'leaflet'
import Leaflet from 'leaflet'
import AlertBox from '@/components/alerts/AlertBox.vue'
import MapViewer from '@/components/map/MapViewer.vue'

const AsyncSearchBox = defineAsyncComponent(() => import('./components/SearchBox.vue'))

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

interface PositionInterface {
    latitude: number
    longitude: number
}

const geojsonObject = ref<GeoJSON.GeoJsonObject | null>(null)
const alertBox = ref({ message: '', key: 0 })
const isCartValid = ref<boolean>(true)
const isConnectionOpen = ref<boolean>(false)
const cartPosition = ref<null | PositionInterface>(null)
const cartMarker = ref<Marker | null>(null)
let socket: null | WebSocket = null
let map: Map | null | undefined = null

const cartIcon = Leaflet.divIcon({
    className: 'cart-locator-marker',
    html: `
        <svg 
            width="32" height="32"
            viewBox="0 0 32 32"
            class="drop-shadow-lg drop-shadow-black/20"
        >
            <circle cx="16" cy="16" r="10" fill="oklch(54.6% 0.245 262.881)" />
            <circle cx="16" cy="16" r="4" fill="white" />
        </svg>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
})

onMounted(async () => {
    await axios
        .get(`/api/establishment/${props.establishmentId}/map/`)
        .then((response) => {
            const viewer = response.data.viewer
            geojsonObject.value = viewer

            if (viewer === undefined) {
                setAlertBoxMessage(
                    'Mapa não encontrado, por favor, recarregue a página. Se o erro persistir, contacte a equipe.',
                )
                return
            }

            startCartLocator()
            cartPosition.value = {
                latitude: 2.1,
                longitude: 3.1,
            }
        })
        .catch((error) => {
            console.error(
                `Error on fetching the  establishment "${props.establishmentId}" map. Error: ${error}`,
            )
        })
})

onBeforeUnmount(() => {
    if (socket) {
        socket.close()
        socket = null
    }

    if (map) {
        map = null
    }
})

const sleep = (ms: number) => {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

watch(cartPosition, async (newValue) => {
    if (!newValue) return
    await sleep(500)
    if (!map) return

    const latLng: [number, number] = [newValue.latitude, newValue.longitude]

    if (!cartMarker.value) {
        cartMarker.value = Leaflet.marker(latLng, {
            icon: cartIcon,
            title: 'Pos',
        }).addTo(map)
    } else {
        cartMarker.value.setLatLng(latLng)
    }
})

function setAlertBoxMessage(msg: string) {
    alertBox.value = {
        message: msg,
        key: alertBox.value.key + 1,
    }
}

function startCartLocator() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${protocol}://${window.location.host}/ws/cart-locator/${props.locatorId}/`
    socket = new WebSocket(url)

    socket.onopen = () => {
        isConnectionOpen.value = true
        console.info(`Connection open to the locator "${props.locatorId}".`)
    }
    socket.onerror = (ev: Event) => {
        isCartValid.value = false
        console.error('Webscoket error:', ev)
    }

    socket.onclose = () => {
        console.error('Connection closed')
        setAlertBoxMessage('A conexão com o servidor foi fechada. Por favor, recarregue a página.')
    }

    socket.onmessage = (ev: MessageEvent) => {
        console.log('Message received from server:', ev.data)
        cartPosition.value = parseLatLog(ev.data)
    }
}

function parseLatLog(text: string): PositionInterface | null {
    const parts = text.split(',')
    if (parts.length !== 2) return null

    const latitude = parseFloat(parts[0].trim())
    const longitude = parseFloat(parts[1].trim())

    if (Number.isNaN(latitude) || Number.isNaN(longitude)) return null

    return {
        latitude,
        longitude,
    }
}
</script>

<style>
.v-enter-active,
.v-leave-active {
    transition: opacity 0.5s ease;
    transition-delay: 0.75ms;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}

.cart-locator-marker {
    transition: transform 1s ease;
}

.loader {
    width: 16px;
    aspect-ratio: 1;
    border-radius: 50%;
    background:
        radial-gradient(farthest-side, #ed303c 94%, #0000),
        radial-gradient(farthest-side, #3b8183 94%, #0000),
        radial-gradient(farthest-side, #fad089 94%, #0000),
        radial-gradient(farthest-side, #ff9c5b 94%, #0000), #ed303c;
    background-size: 105% 105%;
    background-repeat: no-repeat;
    animation: l5 2s infinite;
}
@keyframes l5 {
    0% {
        background-position:
            50% -50px,
            -40px 50%,
            50% calc(100% + 50px),
            calc(100% + 50px) 50%;
    }
    20%,
    25% {
        background-position:
            50% -50px,
            -50px 50%,
            50% calc(100% + 50px),
            50% 50%;
    }
    45%,
    50% {
        background-position:
            50% -50px,
            -50px 50%,
            50% 50%,
            50% 50%;
    }
    75%,
    75% {
        background-position:
            50% -50px,
            50% 50%,
            50% 50%,
            50% 50%;
    }
    95%,
    100% {
        background-position:
            50% 50%,
            50% 50%,
            50% 50%,
            50% 50%;
    }
}
</style>
