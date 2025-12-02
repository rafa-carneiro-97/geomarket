export class AStar {
    private navMesh: NavMesh

    constructor(navMesh: NavMesh) {
        this.navMesh = navMesh
    }

    private heuristic(start: Position, goal: Position): number {
        // Using Euclidean distance as the heuristic
        const dx = goal.lat - start.lat
        const dy = goal.lng - start.lng
        return Math.sqrt(dx * dx + dy * dy)
    }

    private reconstructPath(cameFrom: Map<id, Point>, current: Point): Point[] {
        const path: Point[] = [current]
        while (cameFrom.has(current.getIdentifier())) {
            current = cameFrom.get(current.getIdentifier())!
            path.unshift(current)
        }
        return path
    }

    public findPath(startId: id, goalId: id): Point[] {
        const startPoint = this.navMesh.getPointById(startId)
        const goalPoint = this.navMesh.getPointById(goalId)

        // Open and Closed lists
        const openList: Set<Point> = new Set([startPoint])
        const closedList: Set<Point> = new Set()

        // Costs and heuristics
        const gScore: Map<id, number> = new Map([[startId, 0]])
        const fScore: Map<id, number> = new Map([
            [startId, this.heuristic(startPoint.getPosition(), goalPoint.getPosition())],
        ])

        // To track the best path
        const cameFrom: Map<id, Point> = new Map()

        while (openList.size > 0) {
            // Get the point with the lowest fScore
            let current: Point | undefined = undefined
            let lowestFScore = Infinity
            openList.forEach((point) => {
                const score = fScore.get(point.getIdentifier()) || Infinity
                if (score < lowestFScore) {
                    lowestFScore = score
                    current = point
                }
            })

            if (!current) break

            if (current.getIdentifier() === goalId) {
                return this.reconstructPath(cameFrom, current)
            }

            openList.delete(current)
            closedList.add(current)

            for (const edge of current.getEdges()) {
                const neighbor = edge.end
                if (closedList.has(neighbor)) continue

                const tentativeGScore =
                    (gScore.get(current.getIdentifier()) || Infinity) + edge.cost

                if (!openList.has(neighbor)) {
                    openList.add(neighbor)
                } else if (tentativeGScore >= (gScore.get(neighbor.getIdentifier()) || Infinity)) {
                    continue
                }

                // This path is the best so far, record it
                cameFrom.set(neighbor.getIdentifier(), current)
                gScore.set(neighbor.getIdentifier(), tentativeGScore)
                fScore.set(
                    neighbor.getIdentifier(),
                    tentativeGScore +
                        this.heuristic(neighbor.getPosition(), goalPoint.getPosition()),
                )
            }
        }

        // If no path found, return an empty array
        return []
    }
}
