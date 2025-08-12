import { watch } from 'vue'
import axios from 'axios'
import router from '@/router'
import { authStore } from '@/stores/auth'

function getCSRFToken(): string {
    const input = document.querySelector('input[name=csrfmiddlewaretoken]') as HTMLInputElement

    if (input == null) {
        throw new Error('Csrf token not found')
    }

    return input.value
}

export default {
    install() {
        const auth = authStore()

        watch(
            () => auth.token,
            (newToken) => {
                if (newToken) {
                    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
                    sessionStorage.setItem('authToken', newToken)
                } else {
                    delete axios.defaults.headers.common['Authorization']
                    sessionStorage.removeItem('authToken')
                }
            },
            { immediate: true },
        )

        axios.defaults.headers.common['X-CSRFToken'] = getCSRFToken()
        axios.defaults.headers.common['Content-Type'] = 'application/x-www-form-urlencoded'

        axios.interceptors.response.use(
            (response) => {
                return response
            },
            (error) => {
                if (error.response.status === 401) {
                    auth.logout()
                    router.push({
                        name: 'unauthorized',
                        query: { error: error.response.data.error },
                    })
                }

                return Promise.reject(error)
            },
        )
    },
}
