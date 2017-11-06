// Copyright (c) {{ cookiecutter.author_name }}.
// Distributed under the terms of the Modified BSD License.

var childProcess = require('child_process');
var fs = require('fs-extra');
var path = require('path');


// Pack the lab extension to a tarball for release.
var here = path.resolve('.');
var target = path.join(
  here,
  '{{cookiecutter.python_package_name}}',
  'labextension');

fs.ensureDir(target);

// This also runs the build script because of the `prepack` script.
childProcess.execSync('npm pack ' + here, {
  cwd: target,
  stdio: [0, 1, 2]
});
