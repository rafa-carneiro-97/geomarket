<template>
    <section>
        <AlertBox v-if="alertBox.message" :message="alertBox.message" :key="alertBox.key" />

        <AddGondolaProductAsync
            v-if="addGondolaProduct.key > 0"
            :yPosition="addGondolaProduct.yPosition"
            :xPosition="addGondolaProduct.xPosition"
            :key="addGondolaProduct.key"
            @addGondolaProduct="appendGondolaProduct"
        />

        <p v-if="isHidden" class="text-red-600">Error ao acessar os dados</p>

        <div
            v-if="!isHidden"
            class="flex w-full flex-row flex-nowrap overflow-auto rounded border border-black/10 bg-slate-100 p-4 inset-shadow-sm/15 inset-shadow-black"
        >
            <div class="table">
                <table class="border-separate border-spacing-4">
                    <tbody>
                        <tr v-for="row in maxY + 1" :key="row">
                            <td v-for="column in maxX + 1" :key="column">
                                <div
                                    draggable="true"
                                    @dragstart="onDragStart(column, row)"
                                    @dragover.prevent="onDragOverCell($event, column, row)"
                                    @dragleave="onDragLeaveCell()"
                                    @drop="onDropOnCell($event, column, row)"
                                    @dragend="onDragEnd()"
                                    class="relative flex aspect-8/14 h-full w-40 cursor-grab flex-col overflow-hidden rounded border border-black/20 bg-white shadow shadow-black/15 transition-all active:cursor-grabbing"
                                    :class="{
                                        'scale-95 ring-2 ring-indigo-300':
                                            dragKeyStart === generateCellKey(column, row),

                                        'scale-105 ring-2 ring-red-400':
                                            dropKeyTarget === generateCellKey(column, row),
                                    }"
                                >
                                    <template v-if="tableMap[`${column},${row}`]">
                                        <div class="relative">
                                            <img
                                                v-if="tableMap[`${column},${row}`].product.photoUrl"
                                                :src="
                                                    tableMap[`${column},${row}`].product
                                                        .photoUrl as string
                                                "
                                                alt="Imagem do produto"
                                                class="border-b border-black/10"
                                                draggable="false"
                                            />

                                            <div
                                                v-else
                                                class="flex aspect-square w-full items-center justify-center border-b border-black/10 bg-gray-200"
                                            >
                                                <Image
                                                    :stroke-width="1"
                                                    class="size-2/3 stroke-gray-300"
                                                />
                                            </div>

                                            <span
                                                v-if="
                                                    !tableMap[`${column},${row}`].product.isActive
                                                "
                                                class="absolute bottom-0 left-0 line-clamp-1 flex w-full flex-row flex-nowrap items-center justify-center border-t border-black/15 bg-orange-100 px-1 text-orange-800 opacity-80"
                                            >
                                                <TriangleAlert
                                                    :size="18"
                                                    class="mr-1 stroke-orange-800"
                                                />

                                                em análise
                                            </span>
                                        </div>

                                        <div class="flex flex-1 flex-col px-3 pb-2">
                                            <h3
                                                class="text-bolder line-clamp-2 pt-3 pb-1 text-center text-pretty"
                                            >
                                                {{ tableMap[`${column},${row}`].product.name }}
                                            </h3>

                                            <div
                                                class="flex flex-1 flex-row items-center justify-center gap-4"
                                            >
                                                <button
                                                    type="button"
                                                    @click="
                                                        removeProduct(tableMap[`${column},${row}`])
                                                    "
                                                    class="group mt-auto mb-4 cursor-pointer rounded-full border-2 border-red-400 p-1.5 transition-all hover:border-white hover:bg-red-600"
                                                >
                                                    <Trash2
                                                        :stroke-width="1.8"
                                                        :size="26"
                                                        class="stroke-red-400 group-hover:stroke-white"
                                                    />
                                                </button>
                                            </div>
                                        </div>

                                        <span
                                            class="absolute top-0 right-0 bg-gray-600 px-1 text-sm text-white opacity-60"
                                        >
                                            {{
                                                tableMap[`${column},${row}`].gondola.yPosition + 1
                                            }}-{{
                                                tableMap[`${column},${row}`].gondola.xPosition + 1
                                            }}
                                        </span>
                                    </template>

                                    <template v-else>
                                        <span
                                            class="absolute top-0 right-0 bg-gray-600 px-1 text-sm text-white opacity-60"
                                        >
                                            {{ row }}-{{ column }}
                                        </span>

                                        <div
                                            class="flex flex-1 flex-col items-center justify-center"
                                        >
                                            <div
                                                class="flex aspect-square w-full flex-col items-center justify-center"
                                            >
                                                <Package class="stroke-gray-300" />

                                                <p class="text-gray-300">Vazio</p>
                                            </div>

                                            <button
                                                type="button"
                                                @click="setAddGondolaProduct(column - 1, row - 1)"
                                                class="mt-auto mb-6 cursor-pointer rounded-full bg-blue-400 p-1.5 transition-all hover:scale-105 hover:bg-blue-600"
                                            >
                                                <Plus
                                                    :stroke-width="1.8"
                                                    :size="26"
                                                    class="stroke-white"
                                                />
                                            </button>
                                        </div>
                                    </template>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div class="mt-2 ml-3 flex flex-row items-center justify-start gap-6">
                    <button
                        @click="removeRow()"
                        type="button"
                        class="cursor-pointer rounded-full px-6 opacity-60 transition-all"
                        :class="{
                            'cursor-pointer bg-red-700 hover:scale-105 hover:opacity-100': maxY > 0,
                            'cursor-not-allowed bg-gray-500': maxY === 0,
                        }"
                    >
                        <ChevronUp />
                    </button>

                    <button
                        @click="createRow()"
                        type="button"
                        class="cursor-pointer rounded-full bg-green-600 px-6 opacity-60 transition-all hover:scale-105 hover:opacity-100"
                    >
                        <ChevronDown />
                    </button>
                </div>
            </div>

            <div class="mt-3 ml-2 flex flex-col items-center justify-start gap-6">
                <button
                    @click="removeColumn()"
                    type="button"
                    class="rounded-full py-6 opacity-60 transition-all"
                    :class="{
                        'cursor-pointer bg-red-700 hover:scale-105 hover:opacity-100': maxX > 0,
                        'cursor-not-allowed bg-gray-500': maxX === 0,
                    }"
                >
                    <ChevronLeft />
                </button>

                <button
                    @click="createColumn()"
                    type="button"
                    class="cursor-pointer rounded-full bg-green-600 py-6 opacity-60 transition-all hover:scale-105 hover:opacity-100"
                >
                    <ChevronRight />
                </button>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import {
    ref,
    reactive,
    computed,
    onBeforeMount,
    onUnmounted,
    defineAsyncComponent,
    watch,
    inject,
} from 'vue'
import axios from 'axios'
import {
    ChevronRight,
    ChevronLeft,
    ChevronUp,
    ChevronDown,
    Image,
    Package,
    Plus,
    Trash2,
    TriangleAlert,
} from 'lucide-vue-next'
import AlertBox from '@/components/alerts/AlertBox.vue'
import type { GondolaProductInterface } from '@/types/entities/gondola'

