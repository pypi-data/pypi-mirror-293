import resolve from '@rollup/plugin-node-resolve';
import pkg from './package.json' with { type: 'json' };

export default {
    input: "./tdoc/common/js/tdoc-editor.js",
    output: {
        dir: './tdoc/common/static/',
        // file: pkg.browser,
        format: 'es'
    },
    plugins: [resolve()]
};
