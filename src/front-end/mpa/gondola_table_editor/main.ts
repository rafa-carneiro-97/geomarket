import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import axiosPlugin from '@/plugins/axiosDefault'

document.querySelectorAll('div[role=gondola-table-editor]').forEach((item) => {
    if (item.hasAttribute('initialized')) return
    item.setAttribute('initialized', '')

    const props = {
        gondolaId: item.getAttribute('data-gondola-id'),
        establishmentId: item.getAttribute('data-establishment-id'),
    }

    const app = createApp(App, props)
    const pinia = createPinia()

    app.use(pinia)
    app.use(axiosPlugin)
    app.mount(item)
})
