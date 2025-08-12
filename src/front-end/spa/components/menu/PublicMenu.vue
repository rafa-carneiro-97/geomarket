<template>
    <BaseMenu :items="items" />
</template>

<script lang="ts" setup>
import { MapPinHouse, LogIn } from 'lucide-vue-next'
import BaseMenu from '@/components/menu/BaseMenu.vue'

const items = [
    {
        text: 'Início',
        location: { name: 'home' },
        icon: MapPinHouse,
        addClass: 'stroke-red-400',
    },

    {
        text: 'Login',
        location: { name: 'login' },
        icon: LogIn,
        addClass: 'stroke-orange-400',
    },
]
</script>
