import { Point, type Edge, type Position, type id } from '@/geolocalization/point'

export interface MeshData {
    id: id
    pos: [number, number]
    edges?: Array<id>
}

export class Navmesh {
    private points = new Map<id, Point>()

    public addPoint(id: id, position: Position): Point {
        const point = new Point(id, position)
        this.points.set(id, point)
        return point
    }

    public getPoints(): typeof this.points {
        return this.points
    }

    public addEdge(fromId: string, toId: string): void {
        if (fromId === toId) {
            throw new Error(`Invalid edge. The poins area the same:"${fromId}" = "${toId}"`)
        }

        const startPoint = this.getPointById(fromId)
        const endPoint = this.getPointById(toId)

        startPoint.addEdge(endPoint)
    }

    public projectUserPosition(position: Position) {
        let minDistance = Infinity
        let closestEdge: Edge | null = null
        let closestProjection: Position | null = null

        this.points.forEach((point: Point) => {
            point.getEdges().forEach((edge: Edge) => {
                const projection = this.projectPositionOntoEdge(position, edge)

                if (projection.distance < minDistance) {
                    minDistance = projection.distance
                    closestEdge = edge
                    closestProjection = projection.projected
                }
            })
        })

        console.log('Edge: ' + closestEdge)
        console.log('Projection: ' + closestProjection)
    }

    private getPointById(id: string): Point {
        const point = this.points.get(id)

        if (!point) throw Error(`Point "${id}" not found in the NavMesh.`)

        return point
    }

    public toString(): string {
        let data = 'NavMesh Visualization:\n'

        this.points.forEach((point: Point) => {
            const edges = point.getEdges()
            const pointId = point.getIdentifier()
            data += `Point "${pointId}":\n`
            edges.forEach((edge: Edge) => {
                const identifier = `${edge.start.getIdentifier()} to ${edge.end.getIdentifier()}`
                data += `    Edge  "${identifier}". Cost: ${edge.cost}\n`
            })
        })

        return data
    }

    private projectPositionOntoEdge(
        position: Position,
        edge: Edge,
    ): { projected: Position; distance: number } {
        const ax = edge.start.getPosition().lat
        const ay = edge.start.getPosition().lng
        const bx = edge.end.getPosition().lat
        const by = edge.end.getPosition().lng
        const px = position.lat
        const py = position.lng

        const abx = bx - ax
        const aby = by - ay
        const apx = px - ax
        const apy = py - ay

        const abLenSquared = abx * abx + aby * aby

        if (abLenSquared === 0) {
            // Segment with size 0

            const dx = px - ax
            const dy = py - ay
            return {
                projected: { lat: ax, lng: ay },
                distance: Math.sqrt(dx * dx + dy * dy),
            }
        }

        let t = (apx * abx + apy * aby) / abLenSquared

        t = Math.max(0, Math.min(1, t))

        const projLat = ax + abx * t
        const projLng = ay + aby * t

        const dx = px - projLat
        const dy = py - projLng

        return {
            projected: { lat: projLat, lng: projLng },
            distance: Math.sqrt(dx * dx + dy * dy),
        }
    }
}
