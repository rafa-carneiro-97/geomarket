// Function to compute the projection of point P onto the line defined by points A and B
function projectPointOntoEdge(P, A, B) {
    const AB = { x: B.x - A.x, y: B.y - A.y }
    const AP = { x: P.x - A.x, y: P.y - A.y }

    const AB_AB = AB.x * AB.x + AB.y * AB.y // (B-A)·(B-A)
    const AP_AB = AP.x * AB.x + AP.y * AB.y // (P-A)·(B-A)

    const t = AP_AB / AB_AB

    // Projection point calculation
    let projection
    if (t < 0) {
        projection = { x: A.x, y: A.y } // Snap to A
    } else if (t > 1) {
        projection = { x: B.x, y: B.y } // Snap to B
    } else {
        projection = {
            x: A.x + t * AB.x,
            y: A.y + t * AB.y,
        }
    }

    return projection
}

// Function to calculate distance between two points
function distance(P1, P2) {
    return Math.sqrt((P2.x - P1.x) ** 2 + (P2.y - P1.y) ** 2)
}

// Function to find the closest edge to the current position
function findClosestEdge(P, edges) {
    let closestEdge = edges[0]
    let minDistance = Number.MAX_VALUE

    // Find closest edge by projecting P onto each edge and checking distance
    for (const edge of edges) {
        const projection = projectPointOntoEdge(P, edge.A, edge.B)
        const dist = distance(P, projection)

        if (dist < minDistance) {
            minDistance = dist
            closestEdge = edge
        }
    }

    return closestEdge
}

// Example usage:
const P = { x: 3, y: 1.5 } // Your current position
const edges = [
    { A: { x: 0, y: 0 }, B: { x: 3, y: 0 }, weight: 3 }, // A to B
    { A: { x: 3, y: 0 }, B: { x: 6, y: 0 }, weight: 3 }, // B to C
    { A: { x: 6, y: 0 }, B: { x: 6, y: 2 }, weight: 2 }, // C to D
    { A: { x: 6, y: 2 }, B: { x: 0, y: 2 }, weight: 6 }, // D to E
    { A: { x: 0, y: 2 }, B: { x: 0, y: 0 }, weight: 2 }, // E to A
]

const closestEdge = findClosestEdge(P, edges)
console.log(closestEdge)
