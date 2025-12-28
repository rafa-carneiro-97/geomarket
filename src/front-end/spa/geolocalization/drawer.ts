import Leaflet from 'leaflet'
import type { Map } from 'leaflet'
import type { Navmesh } from '@/geolocalization/navmesh'
import type { Point, Edge } from '@/geolocalization/point'
import './drawer.css'

export class NavmeshDrawer {
    private map: Map
    private navmesh: Navmesh

    constructor(map: Map, navmesh: Navmesh) {
        this.map = map
        this.navmesh = navmesh

        this.map.createPane('edge')
        this.map.getPane('edge')!.style.zIndex = '1000'

        this.map.createPane('point')
        this.map.getPane('point')!.style.zIndex = '1001'

        this.map.createPane('point-info')
        this.map.getPane('point-info')!.style.zIndex = '1002'

        this.map.createPane('edge-cost')
        this.map.getPane('edge-cost')!.style.zIndex = '1003'

        this.map.getPane('popupPane')!.style.zIndex = '1010'
    }

    public draw() {
        this.navmesh.getPoints().forEach((point) => {
            point.getEdges().forEach((edge) => {
                this.drawEdge(edge)
            })
        })

        this.navmesh.getPoints().forEach((point) => {
            this.drawPoints(point)
        })
    }

    public remove() {
        const panesToRemove = ['edge', 'point', 'edge-cost', 'point-info']

        this.map.eachLayer((layer) => {
            const pane = layer.options?.pane
            if (pane && panesToRemove.includes(pane)) {
                this.map.removeLayer(layer)
            }
        })
    }

    private drawEdge(edge: Edge): void | Error {
        const startIdenfier = edge.start.getIdentifier()
        const endIdenfier = edge.end.getIdentifier()

        const startPosition = edge.start.getPosition()
        const endPosition = edge.end.getPosition()

        const id = `edge ${startIdenfier} to ${endIdenfier}`
        const invertedId = `edge ${endIdenfier} to ${startIdenfier}`

        let isBidirecional: boolean = false

        const coords = [
            [startPosition.lng, startPosition.lat],
            [endPosition.lng, endPosition.lat],
        ] as Leaflet.LatLngExpression[]

        this.map.eachLayer((layer) => {
            if (layer.options && 'id' in layer.options) {
                if (layer.options.id === id) {
                    throw new Error(`O navmesh possui uma redundância: ${id}`)
                }

                if (layer.options.id === invertedId) {
                    isBidirecional = true
                    this.map.removeLayer(layer)
                }
            }
        })

        const line = new Leaflet.Polyline(coords, {
            id: id,
            color: isBidirecional ? '#2b7fff' : '#ff6467',
            pane: 'edge',
            weight: 3,
            opacity: 1,
            smoothFactor: 0.1,
            renderer: Leaflet.svg({ padding: 1000 }), // large padding = no clipping effect
        } as Leaflet.PolylineOptions)

        line.bindTooltip(`${edge.cost}`, {
            permanent: true,
            direction: 'center',
            pane: 'edge-cost',
            className: 'map-drawer-edge-cost',
        })

        line.addTo(this.map)
    }

    private drawPoints(point: Point) {
        const position = point.getPosition()
        const id = point.getIdentifier()

        const circle = new Leaflet.CircleMarker([position.lng, position.lat], {
            pane: 'point',
            radius: 6,
            color: 'transparent',
            fillColor: '#000',
            fillOpacity: 1,
            renderer: Leaflet.svg({ padding: 1000 }), // large padding = no clipping effect
        })

        circle.bindTooltip(id, {
            pane: 'point-info',
            permanent: true,
            direction: 'top',
            className: 'map-drawer-point',
        })

        circle.bindPopup(`Latitude: ${position.lat} <br> Lontitude: ${position.lng}`)

        circle.addTo(this.map)
    }
}
