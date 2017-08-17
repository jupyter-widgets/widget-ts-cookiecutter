// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  JupyterLabPlugin, JupyterLab
} from '@jupyterlab/application';

import {
  Token
} from '@phosphor/coreutils';

import * as yourCode from '{{ cookiecutter.npm_package_name }}';

import {
  INBWidgetExtension
 } from "@jupyter-widgets/jupyterlab-manager";


const EXTENSION_ID = '{{ cookiecutter.jlab_extension_id }}'


/**
 * The token identifying the JupyterLab plugin.
 */
export
const IExampleExtension = new Token<IExampleExtension>(EXTENSION_ID);

/**
 * The type of the provided value of the plugin in JupyterLab.
 */
export
interface IExampleExtension {
};


/**
 * The notebook diff provider.
 */
const exampleProvider: JupyterLabPlugin<IExampleExtension> = {
  id: EXTENSION_ID,
  requires: [INBWidgetExtension],
  activate: activateWidgetExtension,
  autoStart: true
};

export default exampleProvider;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: JupyterLab, widgetsManager: INBWidgetExtension): IExampleExtension {
  widgetsManager.registerWidget({
      name: '{{ cookiecutter.npm_package_name }}',
      version: yourCode.JUPYTER_EXTENSION_VERSION,
      exports: yourCode
    });
  return {};
}
