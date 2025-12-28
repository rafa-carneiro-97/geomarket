import { createApp } from 'vue'
import App from './App.vue'

const mapElmt = document.getElementById('map') as HTMLDivElement

const props = {
    locatorId: mapElmt.getAttribute('data-locator-id'),
    establishmentId: mapElmt.getAttribute('data-establishment-id'),
}

createApp(App, props).mount(mapElmt)
