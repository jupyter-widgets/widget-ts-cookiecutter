
# {{ cookiecutter.github_project_name }}

[![Build Status](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }}.svg?branch=master)](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }})
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }})


{{ cookiecutter.project_short_description }}

## Installation

A typical installation requires the following commands to be run:

```bash
pip install {{ cookiecutter.python_package_name  }}
jupyter nbextension enable --py [--sys-prefix|--user|--system] {{ cookiecutter.python_package_name  }}
```

Or, if you use jupyterlab:

```bash
pip install {{ cookiecutter.python_package_name  }}
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
