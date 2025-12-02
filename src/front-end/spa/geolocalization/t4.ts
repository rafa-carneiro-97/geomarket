private euclideanDistance(a: Position, b: Position): number {
    const dx = b.lat - a.lat
    const dy = b.lng - a.lng
    return Math.sqrt(dx * dx + dy * dy)
}

private projectPointOnSegment(p: Position, a: Position, b: Position): Position {
    const ax = a.lat, ay = a.lng
    const bx = b.lat, by = b.lng
    const px = p.lat, py = p.lng

    const abx = bx - ax
    const aby = by - ay
    const apx = px - ax
    const apy = py - ay

    const abLenSquared = abx * abx + aby * aby

    if (abLenSquared === 0) return a // segmento de tamanho 0

    let t = (apx * abx + apy * aby) / abLenSquared

    // Clampa t entre 0 e 1 para garantir que a projeção está no segmento
    t = Math.max(0, Math.min(1, t))

    return {
        lat: ax + abx * t,
        lng: ay + aby * t
    }
}

private generateUserId(): id {
    return `user-${Math.random().toString(36).substring(2, 9)}`
}
