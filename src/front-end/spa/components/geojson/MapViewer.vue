<template>
    <div>
        <AlertBox v-if="alertBox.message" :message="alertBox.message" :key="alertBox.key" />

        <div
            ref="viewer"
            style="height: 500px"
            class="relative w-full border border-b-0 border-black/20 bg-gray-200"
        >
            <TriangleAlert
                v-if="!props.data"
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
import AlertBox from '@/components/AlertBox.vue'
import { Navmesh } from '@/geolocalization/navmesh'
import type { NavmeshDrawer } from '@/geolocalization/drawer'

const props = defineProps({
    data: {
        type: String,
        required: true,
    },
    showNavmesh: {
        type: Boolean,
        required: true,
    },
})

const viewer = useTemplateRef<HTMLDivElement>('viewer')
let navmesh: Navmesh | null = new Navmesh()
let navmeshDrawer: NavmeshDrawer | null = null
const OUTER_DISTANCE = 20
let map: Map | null = null

onBeforeUnmount(() => {
    closeMap()
    navmesh = null
    navmeshDrawer = null
})

onMounted(async () => {
    try {
        const parsed = JSON.parse(props.data)
        processViewerData(parsed.viewer)
        processNavmeshData(parsed.navmesh)
    } catch (err) {
        console.error(err)
        setAlertBoxMessage('Dados do mapa inválido! Acesse o log para ver mais informações.')
    }

    if (props.showNavmesh) {
        const drawer = await getNavmeshDrawer()
        drawer?.draw()
    }
})

const alertBox = ref({ message: '', key: 0 })
const geojson = ref<GeoJSON | null>(null)

watch(geojson, (newValue) => {
    if (newValue == null) return

    closeMap()

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

    map = Leaflet.map(viewer.value as HTMLDivElement, options)
    newValue.addTo(map)
    map.on('zoomend', () => {
        updateLayers()
    })
})

watch(
    () => props.showNavmesh,
    async (newValue, oldValue) => {
        if (newValue === true || (newValue === false && oldValue === true)) {
            const drawer = await getNavmeshDrawer()
            if (newValue === true) {
                drawer?.draw()
            } else {
                drawer?.remove()
            }
        }
    },
)

async function getNavmeshDrawer(): Promise<NavmeshDrawer | null> {
    if (navmeshDrawer !== null) {
        return navmeshDrawer
    }

    try {
        const module = await import('@/geolocalization/drawer')
        const drawer = new module.NavmeshDrawer(map as Map, navmesh as Navmesh)
        navmeshDrawer = drawer
    } catch (err) {
        console.error(err)
        if (err instanceof Error) setAlertBoxMessage(err.message)
    } finally {
        return navmeshDrawer
    }
}

function setAlertBoxMessage(msg: string) {
    alertBox.value = {
        message: msg,
        key: alertBox.value.key + 1,
    }
}

function processViewerData(data: GeoJSON.GeoJsonObject) {
    try {
        geojson.value = Leaflet.geoJSON(data, {
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
            'Não foi possível processar a visualização do mapa! Acesse o log para ver mais informações.',
        )
    }
}

function processNavmeshData(
    data: Array<{ id: string; pos: [number, number]; edges: Array<string> }>,
) {
    try {
        data.forEach((item) => {
            navmesh?.addPoint(item.id, {
                lat: item.pos[0],
                lng: item.pos[1],
            })
        })

        data.forEach((item) => {
            item.edges.forEach((edge) => {
                navmesh?.addEdge(item.id, edge)
            })
        })
    } catch (err) {
        console.error(err)
        setAlertBoxMessage(
            'Não foi possível processar a área de navegação do mapa! Acesse o log para ver mais informações.',
        )
    } finally {
        console.debug(navmesh?.toString())
    }
}

function closeMap() {
    if (map) {
        map.stop()
        map.remove()
        map = null
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
