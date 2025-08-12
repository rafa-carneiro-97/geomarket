import { defineStore } from 'pinia'
import axios from 'axios'

const AUTH_STORAGE_NAMES = {
    token: 'authToken',
    // permissions : Array<string: string>
}

interface UserInfo {
    firstName: string
    lastName: string
    email: string
    isStaff: boolean
}

interface LoginDetail {
    username: string
    password: string
    stayConnected?: boolean
}

export const authStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem(AUTH_STORAGE_NAMES.token) || '',
        userInfo: null as UserInfo | null,
        // permissions: JSON.parse(localStorage.getItem('permissions') || '[]'),
    }),

    actions: {
        async validateToken(): Promise<boolean> {
            return axios.get('api/auth/token')
        },

        async login({ username, password, stayConnected = false }: LoginDetail) {
            return axios
                .post(
                    'api/login/form',
                    {
                        username: username,
                        password: password,
                        stay_connected: stayConnected,
                    },
                    {
                        withCredentials: true,
                    },
                )
                .then((response) => {
                    this.token = response.data.token

                    if (stayConnected === true) {
                        localStorage.setItem(AUTH_STORAGE_NAMES.token, this.token)
                    }
                })
        },

        logout() {
            this.userInfo = null
            localStorage.removeItem(AUTH_STORAGE_NAMES.token)
            this.token = ''
        },

        async fetchUserInfo() {
            if (this.userInfo === null) {
                await axios.get('api/auth/user/info').then((response) => {
                    this.userInfo = response.data
                })
            }
        },
    },
})
