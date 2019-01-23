import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';


export default {
    input: 'src/frontend/main.js',
    output: {
        name: 'HexchanJS',
        file: 'dev/frontend/scripts.js',
        format: 'iife',
        globals: {
            'jquery': '$',
            'underscore': '_',
            'js-cookie': 'Cookies',
            'lightbox2': 'lightbox',
        },
    },
    external: ['jquery', 'underscore', 'js-cookie', 'lightbox2'],
    plugins: [
        resolve(),
        commonjs(),
    ],
};
