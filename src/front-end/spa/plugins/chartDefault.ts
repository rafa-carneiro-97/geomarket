import { Chart, PieController, ArcElement, Tooltip, Legend } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

export default {
    async install() {
        Chart.register(PieController, ArcElement, Tooltip, Legend, ChartDataLabels)

        // Set global defaults for Chart.js
        Chart.defaults.responsive = true

        Chart.defaults.plugins.tooltip.enabled = true

        Object.assign(Chart.defaults.plugins.legend, {
            position: 'top',
            align: 'start',
            fullSize: true,
            labels: {
                boxWidth: 12,
                boxHeight: 12,
                padding: 16,
                font: {
                    size: 16,
                },
            },
        })

        if (Chart.defaults.plugins.datalabels) {
            Object.assign(Chart.defaults.plugins.datalabels, {
                color: '#fff',
                font: {
                    weight: '400',
                    size: 14,
                },
            })
        }
    },
}
