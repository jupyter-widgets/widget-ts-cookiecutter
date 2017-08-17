var loaders = [
  { test: /\.ts$/, loader: 'ts-loader' },
  { test: /\.json$/, loader: 'json-loader' },
  { test: /\.js$/, loader: "source-map-loader" },
];

module.exports = {
  entry: './src/index.ts',
  output: {
    filename: 'index.js',
    path: __dirname + '/../../{{ cookiecutter.python_package_name }}/nbextension/static',
    libraryTarget: 'amd'
  },
  module: {
    loaders: loaders
  },
  devtool: 'source-map',
  externals: ['@jupyter-widgets/base'],
  resolve: {
    // Add '.ts' and '.tsx' as resolvable extensions.
    extensions: [".webpack.js", ".web.js", ".ts", ".js"]
  }
};
