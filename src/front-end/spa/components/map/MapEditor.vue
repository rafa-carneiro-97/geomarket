<template>
    <div>
        <AlertBox v-if="alertBox.message" :message="alertBox.message" :key="alertBox.key" />

        <MapViewer :geojsonObject="geojsonObject" @map="(v) => (map = v)" />

        <div role="setup" class="bg-gray-600">
            <div class="checkbox">
                <label class="flex items-center justify-center hover:bg-transparent">
                    <input type="checkbox" v-model="showNavmesh" />
                    Mostrar navegação
                </label>
            </div>
        </div>

        <div style="max-height: 400px; overflow-y: auto">
            <div role="editor" class="relative">
                <textarea
                    ref="textarea"
                    spellcheck="false"
                    @scroll="syncLeftScroll()"
                    @input="(updateHighlight(), syncLeftScroll())"
                    @keydown="editorActions"
                ></textarea>

                <pre
                    ref="pre"
                    class="line-numbers"
                ><code ref="code" class="language-json"></code></pre>
            </div>
        </div>

        <button
            role="apply"
            type="button"
            @click="updateMapViewer()"
            class="btn btn-green mt-2 ml-auto"
        >
            Aplicar
        </button>
    </div>
</template>

<script lang="ts" setup>
import { ref, useTemplateRef, onMounted, onBeforeUnmount, watch } from 'vue'
import Prism from 'prismjs'
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/plugins/line-highlight/prism-line-highlight'
import 'prismjs/plugins/line-highlight/prism-line-highlight.css'
import 'prismjs/components/prism-json'
import 'prismjs/themes/prism-tomorrow.css' // Theme
import prettier from 'prettier/standalone'
import type { Options as PrettierOptions } from 'prettier'
import { type Plugin } from 'prettier'
import * as pluginESTree from 'prettier/plugins/estree'
import * as pluginBabel from 'prettier/plugins/babel'
import type { Map } from 'leaflet'
import AlertBox from '@/components/alerts/AlertBox.vue'
import MapViewer from '@/components/map/MapViewer.vue'
import { MeshData, Navmesh } from '@/geolocalization/navmesh'
import { NavmeshDrawer } from '@/geolocalization/drawer'

const props = defineProps({
    initialData: {
        type: String,
        required: true,
    },
})

const emit = defineEmits<{
    (e: 'compressedData', payload: string): void
}>()

const showNavmesh = ref<boolean>(true)
const alertBox = ref({ message: '', key: 0 })
const textarea = useTemplateRef<HTMLTextAreaElement>('textarea')
const pre = useTemplateRef<HTMLElement>('pre')
const code = useTemplateRef<HTMLElement>('code')
const geojsonObject = ref<GeoJSON.GeoJsonObject | null>(null)
const map = ref<Map | null>(null)
let navmesh: Navmesh | null = new Navmesh()
let navmeshDrawer: NavmeshDrawer | null = null

onMounted(() => {
    const textareaElmt = textarea.value as HTMLTextAreaElement
    textareaElmt.value = props.initialData
    updateMapViewer()
    prettifyTextarea()
})

onBeforeUnmount(() => {
    navmesh = null
    navmeshDrawer = null
})

watch(showNavmesh, (newValue) => {
    if (newValue) {
        navmeshDrawer?.draw()
    } else {
        navmeshDrawer?.remove()
    }
})

watch(map, (newValue) => {
    if (newValue === null) {
        navmeshDrawer = null
        return
    }

    navmeshDrawer = new NavmeshDrawer(newValue as Map, navmesh as Navmesh)

    if (showNavmesh.value) {
        navmeshDrawer.draw()
    } else {
        navmeshDrawer.remove()
    }
})

function setAlertBoxMessage(msg: string) {
    alertBox.value = {
        message: msg,
        key: alertBox.value.key + 1,
    }
}

function editorActions(event: KeyboardEvent) {
    const textareaElmt = textarea.value as HTMLTextAreaElement
    const text = textareaElmt.value

    const beforeCursor = text.substring(0, textareaElmt.selectionStart)
    const afterCursor = text.slice(textareaElmt.selectionEnd, textareaElmt.value.length)
    const currentLine = beforeCursor.substring(beforeCursor.lastIndexOf('\n') + 1)

    switch (event.key) {
        case 'Tab': {
            event.preventDefault()
            textareaElmt.value = `${beforeCursor}\t${afterCursor}`
            const position = beforeCursor.length + 1
            textareaElmt.setSelectionRange(position, position)
            break
        }

        case 'Enter':
            event.preventDefault()
            // Match leading whitespace (spaces and/or tabs)
            const indentMatch = currentLine.match(/^[ \t]*/)
            const indent = indentMatch ? indentMatch[0] : ''
            const insertion = `\n${indent}`
            textareaElmt.value = `${beforeCursor}${insertion}${afterCursor}`
            const position = beforeCursor.length + insertion.length
            textareaElmt.setSelectionRange(position, position)
            break
        case 's':
            if (!(event.ctrlKey || event.metaKey)) return
            event.preventDefault()
            updateMapViewer()
            break

        case 'p':
            if (!(event.ctrlKey || event.metaKey)) return
            event.preventDefault()
            prettifyTextarea()
            break
    }

    updateHighlight()
}

