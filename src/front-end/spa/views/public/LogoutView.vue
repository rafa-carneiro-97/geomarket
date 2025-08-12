<script setup lang="ts">
import { authStore } from '@/stores/auth'

authStore().logout()
window.location.href = 'servidor/sair'
</script>
