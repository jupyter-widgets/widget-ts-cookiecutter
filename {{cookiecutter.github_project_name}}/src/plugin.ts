// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import * as yourCode from './example';

import {
  JUPYTER_EXTENSION_VERSION
} from './version';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';


const EXTENSION_ID = '{{ cookiecutter.jlab_extension_id }}';


/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: '{{ cookiecutter.npm_package_name }}',
    version: JUPYTER_EXTENSION_VERSION,
    exports: yourCode
  });
}
