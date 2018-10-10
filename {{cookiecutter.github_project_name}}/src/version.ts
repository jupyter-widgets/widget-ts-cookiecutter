// Copyright (c) {{ cookiecutter.author_name }}.
// Distributed under the terms of the Modified BSD License.

const data = require('../package.json');

/**
 * The current package version.
 */
export const MODULE_VERSION = data.version;

/*
 * The current package name.
 */
export const MODULE_NAME = data.name;
