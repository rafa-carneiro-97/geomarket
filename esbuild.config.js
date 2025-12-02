import fs from 'fs'
import path from 'path'
import { fileURLToPath, URL } from 'url'
import esbuild from 'esbuild'
import vuePlugin from 'esbuild-plugin-vue-next'
import dotenv from 'dotenv'

const isDevMode = process.argv.includes('--dev')

function envPlugin(path) {
    if (!fs.existsSync(path)) {
        throw new Error(`The .env path "${path}" does not exists`)
    }

    const parsed = dotenv.parse(fs.readFileSync(path))

    return {
        name: 'env',
        setup({ onResolve, onLoad }) {
            // Intercept import paths called "env" and tag them with the "env-ns" namespace.
            onResolve({ filter: /^env$/ }, (args) => {
                return {
                    path: args.path,
                    namespace: 'env-ns',
                    external: false,
                }
            })

            function parseEnvValue(value) {
                if (value === 'true') return true
                if (value === 'false') return false
                if (!isNaN(value)) return Number(value)
                return value
            }

            // Load paths tagged with the "env-ns" namespace.
            onLoad({ filter: /.*/, namespace: 'env-ns' }, () => {
                const processed = Object.fromEntries(
                    Object.entries(parsed).map(([key, value]) => {
                        return [key, parseEnvValue(value)]
                    }),
                )

                return {
                    contents: JSON.stringify(processed),
                    loader: 'json',
                }
            })
        },
    }
}

const stylePlugin = {
    name: 'style',
    setup({ onLoad }) {
        onLoad({ filter: /\.css$/ }, (args) => {
            const css = fs.readFileSync(args.path, 'utf8')
            return {
                contents: `
                    document.head.appendChild(document.createElement('style')).appendChild(
                        document.createTextNode(${JSON.stringify(css).replaceAll(/\\n/g, ' ')})
                    )
                `,
            }
        })
    },
}

const outdirCleanerPlugin = {
    name: 'outdir-cleaner',
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

const loggerPlugin = {
    name: 'logger',
    setup({ onStart, onEnd, initialOptions }) {
        let startTime
        onStart(function () {
            startTime = Date.now()
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

            const dirPath = initialOptions.outdir
            if (dirPath) {
                const files = fs.readdirSync(dirPath, {
                    withFileTypes: true,
                    recursive: true,
                })

                for (const item of files) {
                    const itemPath = path.resolve(item.parentPath, item.name)
                    const stat = fs.statSync(itemPath)
                    if (stat.isFile()) {
                        console.log('\x1b[34m%s\x1b[0m', `build finished: ${itemPath}`)
                        console.log(
                            '\x1b[33m%s\x1b[0m',
                            `Size: ${(stat.size / 1024).toFixed(1)} kb`,
                        )
                    }
                }
            }

            console.log('\x1b[32m%s\x1b[0m', `Done in ${Date.now() - startTime} ms`)
        })
    },
}

const defaultOption = {
    charset: 'utf8',
    tsconfig: '.\\tsconfig.json',
    bundle: true,
    minify: true,
    sourcemap: isDevMode,
    platform: 'browser',
    target: ['chrome90', 'firefox120'],
    format: 'esm',
    logLevel: 'silent',
    plugins: [
        stylePlugin,
        loggerPlugin,
        outdirCleanerPlugin,
        envPlugin('src\\front-end\\spa\\.env'),
        vuePlugin(),
    ],
    splitting: true,
    entryNames: '[dir]\\[name].min',
    chunkNames: 'bundled-chunks\\[name]-[hash].min',
    assetNames: 'bundled-assets\\[name]-[hash]',
    alias: {
        '@': fileURLToPath(new URL('.\\src\\front-end\\spa', import.meta.url)),
    },
    loader: {
        '.webp': 'file',
        '.png': 'file',
        '.jpg': 'file',
        '.svg': 'file',
    },
}

const entries = [
    // SPA
    {
        ...defaultOption,
        entryPoints: ['src\\front-end\\spa\\main.ts'],
        outdir: '.\\src\\back-end\\apps\\spa\\static\\spa\\_js\\index\\',
        publicPath: '/static/spa/_js/index',
    },

    // MPA
    {
        ...defaultOption,
        entryPoints: ['src\\front-end\\mpa\\image\\crop\\main.ts'],
        outdir: 'src\\back-end\\apps\\core\\static\\core\\_js\\widgets\\image_cropper\\bundled\\',
    },

    {
        ...defaultOption,
        entryPoints: ['src\\front-end\\mpa\\map_editor\\main.ts'],
        outdir: 'src\\back-end\\apps\\business\\static\\business\\_js\\widgets\\map_editor\\bundled\\',
    },

    {
        ...defaultOption,
        entryPoints: ['src\\front-end\\mpa\\gondola_table_editor\\main.ts'],
        outdir: 'src\\back-end\\apps\\business\\static\\business\\_js\\widgets\\gondola_table_editor\\bundled\\',
    },
]

entries.forEach(function (item) {
    esbuild.context(item).then((context) => {
        context.watch()
    })
})
