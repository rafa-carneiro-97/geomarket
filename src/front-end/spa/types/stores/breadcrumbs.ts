import { type LucideIcon } from 'lucide-vue-next'

export interface BreadcrumbItem {
    icon?: LucideIcon | null
    label: string
    link?: string
}
