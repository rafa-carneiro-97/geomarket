<template>
    <BaseMenu :items="items" />
</template>

<script lang="ts" setup>
import { LayoutGrid, LogOut } from 'lucide-vue-next'
import BaseMenu from '@/components/menu/BaseMenu.vue'

const items = [
    {
        text: 'Painel',
        location: { name: 'dashboard' },
        icon: LayoutGrid,
        addClass: 'stroke-red-400',
    },

    {
        text: 'Sair',
        location: { name: 'logout' },
        icon: LogOut,
        addClass: 'stroke-orange-400',
    },
]
</script>
