// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  JupyterLabPlugin, JupyterLab
} from '@jupyterlab/application';

import {
  Token
} from '@phosphor/coreutils';

import * as myCode from '{{ cookiecutter.npm_package_name }}';

import {
  INBWidgetExtension
 } from "@jupyter-widgets/jupyterlab-manager";


const EXTENSION_ID = '{{ cookiecutter.jlab_extension_id }}'


/**
 * The token identifying the JupyterLab plugin.
 */
export
const {{ cookiecutter.jlab_extension_interface_name }} = new Token<{{ cookiecutter.jlab_extension_interface_name }}>(EXTENSION_ID);

/**
 * The type of the provided value of the plugin in JupyterLab.
 */
export
interface {{ cookiecutter.jlab_extension_interface_name }} {
};


/**
 * The notebook diff provider.
 */
const exampleProvider: JupyterLabPlugin<{{ cookiecutter.jlab_extension_interface_name }}> = {
  id: EXTENSION_ID,
  requires: [INBWidgetExtension],
  activate: activateWidgetExtension,
  autoStart: true
};

export default exampleProvider;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: JupyterLab, widgetsManager: INBWidgetExtension): {{ cookiecutter.jlab_extension_interface_name }} {
  widgetsManager.registerWidget({
      name: 'jupyter-datawidgets',
      version: {{ cookiecutter.jlab_extension_interface_name }}.JUPYTER_EXTENSION_VERSION,
      exports: {{ cookiecutter.jlab_extension_interface_name }}
    });
  return {};
}
