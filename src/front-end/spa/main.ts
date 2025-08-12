import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { createPinia } from 'pinia'
import axiosHeadersPlugin from '@/plugins/axiosHeaders'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(axiosHeadersPlugin)

app.mount('#app')
