import { defineStore } from 'pinia'
import axios from 'axios'
import { employeeStore } from '@/stores/employee'
import { breadcrumbsStore } from '@/stores/breadcrumbs'

import type { UserInfo, LoginDetail } from '@/types/stores/auth'

const AUTH_TOKEN_NAME = 'authToken'

const cookieAuth = {
    createToken(token: string) {
        document.cookie = `${AUTH_TOKEN_NAME}=${token}; Path=/; Secure; SameSite=Lax`
    },

    getTokenValue(): string {
        const cookies = `; ${document.cookie}`
        const parts = cookies.split(`${AUTH_TOKEN_NAME}=`)

        if (parts.length !== 2) return ''

        const value = parts.pop()!.split(';').shift() || ''

        return value
    },

    deleteToken() {
        document.cookie = `${AUTH_TOKEN_NAME}=; Path=/; Max-Age=0;`
    },
}

export const authStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem(AUTH_TOKEN_NAME) || cookieAuth.getTokenValue() || '',
        userInfo: null as UserInfo | null,
    }),

    actions: {
        async validateToken(): Promise<boolean> {
            return axios
                .get('/api/auth/token/validate')
                .then((response) => {
                    if (response.status === 204) {
                        return true
                    }

                    return false
                })
                .catch(() => {
                    return false
                })
        },

        async login({ username, password, stayConnected = false }: LoginDetail) {
            return axios
                .post(
                    '/api/login/form',
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

                    cookieAuth.createToken(this.token)

                    if (stayConnected === true) {
                        localStorage.setItem(AUTH_TOKEN_NAME, this.token)
                    }
                })
        },

        logout() {
            cookieAuth.deleteToken()
            localStorage.removeItem(AUTH_TOKEN_NAME)
            this.$reset()
            employeeStore().reset()
            breadcrumbsStore().reset()
        },

        async fetchInfo() {
            if (this.userInfo === null) {
                await axios.get('/api/auth/user/info').then((response) => {
                    this.userInfo = response.data
                })
            }

            return this.userInfo
        },
    },
})
