import { watch } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ScrollSmoother, ScrollToPlugin, MorphSVGPlugin } from 'gsap/all'

export default {
    install() {
        gsap.registerPlugin(ScrollTrigger, ScrollSmoother, ScrollToPlugin, MorphSVGPlugin)

        watch(
            () => document.body.scrollHeight,
            (newValue, oldValue) => {
                if (newValue === oldValue) return

                // Refresh all scroll triggers
                ScrollTrigger.getAll().forEach((item) => {
                    item.refresh()
                })
            },
        )
    },
}
