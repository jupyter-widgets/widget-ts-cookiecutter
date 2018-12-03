// Custom webpack rules
const rules = [
  { test: /\.ts$/, loader: 'ts-loader' },
  { test: /\.js$/, loader: 'source-map-loader' },
];

const version = require('./package.json').version;
const path = require('path');


const resolve = {
  // Add '.ts' and '.tsx' as resolvable extensions.
  extensions: [".webpack.js", ".web.js", ".ts", ".js"]
};

module.exports = [
  {
    // Notebook extension
    entry: './src/extension.ts',
    output: {
      filename: 'index.js',
      path: path.resolve(__dirname, '{{ cookiecutter.python_package_name }}', 'nbextension', 'static'),
      libraryTarget: 'amd'
    },
    module: {
      rules: rules
    },
    devtool: 'source-map',
    externals: ['@jupyter-widgets/base'],
    resolve,
  },

  {
    // embeddable bundle (e.g. for docs)
    entry: './src/index.ts',
    output: {
      filename: 'embed-bundle.js',
      path: path.resolve(__dirname, 'docs', 'source', '_static'),
      library: "{{ cookiecutter.npm_package_name }}",
      libraryTarget: 'amd'
    },
    module: {
      rules: rules
    },
    devtool: 'source-map',
    externals: ['@jupyter-widgets/base'],
    resolve,
  },
  {// Embeddable {{ cookiecutter.npm_package_name }} bundle
    //
    // This bundle is generally almost identical to the notebook bundle
    // containing the custom widget views and models.
    //
    // The only difference is in the configuration of the webpack public path
    // for the static assets.
    //
    // It will be automatically distributed by unpkg to work with the static
    // widget embedder.
    //
    // The target bundle is always `dist/index.js`, which is the path required
    // by the custom widget embedder.
    //
    entry: './src/index.ts',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'dist'),
        libraryTarget: 'amd',
        library: "{{ cookiecutter.npm_package_name }}",
        publicPath: 'https://unpkg.com/{{ cookiecutter.npm_package_name }}@' + version + '/dist/'
    },
    devtool: 'source-map',
    module: {
        rules: rules
    },
    externals: ['@jupyter-widgets/base'],
    resolve,
  }
];
