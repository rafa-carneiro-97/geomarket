<template>
    <div>
        <AlertBox v-if="alertBox.message" :message="alertBox.message" :key="alertBox.key" />

        <div
            ref="viewer"
            style="height: 500px"
            class="relative w-full border border-b-0 border-black/20 bg-gray-200"
        >
            <TriangleAlert
                v-if="!geojson"
                :size="60"
                class="absolute top-1/2 left-1/2 -translate-1/2 stroke-gray-500"
            />
        </div>
    </div>
</template>

<style scoped>
:deep(.map-textbox) {
    background-color: transparent;
    padding: 0;
    border: 0px;
    box-shadow: none;
    color: black;
    font-weight: bolder;
}
</style>

<script lang="ts" setup>
import { ref, useTemplateRef, onMounted, onBeforeUnmount, watch } from 'vue'
import { TriangleAlert } from 'lucide-vue-next'
import Leaflet from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { Map, MapOptions, GeoJSON, GeoJSONOptions, Layer } from 'leaflet'
import AlertBox from '@/components/alerts/AlertBox.vue'

const props = defineProps({
    geojsonObject: {
        type: Object as () => GeoJSON.GeoJsonObject | null,
        required: true,
    },
})

const emit = defineEmits<{
    (e: 'map', value: Map | null): void
}>()

const viewer = useTemplateRef<HTMLDivElement>('viewer')
const geojson = ref<GeoJSON | null>(null)
const alertBox = ref({ message: '', key: 0 })
const OUTER_DISTANCE = 20
let map: Map | null = null

onBeforeUnmount(() => {
    closeMap()
})

onMounted(() => {
    if (props.geojsonObject === null) return
    processGeojsonObject(props.geojsonObject)
})

watch(
    () => props.geojsonObject,
    (newValue) => {
        if (newValue === null) {
            geojson.value?.remove()
            geojson.value = null
            closeMap()
            return
        }

        processGeojsonObject(newValue)
    },
)

watch(geojson, (newValue) => {
    if (newValue === null) return

    const bounds = newValue.getBounds()

    const expandedGeojsonBounds = Leaflet.latLngBounds(
        Leaflet.latLng(bounds.getSouth() - OUTER_DISTANCE, bounds.getWest() - OUTER_DISTANCE),
        Leaflet.latLng(bounds.getNorth() + OUTER_DISTANCE, bounds.getEast() + OUTER_DISTANCE),
    )

    const options: MapOptions = {
        renderer: Leaflet.svg({ padding: 1000 }), // large padding = no clipping effect
        attributionControl: false,
        // Interaction
        zoomSnap: 0.2,
        zoomDelta: 0.5,
        trackResize: false,
        zoomControl: false,
        // Inertia
        inertia: true,
        // State
        crs: Leaflet.CRS.Simple,
        center: [0, 0],
        minZoom: 2,
        maxZoom: 6,
        zoom: 0,
        maxBounds: expandedGeojsonBounds,
    }

    createMap(options)
})

function setAlertBoxMessage(msg: string) {
    alertBox.value = {
        message: msg,
        key: alertBox.value.key + 1,
    }
}

function createMap(options: MapOptions) {
    if (geojson.value == null) return

    closeMap()

    map = Leaflet.map(viewer.value as HTMLDivElement, options)

    geojson.value.addTo(map)

    map.on('zoomend', () => {
        updateLayers()
    })

    emit('map', map)
}

function closeMap() {
    if (map) {
        map.stop()
        map.remove()
        map = null

        emit('map', null)
    }
}

function processGeojsonObject(geojsonObj: GeoJSON.GeoJsonObject) {
    if (geojsonObj === null) return

    try {
        geojson.value = Leaflet.geoJSON(geojsonObj, {
            style: (feature: GeoJSON.Feature) => {
                return feature.properties?.styles
            },
            onEachFeature: (feature: GeoJSON.Feature, layer: Layer) => {
                createMapTextbox(feature, layer)
            },
        } as GeoJSONOptions)
    } catch (err) {
        console.error(err)
        setAlertBoxMessage(
            'Não foi possível processar o mapa! Acesse o log para ver mais informações.',
        )
    }
}

function updateLayers() {
    if (map === null) return
    if (geojson.value === null) return

    const currentZoom = map.getZoom()

    geojson.value.eachLayer((layer: Layer) => {
        if (!('feature' in layer && layer.feature)) return

        const maxZoom = (layer.feature as GeoJSON.Feature).properties?.maxZoom
        if (maxZoom && currentZoom > maxZoom) {
            map?.removeLayer(layer)
            return
        }

        if (maxZoom && currentZoom < maxZoom) {
            if (!map!.hasLayer(layer)) {
                map?.addLayer(layer)
            }
            return
        }

        const minZoom = (layer.feature as GeoJSON.Feature).properties?.minZoom
        if (minZoom && currentZoom < minZoom) {
            map?.removeLayer(layer)
            return
        }

        if (minZoom && currentZoom > minZoom) {
            if (!map!.hasLayer(layer)) {
                map?.addLayer(layer)
            }
            return
        }
    })
}

function createMapTextbox(feature: GeoJSON.Feature, layer: Layer) {
    if (!feature.properties?.textbox) return

    if (feature.geometry.type !== 'Polygon') {
        setAlertBoxMessage('A propriedade "textbox" é permitido apenas em "Polygons"')
        return
    }

    const styles = feature.properties?.textbox.styles

    layer.bindTooltip(feature.properties?.textbox.text, {
        permanent: true,
        direction: 'center',
        className: 'map-textbox',
    })

    layer.on('tooltipopen', () => {
        const tooltipElmt = layer.getTooltip()?.getElement()

        if (!tooltipElmt) return

        tooltipElmt.style.fontSize = `${styles.fontSize || 16}px`
        tooltipElmt.style.opacity = styles.opacity || 1
        tooltipElmt.style.color = styles.color || '#000'
    })

    layer.openTooltip()
}
</script>
