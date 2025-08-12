<template>
    <div
        class="relative flex min-h-dvh flex-row-reverse items-center justify-center bg-green-400/70"
    >
        <div class="p-4">
            <h1 class="text-shadow text-center font-bold text-white">
                <span class="text-8xl">404</span>
                <span class="-mt-4 block text-xl"> Página não encontrada. </span>
            </h1>

            <RouterLink :to="{ name: 'home' }" class="btn btn-red mx-auto mt-8">
                Voltar para o início
            </RouterLink>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" class="max-w-sm">
            <g fill="#fff">
                <path
                    d="M132.6 317.5c-1.9.5-3.6 1.3-5.2 2.3-7.3 5-1.4 10.3.7 15.8 7.5 19.6-40.9 16.6-46.8 33.5-2.4 6.8-.4 14.6 5.1 20.1 4.8 4.8 11.8 7.6 18.9 9.7 32.8 9.5 72.4 9.2 106.9 10.5 41 1.5 82.3 2.2 123.3 1 6.7-.2 13.6-.5 19.9-2.6 6.3-2.1 11.9-6.4 13.1-11.8 3.1-13.3-19.4-24.5-14.8-37.5 3.8-10.8 20.1-11.6 30.6-15.3 6.4-2.3 12.6-5.7 15.6-10.9 16.9-28.4-57.7-30.5-74.8-30.3-30.2.3-59.9 5.2-89.9 7.1-32.5 2.1-66 1.4-97.8 7.4-1.6.2-3.2.5-4.8 1"
                />

                <path
                    d="M435.6 465.7c4.7 1.5 10.5 1.6 15.9 1.7 3.2 0 6.4.1 9.6.1 4.4.1 9.2 0 12.6-1.5 1.2-.6 2.2-1.4 2.3-2.2.2-2-3.9-3.2-7.5-3.4-9.3-.7-15.7-4.4-25.6-2.8-6.3.9-16.7 5.1-7.3 8.1"
                />
            </g>

            <path fill="#f1fbfe" d="M272.4 473.6V168.4l151.7-16.7v302.6z" />

            <path
                fill="#c2e8f8"
                d="M211.6 131.5l60.8 36.9v305.2l-60.8-42.5zm177.8-51.2l-177.8 51.2L242 92.9z"
            />
            <path
                fill="#f0f9fc"
                d="M388.2 56.2c-.5-9.5-8.7-16.8-18.2-16.2l-112 7.4c-9 .6-16 8.1-16 17.1v28.4l147.5-12.5-1.3-24.2z"
            />

            <path fill="#99c9da" d="M315.6 97.7l-104 33.8 60.8 36.9z" />

            <path fill="#e4f5f9" d="M272.4 168.4L242 92.9l147.4-12.6 34.7 71.4z" />

            <path fill="#5f4b8b" d="M404.1 264.7 301.8 276.4V182.3L404.1 170.6Z" />

            <path
                fill="#7367a4"
                d="M216.3 161.2V169.4L266.6 198.5V190.1ZM216.3 383.9V392.1L266.6 421.2V412.8Z"
            />

            <g fill="#fff">
                <path d="M399.1 259.1l-92.3 10.6V188l92.3-10.5v19.6z" />

                <path fill="#aa9dce" d="M399.1 184.8l-92.3 10.5V188l92.3-10.5v1.5z" />

                <path
                    d="M312.9 191.5c0 .8-.6 1.5-1.4 1.6s-1.4-.5-1.4-1.3.6-1.5 1.4-1.6c.8-.1 1.4.5 1.4 1.3m5.6-.6c0 .8-.6 1.5-1.4 1.6-.8.1-1.4-.5-1.4-1.3s.6-1.5 1.4-1.6c.8-.1 1.4.4 1.4 1.3m5.7-.7c0 .8-.6 1.5-1.4 1.6-.8.1-1.4-.5-1.4-1.3s.6-1.5 1.4-1.6c.8-.1 1.4.5 1.4 1.3"
                />
            </g>

            <g>
                <g ref="milk-face-eyes" fill="#4f3e7c">
                    <circle cx="375.3" cy="215.6" r="5" />
                    <circle cx="330.9" cy="220" r="5" />
                </g>

                <path
                    ref="mouth"
                    fill="none"
                    stroke="#4f3e7c"
                    stroke-linecap="round"
                    stroke-miterlimit="10"
                    stroke-width="4"
                    d="M341.1 240.5s15.4 10.5 27.3-3.5"
                />
            </g>

            <path
                fill="#4f3e7c"
                d="m337 401c9.8109-1.8282 16.9407-2.9273 24.9281-4.3612l-.1193 24.4046C361.789 421.8402 360 423 359 423c-6.4162 1.6345-13.0564 2.7837-19.7029 3.8755-.6146.1009-1.3682-.645-2.0573-.9978zm2.5277-8.1234c-1.5277.1234-2.3314-1.6553-2.3855-2.468-.8151-12.2465 1.0002-23.6701 9.9539-33.0667l20.4196-22.3785C386 308 340 296 327.4892 330.6967c-.4671 1.665-2.5325 3.8866-4.0723 4.0723l-21.1204 1.4304C303 296 356 280 377.2455 290.376 394 295 407 321 391.7255 339.3951c-7.0983 9.5926-15.7344 18.0422-23.6327 27.0502-3.7564 4.2843-6.5812 8.8503-6.2001 15.0735.3943 6.4399-.8213 7.3614-7.3521 8.4962l-15.0129 2.861"
            />
        </svg>
    </div>
</template>

<script lang="ts" setup>
import { useTemplateRef, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { gsap } from 'gsap'

const groupMilkEyes = useTemplateRef<SVGElement>('milk-face-eyes')
const mouth = useTemplateRef<SVGElement>('mouth')
let blinkTl: gsap.core.Timeline | null = null
let mouthTl: gsap.core.Timeline | null = null

onUnmounted(() => {
    blinkTl?.kill()
    blinkTl = null

    mouthTl?.kill()
    mouthTl = null
})

onMounted(() => {
    const circles = groupMilkEyes.value?.querySelectorAll('circle') as NodeListOf<SVGCircleElement>
    blinkTl = gsap.timeline({
        repeat: -1,
        repeatDelay: 4,
        yoyo: true,
        defaults: { ease: 'none' },
    })
    blinkTl.to(circles, {
        duration: 0.1,
        scaleY: 0,
        transformOrigin: 'center',
        repeat: 1,
        yoyo: true,
    })

    mouthTl = gsap.timeline({
        repeat: -1,
        repeatDelay: 6,
        yoyo: true,
    })

    mouthTl.to(mouth.value, {
        duration: 2,
        morphSVG: { shape: 'M338.4 239.8l32-3.9' },
        ease: 'back.out(1.7)',
    })
})
</script>
