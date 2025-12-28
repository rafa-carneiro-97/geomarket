<template>
    <section
        ref="section"
        class="fixed top-0 left-0 flex h-dvh w-full items-center justify-center overflow-auto bg-black/80 py-12 will-change-[opacity]"
        style="z-index: 9999"
    >
        <div class="mx-auto overflow-hidden rounded border bg-gray-100 pb-6" style="max-width: 98%">
            <button
                aria-label="Fechar"
                type="button"
                class="ml-auto table cursor-pointer pb-1 pl-1"
            >
                <X
                    :size="36"
                    :strokeWidth="2"
                    aria-label="Fechar"
                    @click="(emit('confirmed'), hide())"
                    class="boder-l ml-auto cursor-pointer stroke-gray-400 p-1 hover:stroke-black"
                />
            </button>

            <p
                class="max-w-sm px-3 text-center text-lg text-balance break-normal hyphens-auto text-black"
            >
                {{ props.message }}
            </p>

            <button
                aria-label="Fechar"
                type="button"
                @click="(emit('confirmed'), hide())"
                class="btn btn-blue mx-auto mt-5"
            >
                Confirmar
            </button>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { useTemplateRef, onMounted, watch } from 'vue'
import { X } from 'lucide-vue-next'
import { gsap } from 'gsap'

onMounted(() => {
    show()
})

const props = defineProps({
    message: {
        type: String,
        required: true,
    },
})

const section = useTemplateRef<HTMLElement>('section')

const emit = defineEmits<{
    (e: 'confirmed', payload: void): void
}>()

watch(
    () => props.message,
    () => {
        show()
    },
)

const show = () => {
    gsap.from(section.value, {
        duration: 0.5,
        opacity: 0,
    })
}

const hide = () => {
    const sectionElmt = section.value as HTMLElement

    gsap.to(sectionElmt, {
        duration: 0.5,
        opacity: 0,
        onComplete: () => {
            sectionElmt.style.display = 'none'
        },
    })
}
</script>
