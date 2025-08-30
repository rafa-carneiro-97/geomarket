import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import type { EstablishmentInfo } from '@/types/stores/employee'

export const employeeStore = defineStore('employee', {
    state: () => ({
        establishment: {
            id: null as number | null,
            info: null as EstablishmentInfo | null,
        },
    }),

    actions: {
        async getEstablishmentInfo(): Promise<EstablishmentInfo | void> {
            if (!this.establishment.id) {
                router.push({
                    name: 'unauthorized',
                    query: {
                        error: `Identificador do estabelecimento não informado.`,
                    },
                })
            }

            if (this.establishment.info !== null) {
                return this.establishment.info
            }

            return await axios
                .get(`/api/establishment/${this.establishment.id}/`)
                .then((response) => {
                    this.establishment.info = {
                        name: response.data.name,
                        address: response.data.address,
                    }

                    return this.establishment.info
                })
                .catch(() => {
                    router.push({
                        name: 'unauthorized',
                        query: {
                            error: `O servidor negou o acesso as informações do estabelecimento (${this.establishment.id}).`,
                        },
                    })
                })
        },

        reset() {
            this.$reset()
        },
    },
})
