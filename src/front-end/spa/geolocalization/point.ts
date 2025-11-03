export type id = string

export interface Position {
    lat: number
    lng: number
}

export interface Edge {
    start: Point
    end: Point
    cost: number
}

export class Point {
    private identifier: id
    private position: Position
    private edges = Array<Edge>()

    constructor(identifier: id, position: Position) {
        this.identifier = identifier
        this.position = position
    }

    public getPosition(): Position {
        return this.position
    }

    public getIdentifier(): id {
        return this.identifier
    }

    public getEdges(): Array<Edge> {
        return this.edges
    }

    public addEdge(endPoint: Point) {
        const cost = this.euclideanDistance(this.position, endPoint.position)

        this.edges.push({
            start: this,
            end: endPoint,
            cost: cost,
        })
    }

    private euclideanDistance(start: Position, end: Position): number {
        const dx = end.lat - start.lat
        const dy = end.lng - start.lng
        const result = Math.sqrt(dx * dx + dy * dy)
        return Math.round(result * 100) / 100
    }
}
