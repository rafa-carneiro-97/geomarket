import type { ProductInterface } from '@/types/entities/product'

export interface GondolaProductInterface {
    id?: string
    gondola: {
        xPosition: number
        yPosition: number
    }
    product: ProductInterface
}