const establishmentId = inject('establishmentId')

const props = defineProps({
    gondolaId: {
        type: String,
        required: true,
    },
})

const emit = defineEmits<{
    (e: 'initialSize', size: number): void
    (
        e: 'result',
        value: { dataset: Array<GondolaProductInterface>; deleted: Array<GondolaProductInterface> },
    ): void
}>()

const AddGondolaProductAsync = defineAsyncComponent(
    () => import('@/components/gondola/forms/AddGondolaProduct.vue'),
)
let initialGondolaProducts = new Array<GondolaProductInterface>()
const alertBox = ref({ message: '', key: 0 })
const addGondolaProduct = ref({ key: 0, yPosition: -1, xPosition: -1 })
const tableData = ref<Array<GondolaProductInterface>>([])
const tableMap = computed(() => {
    const m: Record<string, GondolaProductInterface> = {}
    for (const item of tableData.value) {
        m[`${item.gondola.xPosition + 1},${item.gondola.yPosition + 1}`] = item
    }

    return m
})
const maxX = ref<number>(0)
const maxY = ref<number>(0)
const dragKeyStart = ref<string>('')
const dropKeyTarget = ref<string>('')
const drag = reactive({
    droppedOnTarget: false as boolean,
    position: {
        start: {
            x: null as null | number,
            y: null as null | number,
        },
    },
})
const isHidden = ref<boolean>(false)

onBeforeMount(() => {
    axios
        .get(`/api/establishment/${establishmentId}/gondola/${props.gondolaId}/products/`)
        .then((response) => {
            const data = response.data as Array<GondolaProductInterface>

            emit('initialSize', data.length)

            if (data.length === 0) return

            maxX.value = Math.max(...data.map((item) => item.gondola.xPosition))
            maxY.value = Math.max(...data.map((item) => item.gondola.yPosition))

            initialGondolaProducts = Array.from(data)
            tableData.value = Array.from(data)
        })
        .catch((error) => {
            isHidden.value = true
            console.error(error)
            setAlertBoxMessage(
                'Erro ao carregar os produtos da gôndola. Acesse o console para mais detalhes.',
            )
        })
})

