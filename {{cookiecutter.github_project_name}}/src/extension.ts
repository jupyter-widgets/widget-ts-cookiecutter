// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.

const __body = document.querySelector('body');
// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const __db_url = __body!.getAttribute('data-base-url');
(window as any).__webpack_public_path__ = __db_url + 'nbextensions/{{ cookiecutter.python_package_name }}';

export * from './index';
