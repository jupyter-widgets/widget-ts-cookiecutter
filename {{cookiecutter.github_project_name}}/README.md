
# {{ cookiecutter.github_project_name }}

[![Build Status](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }}.svg?branch=master)](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }})
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }})


{{ cookiecutter.project_short_description }}

## Installation

A typical installation requires the following three commands to be run:

```bash
pip install {{ cookiecutter.python_package_name  }}
jupyter nbextension install --py [--sys-prefix|--user|--system] {{ cookiecutter.python_package_name  }}
jupyter nbextension enable --py [--sys-prefix|--user|--system] {{ cookiecutter.python_package_name  }}
```

Or, if you use jupyterlab:

```bash
pip install {{ cookiecutter.python_package_name  }}
jupyter labextension install {{ cookiecutter.jlab_extension_name }}
```
