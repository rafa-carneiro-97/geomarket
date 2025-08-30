<template>
    <nav
        aria-label="Breadcrumb"
        class="mx-auto mb-6 flex w-11/12 max-w-6xl flex-wrap items-center gap-2"
    >
        <BreadcrumbItem
            :icon="ClipboardList"
            label="Início"
            :link="{ name: 'establishments' }"
            :isLast="items.length === 0"
        />

        <template v-for="(crumb, index) in items" :key="index">
            <BreadcrumbItem
                :icon="crumb.icon ?? undefined"
                :label="crumb.label"
                :link="crumb.link as string"
                :isLast="index === items.length - 1"
                @activate="activatedCrumb(index)"
            />
        </template>
    </nav>
</template>

<script lang="ts" setup>
import { ClipboardList } from 'lucide-vue-next'
import { breadcrumbsStore } from '@/stores/breadcrumbs'
import BreadcrumbItem from '@/components/breadcrumbs/BreadcrumbItem.vue'

const breadcrumbs = breadcrumbsStore()

const items = breadcrumbs.items

function activatedCrumb(index: number) {
    breadcrumbs.items = breadcrumbs.items.slice(0, index + 1)
}
</script>
