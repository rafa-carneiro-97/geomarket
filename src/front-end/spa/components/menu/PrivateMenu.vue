<template>
    <MenuLayout>
        <template #nav>
            <MenuItem
                label="Estabelecimentos"
                :location="{ name: 'establishments' }"
                :icon="ClipboardList"
                class="stroke-red-400"
            ></MenuItem>

            <div>
                <span class="mt-3 block w-full text-center text-white/30">Atacadão</span>

                <MenuList
                    label="Funcionários"
                    :icon="Users"
                    :links="[
                        { text: 'Home', location: { name: 'establishments' } },
                        { text: 'Home', location: { name: 'home' } },
                        { text: 'Home', location: { name: 'home' } },
                    ]"
                />

                <MenuList
                    label="Funcionários"
                    :icon="Users"
                    :links="[
                        { text: 'Home', location: { name: 'home' } },
                        { text: 'Home', location: { name: 'home' } },
                        { text: 'Home', location: { name: 'home' } },
                    ]"
                />
            </div>

            <span class="mt-3 block w-full text-center text-white/30">Configurações</span>

            <MenuItem
                label="Sua conta"
                :location="{ name: 'establishments' }"
                :icon="User"
                class="stroke-white"
            ></MenuItem>

            <MenuItem
                label="Sair"
                :location="{ name: 'logout' }"
                :icon="LogOut"
                class="stroke-orange-400"
            ></MenuItem>
        </template>
    </MenuLayout>
</template>

<script lang="ts" setup>
import { ClipboardList, LogOut, User, Users } from 'lucide-vue-next'
import MenuLayout from '@/components/menu/MenuLayout.vue'
import MenuItem from '@/components/menu/MenuItem.vue'
import MenuList from '@/components/menu/MenuList.vue'
</script>
