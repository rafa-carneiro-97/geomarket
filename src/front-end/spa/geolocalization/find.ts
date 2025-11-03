import type { Edge, Point, Position, id } from '@/geolocalization/point'
import type { NavMesh } from '@/geolocalization/navmesh'

export class AStar {
    private navMesh: NavMesh

    constructor(navMesh: NavMesh) {
        this.navMesh = navMesh
    }

    private heuristic(start: Point, goal: Point): number {
        // Using Euclidean distance as the heuristic
        const dx = goal.getPosition().lat - start.getPosition().lat
        const dy = goal.getPosition().lng - start.getPosition().lng
        return Math.sqrt(dx * dx + dy * dy)
    }
}
