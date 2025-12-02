export interface ProductInterface {
    id: number
    name: string
    barcode: string
    keywords: Array<string>
    photoUrl: string | null
    isActive: boolean
}