function prettifyTextarea() {
    const textareaElmt = textarea.value as HTMLTextAreaElement
    try {
        prettier
            .format(textareaElmt.value, {
                parser: 'json',
                plugins: [pluginESTree as Plugin, pluginBabel],
                tabWidth: 4,
                printWidth: 60,
            } as PrettierOptions)
            .then((formatted) => {
                textareaElmt.value = formatted
                updateHighlight()
            })
    } catch (err) {
        console.error(err)
    } finally {
        updateHighlight()
    }
}

function updateHighlight() {
    let text = textarea.value?.value as string
    text = text.replace(/&/g, '&amp;')
    text = text.replace(/</g, '&lt')
    text = text.replace(/>/g, '&gt;')

    if (text[text.length - 1] == '\n') text += ' '

    const codeElmt = code.value as HTMLElement
    codeElmt.innerHTML = text

    Prism.highlightElement(codeElmt, false, () => {
        let depth = 0
        const colors = ['#5c90bb', '#e06c75', '#98c379', '#c678dd']

        requestAnimationFrame(() => {
            codeElmt.querySelectorAll('span.token.punctuation').forEach((node) => {
                const text = node.textContent
                const elmt = node as HTMLElement

                if (text === '{' || text === '[') {
                    depth += 1
                    elmt.style.color = colors[(depth - 1) % colors.length]
                }

                if (text === '}' || text === ']') {
                    elmt.style.color = colors[(depth - 1) % colors.length]
                    depth -= 1
                }
            })
        })
    })
}

function syncLeftScroll() {
    pre.value!.scrollLeft = textarea.value!.scrollLeft
}

function updateMapViewer() {
    const text = textarea.value?.value as string
    let parsed: object | null = null

    try {
        parsed = JSON.parse(text)
    } catch (err) {
        console.error(err)
        setAlertBoxMessage(
            `Não foi possível aplicar as alterações na visualização do. Acesse o log para ver mais informações.`,
        )
        return
    }

    if (parsed === null) return
    const compressed = JSON.stringify(parsed, null)
    emit('compressedData', compressed)

    if ('viewer' in parsed) {
        geojsonObject.value = parsed.viewer as GeoJSON.GeoJsonObject
    }

    if ('meshData' in parsed) {
        try {
            processMeshData(parsed.meshData as Array<MeshData>)
        } catch (err) {
            console.error(err)
            setAlertBoxMessage(
                'Não foi possível processar a área de navegação do mapa! Acesse o log para ver mais informações.',
            )
            return
        }
    }
}

function processMeshData(data: Array<MeshData>) {
    data.forEach((item) => {
        navmesh?.addPoint(item.id, {
            lat: item.pos[0],
            lng: item.pos[1],
        })
    })

    data.forEach((item) => {
        item.edges?.forEach((edge) => {
            navmesh?.addEdge(item.id, edge)
        })
    })

    console.debug(navmesh?.toString())
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@100..700&display=swap');

div[role='editor'] {
    &:deep(*) {
        margin: 0;
        padding: 0;
        tab-size: 4;
        font-family: 'Roboto Mono', monospace;
        font-size: 1em;
        line-height: 1.5;
    }

    &:deep(textarea),
    &:deep(pre) {
        padding: 0 0 12px 58px;
        min-height: 280px;
    }

    &:deep(textarea) {
        position: absolute;
        overflow-y: hidden;
        color: transparent;
        top: -1px;
        left: -1px;
        bottom: 0;
        right: 0;
        z-index: 2;
        resize: none;
        background: transparent;
        caret-color: #eefd16;
        white-space: nowrap;
    }

    &:deep(.line-numbers .line-numbers-rows) {
        position: absolute;
        top: 3px;
        left: 0;
        pointer-events: none;
        font-size: 100%;
        width: 50px;
        letter-spacing: -1px;
        border-right: 1px solid #359ac9;
        user-select: none;
    }

    &:deep(.line-numbers-rows > span) {
        display: block;
        counter-increment: linenumber;
    }

    &:deep(.line-numbers-rows > span:before) {
        content: counter(linenumber);
        color: #359ac9;
        display: block;
        padding-right: 0.8em;
        text-align: right;
        background: #2d2d2d;
    }
}
</style>
