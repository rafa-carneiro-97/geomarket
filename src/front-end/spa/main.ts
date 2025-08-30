import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { createPinia } from 'pinia'
import axiosPlugin from '@/plugins/axiosDefault'
import chartPlugin from '@/plugins/chartDefault'
import gsapPlugin from '@/plugins/gsapDefault'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.use(axiosPlugin)
app.use(chartPlugin)
app.use(gsapPlugin)

app.mount('#app')
