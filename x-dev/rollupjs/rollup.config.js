
import path from 'path';
import nodeResolve from '@rollup/plugin-node-resolve';
import del from 'rollup-plugin-delete';
import svelte from 'rollup-plugin-svelte';
import scss from 'rollup-plugin-scss';
import { terser } from 'rollup-plugin-terser';
import sizes from 'rollup-plugin-sizes';

const project_dir = path.resolve(__dirname, '../..');
const src_dir = path.resolve(project_dir, 'front-end');
const dest_dir = path.resolve(project_dir, 'cfcserver/static');

import built_config from './built.config.js';
const built_dir = path.resolve(dest_dir, built_config.dest_dir);

const isDev = process.env.BUILD.toLowerCase().startsWith('dev');

const site_build = {
    input: {
        site: path.resolve(src_dir, 'main.bundle.rollup-entry.js')
    },
    output: {
        dir: built_dir,
        entryFileNames: '[name].js',
        globals: {},
        // format: 'es',       // for downstream bundlers (Hugo pipes, etc)
        format: 'iife',     // for browser
    },
    plugins: [
        del({
            targets: [built_dir],
            force: true, runOnce: true //, verbose: true
        }),
        nodeResolve({
            moduleDirectories: ['x-dev/node_modules', 'node_modules']
        }),
        svelte({
            // include: path.resolve(src_dir, 'javascript/components/**/*.svelte'),
            emitCss: false,
            compilerOptions: {
                // customElement: true,
            }
        }),
        scss({
            output: path.resolve(built_dir, 'site.css'),
            outputStyle: isDev ? 'expanded': 'compressed',
            // includePaths: ['../../../x-dev/node_modules']
            watch: src_dir+'/css'
        }),
        terser(),
        (isDev) ? sizes({details: false}) : null
    ],
    watch: { clearScreen: false }
}

export default [site_build];