onUnmounted(() => {
    initialGondolaProducts = []
})

watch(
    tableData,
    (newValue) => {
        const data = JSON.parse(JSON.stringify(newValue)) as Array<GondolaProductInterface>
        const ids = data.map((item) => item.id)
        const uniqueIds = new Set(ids.filter(Boolean))

        const deleted = initialGondolaProducts.filter((item) => {
            return item.id && !uniqueIds.has(item.id)
        })

        emit('result', {
            dataset: data,
            deleted: deleted,
        })
    },
    { deep: true },
)

function setAlertBoxMessage(msg: string) {
    alertBox.value = {
        message: msg,
        key: alertBox.value.key + 1,
    }
}

function setAddGondolaProduct(xPosition: number, yPosition: number) {
    const key = addGondolaProduct.value.key + 1
    addGondolaProduct.value = {
        key: key,
        xPosition: xPosition,
        yPosition: yPosition,
    }
}

function removeProduct(gondolaProduct: GondolaProductInterface) {
    const yPos = gondolaProduct.gondola.yPosition
    const xPos = gondolaProduct.gondola.xPosition

    const index = tableData.value.findIndex(
        (item) => item.gondola.xPosition === xPos && item.gondola.yPosition === yPos,
    )

    if (index !== -1) {
        tableData.value.splice(index, 1) // Removes the item at the found index
    }
}

function resetDrag() {
    drag.position = {
        start: {
            x: null,
            y: null,
        },
    }
}

function onDragStart(column: number, row: number) {
    const xPos = column - 1
    const yPos = row - 1
    dragKeyStart.value = `${xPos}-${yPos}`

    drag.position.start = {
        x: xPos,
        y: yPos,
    }

    console.debug(`Drag start position. X: ${drag.position.start.x}. Y: ${drag.position.start.y}`)
}

function onDragEnd() {
    dragKeyStart.value = ''
    dropKeyTarget.value = ''
    // dropped somewhere in the container but not on a cell: treat as cancel
    if (!drag.droppedOnTarget) resetDrag()
}

function onDragOverCell(event: DragEvent, column: number, row: number) {
    event.preventDefault()

    const key = generateCellKey(column, row)
    if (dragKeyStart.value !== key) dropKeyTarget.value = key
}

function onDragLeaveCell() {
    if (dropKeyTarget.value !== '') dropKeyTarget.value = ''
}

function generateCellKey(column: number, row: number): string {
    return `${column - 1}-${row - 1}`
}

function onDropOnCell(event: DragEvent, column: number, row: number) {
    const endXPos = column - 1
    const endYPos = row - 1
    event.preventDefault()

    console.debug(`Drag end position. X: ${endXPos}. Y: ${endYPos}`)

    if (drag.position.start.x === null || drag.position.start.y === null) {
        const msg = 'Não existe a informação da posição incial do elemento para arrasto.'
        console.info(msg)
        setAlertBoxMessage(msg)
        return
    }

    const startXPos = drag.position.start.x as number
    const startYPos = drag.position.start.y as number

    drag.droppedOnTarget = true

    if (startXPos === endXPos && startYPos === endYPos) {
        console.debug(
            `Drag canceled because ende position at the same cell. X: ${endXPos}. Y: ${endYPos}.`,
        )
        resetDrag()
        return
    }

    const newDataTable = new Array<GondolaProductInterface>()

    tableData.value.forEach((item) => {
        // create and object without the reactivity
        const obj = JSON.parse(JSON.stringify(item)) as GondolaProductInterface

        if (item.gondola.xPosition === startXPos && item.gondola.yPosition === startYPos) {
            obj.gondola.xPosition = endXPos
            obj.gondola.yPosition = endYPos
        }

        if (item.gondola.xPosition === endXPos && item.gondola.yPosition === endYPos) {
            obj.gondola.xPosition = startXPos
            obj.gondola.yPosition = startYPos
        }

        newDataTable.push(obj)
    })

    tableData.value = newDataTable
}

function createColumn() {
    maxX.value += 1
}

function removeColumn() {
    const minX = Math.max(...tableData.value.map((item) => item.gondola.xPosition))
    if (maxX.value > 0 && maxX.value > minX) {
        maxX.value -= 1
    }
}

function createRow() {
    maxY.value += 1
}

function removeRow() {
    const minY = Math.max(...tableData.value.map((item) => item.gondola.yPosition))
    if (maxY.value > 0 && maxY.value > minY) {
        maxY.value -= 1
    }
}

function appendGondolaProduct(gondolaProduct: GondolaProductInterface) {
    tableData.value.push(gondolaProduct)
}
</script>
