<template>
    <section
        ref="section"
        class="fixed top-0 left-0 flex h-dvh w-full items-center justify-center overflow-auto bg-black/80 py-12 will-change-[opacity]"
        style="z-index: 9999"
    >
        <div class="mx-auto w-11/12 max-w-md overflow-hidden rounded border bg-gray-100 p-3">
            <div class="py-4 text-center text-lg text-balance break-normal hyphens-auto text-black">
                {{ props.message }}
            </div>

            <button
                aria-label="Fechar"
                type="button"
                @click="(emit('confirmed'), hide())"
                class="btn btn-blue mx-auto"
            >
                Confirmar
            </button>
        </div>
    </section>
</template>

<script lang="ts" setup>
import { useTemplateRef, onMounted, watch } from 'vue'
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
