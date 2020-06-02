
{{ cookiecutter.python_package_name | replace("-", "_") }}
=====================================

Version: |release|

{{cookiecutter.project_short_description}}


Quickstart
----------

To get started with {{ cookiecutter.python_package_name | replace("-", "_") }}, install with pip::

    pip install {{ cookiecutter.python_package_name | replace("-", "_") }}

or with conda::

    conda install {{ cookiecutter.python_package_name | replace("-", "_") }}


Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Installation and usage

   installing
   introduction

.. toctree::
   :maxdepth: 1

   examples/index


.. toctree::
   :maxdepth: 2
   :caption: Development

   develop-install


.. links

.. _`Jupyter widgets`: https://jupyter.org/widgets.html

.. _`notebook`: https://jupyter-notebook.readthedocs.io/en/latest/
