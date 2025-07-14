import fs from 'fs'
import path from 'path'
import esbuild from 'esbuild'
import { fileURLToPath, URL } from 'url'
import vuePlugin from 'esbuild-plugin-vue-next'

const style_plugin = {
    name: 'inline-style-plugin',
    setup({ onLoad }) {
        onLoad({ filter: /\.css$/ }, (args) => {
            const css = fs.readFileSync(args.path, 'utf8')
            return {
                contents:
                    `document.head.appendChild(document.createElement('style'))` +
                    `.appendChild(document.createTextNode(${JSON.stringify(css)}))`,
            }
        })
    },
}

const outdir_cleaner_plugin = {
    name: 'outdir-cleaner-plugin',
    setup({ onStart, initialOptions }) {
        onStart(function () {
            const dir = path.resolve(initialOptions.outdir)
            if (fs.existsSync(dir)) {
                fs.rmSync(dir, { recursive: true, force: true })
                console.log('\x1b[35m%s\x1b[0m', `🧹 Cleaning: ${dir}`)
            }
        })
    },
}

const logger_plugin = {
    name: 'logger-plugin',
    setup({ onStart, onEnd, initialOptions }) {
        let start_time
        onStart(function () {
            start_time = Date.now()
        })

        onEnd((result) => {
            const entryPoint = initialOptions.entryPoints[0]
            console.log('\n\x1b[36m%s\x1b[0m', entryPoint)

            if (result.warnings.length !== 0) {
                const warnings = JSON.stringify(result.warnings, null, 4)
                console.warn(`Warnings: ${warnings}`)
            }

            if (result.errors.length !== 0) {
                const erros = JSON.stringify(result.errors, null, 4)
                console.error(`Errors: ${erros}`)
                return
            }

            if (initialOptions.outfile) {
                const stat = fs.statSync(initialOptions.outfile)
                console.log('\x1b[34m%s\x1b[0m', `build finished: ${initialOptions.outfilet}`)
                console.log('\x1b[33m%s\x1b[0m', `Size: ${(stat.size / 1024).toFixed(1)} kb`)
            }

            const dir_path = initialOptions.outdir
            if (dir_path) {
                const files = fs.readdirSync(dir_path, {
                    withFileTypes: true,
                    recursive: true,
                })

                for (const item of files) {
                    const item_path = path.resolve(item.parentPath, item.name)
                    const stat = fs.statSync(item_path)
                    if (stat.isFile()) {
                        console.log('\x1b[34m%s\x1b[0m', `build finished: ${item_path}`)
                        console.log(
                            '\x1b[33m%s\x1b[0m',
                            `Size: ${(stat.size / 1024).toFixed(1)} kb`,
                        )
                    }
                }
            }

            console.log('\x1b[32m%s\x1b[0m', `Done in ${Date.now() - start_time} ms`)
        })
    },
}

const default_option = {
    tsconfig: '.\\tsconfig.json',
    bundle: true,
    minify: true,
    sourcemap: false,
    platform: 'browser',
    target: ['chrome90', 'firefox120'],
    format: 'esm',
    logLevel: 'silent',
    plugins: [style_plugin, logger_plugin],
}

const options = [
    {
        ...default_option,
        alias: {
            '@': fileURLToPath(new URL('.\\src\\front-end\\spa', import.meta.url)),
        },
        entryPoints: ['src\\front-end\\spa\\main.ts'],
        splitting: true,
        outdir: '.\\src\\back-end\\apps\\spa\\static\\spa\\_js\\index\\',
        publicPath: '/static/spa/_js/index',
        plugins: [...default_option.plugins, outdir_cleaner_plugin, vuePlugin()],
        entryNames: '[dir]/[name].min',
        chunkNames: 'bundled-chunks/[name]-[hash].min',
        assetNames: 'bundled-assets/[name]-[hash]',
        loader: {
            '.webp': 'file',
            '.png': 'file',
            '.jpg': 'file',
            '.svg': 'file',
        },
    },
]

options.forEach(function (item) {
    esbuild.context(item).then((context) => {
        context.watch()
    })
})
