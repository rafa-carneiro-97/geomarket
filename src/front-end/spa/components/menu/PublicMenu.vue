<template>
    <MenuLayout>
        <template #nav>
            <MenuItem
                label="Início"
                :location="{ name: 'home' }"
                :icon="MapPinHouse"
                class="stroke-red-300"
            ></MenuItem>

            <MenuItem
                label="Cria conta"
                :location="{ name: 'user-add' }"
                :icon="UserPlus"
                class="stroke-green-300"
            ></MenuItem>

            <MenuItem
                label="Login"
                :location="{ name: 'login' }"
                :icon="LogIn"
                class="stroke-orange-300"
            ></MenuItem>
        </template>
    </MenuLayout>
</template>

<script lang="ts" setup>
import { MapPinHouse, LogIn, UserPlus } from 'lucide-vue-next'
import MenuLayout from '@/components/menu/MenuLayout.vue'
import MenuItem from '@/components/menu/MenuItem.vue'
</script>
