class AStar {
    navMesh: NavMesh

    constructor(navMesh: NavMesh) {
        this.navMesh = navMesh
    }

    heuristic(a: Node, b: Node): number {
        // Use Manhattan distance as heuristic for grid-based pathfinding
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y)
    }

    findPath(start: Node, goal: Node): Node[] {
        const openList: Node[] = []
        const closedList: Set<Node> = new Set()
        const cameFrom: Map<Node, Node | null> = new Map()

        const gScore: Map<Node, number> = new Map()
        const fScore: Map<Node, number> = new Map()

        gScore.set(start, 0)
        fScore.set(start, this.heuristic(start, goal))

        openList.push(start)

        while (openList.length > 0) {
            // Find the node with the lowest fScore
            openList.sort((a, b) => (fScore.get(a)! < fScore.get(b)! ? -1 : 1))
            const current = openList.shift()!

            if (current === goal) {
                // Reconstruct path
                const path: Node[] = []
                let currentNode: Node | null = current
                while (currentNode !== null) {
                    path.unshift(currentNode)
                    currentNode = cameFrom.get(currentNode) || null
                }
                return path
            }

            closedList.add(current)

            for (const neighbor of current.neighbors) {
                if (closedList.has(neighbor)) continue

                const tentativeGScore = (gScore.get(current) || Infinity) + 1

                if (!openList.includes(neighbor)) openList.push(neighbor)

                if (tentativeGScore >= (gScore.get(neighbor) || Infinity)) continue

                cameFrom.set(neighbor, current)
                gScore.set(neighbor, tentativeGScore)
                fScore.set(neighbor, tentativeGScore + this.heuristic(neighbor, goal))
            }
        }

        return [] // No path found
    }
}

const navMesh = new NavMesh()
navMesh.generateGrid(5, 5) // Generate a 5x5 grid

const start = navMesh.getNodeById('0,0')
const goal = navMesh.getNodeById('4,4')

if (start && goal) {
    const astar = new AStar(navMesh)
    const path = astar.findPath(start, goal)
    console.log('Path found:', path.map((node) => `${node.x},${node.y}`).join(' -> '))
} else {
    console.log('Start or Goal not found')
}
