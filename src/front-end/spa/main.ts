import { createApp } from 'vue'
import FontAwesomeIcon from '@/fonteAwsome'
import App from '@/App.vue'
import router from '@/router'
import axiosHeadersPlugin from '@/plugins/axiosHeaders'

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)

app.use(axiosHeadersPlugin)
app.use(router)

app.mount('#app')
