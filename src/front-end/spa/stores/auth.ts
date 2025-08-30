import { defineStore } from 'pinia'
import axios from 'axios'
import { employeeStore } from '@/stores/employee'
import { breadcrumbsStore } from '@/stores/breadcrumbs'

import type { UserInfo, LoginDetail } from '@/types/stores/auth'

const AUTH_TOKEN_NAME = 'authToken'

export const authStore = defineStore('auth', {
    state: () => ({
        token:
            localStorage.getItem(AUTH_TOKEN_NAME) || sessionStorage.getItem(AUTH_TOKEN_NAME) || '',
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
                    sessionStorage.setItem(AUTH_TOKEN_NAME, this.token)

                    if (stayConnected === true) {
                        localStorage.setItem(AUTH_TOKEN_NAME, this.token)
                    }
                })
        },

        logout() {
            sessionStorage.removeItem(AUTH_TOKEN_NAME)
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
