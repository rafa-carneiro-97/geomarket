import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import axiosPlugin from '@/plugins/axiosDefault'

const elmt = document.getElementById('info') as HTMLDivElement

const props = {
    locatorId: elmt.getAttribute('data-locator-id'),
    establishmentId: elmt.getAttribute('data-establishment-id'),
}

const app = createApp(App, props)
const pinia = createPinia()

app.use(pinia)
app.use(axiosPlugin)
app.mount(elmt)
