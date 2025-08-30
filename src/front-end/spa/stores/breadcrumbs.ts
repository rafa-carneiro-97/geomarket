import { defineStore } from 'pinia'
import type { BreadcrumbItem } from '@/types/stores/breadcrumbs'

const BREADCRUMBS_ITEMS = 'breadcrumbsItems'

export const breadcrumbsStore = defineStore('breadcrumbs', {
    state: () => ({
        items: JSON.parse(
            sessionStorage.getItem(BREADCRUMBS_ITEMS) ?? '[]',
        ) as Array<BreadcrumbItem>,
    }),

    getters: {
        last: (state) => state.items.at(-1) ?? null,
    },

    actions: {
        push(item: BreadcrumbItem, dedupe = true) {
            item.link = item.link ?? window.location.pathname

            if (dedupe) {
                const last = this.items.at(-1)
                if (
                    last &&
                    last.label === item.label &&
                    JSON.stringify(last.link) === JSON.stringify(item.link)
                ) {
                    return
                }
            }

            this.items.push(item)
            sessionStorage.setItem(BREADCRUMBS_ITEMS, JSON.stringify(this.items))
        },

        reset() {
            sessionStorage.removeItem(BREADCRUMBS_ITEMS)
            this.$reset()
        },
    },
})
