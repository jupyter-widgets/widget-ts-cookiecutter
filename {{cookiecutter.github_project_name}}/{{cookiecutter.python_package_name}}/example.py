#!/usr/bin/env python
# coding: utf-8

# Copyright (c) {{ cookiecutter.author_name }}.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode

module_name = "{{ cookiecutter.npm_package_name }}"
module_version = "{{ cookiecutter.npm_package_version }}"


class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = 'ExampleModel'
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _model_name = 'ExampleView'
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World')