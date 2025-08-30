import { type LucideIcon } from 'lucide-vue-next'

export interface Option {
    icon?: { component: LucideIcon; class?: string }
    identifier: string
    value: string
}
