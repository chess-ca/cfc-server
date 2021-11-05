
const fs = require('fs');
const path = require('path');
const nodeResolve = require('@rollup/plugin-node-resolve');
const del = require('rollup-plugin-delete');
const scss = require('rollup-plugin-scss');
const { terser } = require('rollup-plugin-terser');
const sizes = require('rollup-plugin-sizes');

const src_dir = path.resolve(__dirname, '../../cfcserver/static-src');
const static_dir = path.resolve(__dirname, '../../cfcserver/static');
const built_config = require(src_dir+'/built.config.cjs');
const built_dir = path.resolve(static_dir, built_config.dest_dir);

const isDev = process.env.BUILD.toLowerCase().startsWith('dev');

const site_build = {
    input: {
        site: path.resolve(src_dir, 'main.bundle.rollup-entry.js')
    },
    output: {
        dir: built_dir,
        entryFileNames: '[name].js',
        globals: {},
        format: 'iife'
    },
    plugins: [
        nodeResolve.nodeResolve({
            moduleDirectories: ['x-dev/node_modules', 'node_modules']
        })
        ,del({
            targets: [built_dir],
            force: true, runOnce: true //, verbose: true
        })
        ,scss({
            output: path.resolve(built_dir, 'site.css'),
            outputStyle: isDev ? 'expanded' : 'compressed',
            // includePaths: ['../../../x-dev/node_modules']
            watch: src_dir+'/css'
        })
        ,isDev ? null : terser()
        ,sizes({details: false})
    ],
    watch: { include: 'cfcserver/static-src/**' }
};

module.exports = [site_build];
