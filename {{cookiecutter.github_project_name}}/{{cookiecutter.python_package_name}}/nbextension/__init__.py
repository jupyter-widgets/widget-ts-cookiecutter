#!/usr/bin/env python
# coding: utf-8

# Copyright (c) {{ cookiecutter.author_name }}
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': '{{ cookiecutter.python_package_name }}',
        'require': '{{ cookiecutter.python_package_name }}/extension'
    }]
