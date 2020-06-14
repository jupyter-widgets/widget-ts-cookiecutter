
# {{ cookiecutter.github_project_name }}

[![Build Status](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }}.svg?branch=master)](https://travis-ci.org/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name  }})
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name  }})


{{ cookiecutter.project_short_description }}

## Installation

You can install using `pip`:

```bash
pip install {{ cookiecutter.python_package_name  }}
```

Or if you use jupyterlab:

```bash
pip install {{ cookiecutter.python_package_name  }}
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] {{ cookiecutter.python_package_name  }}
```

## Development Installation


```bash
# First install the python package. This will also build the JS packages.
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension install .
```

For classic notebook, you can run:

```
jupyter nbextension install --sys-prefix --symlink --overwrite --py <your python package name>
jupyter nbextension enable --sys-prefix --py <your python package name>
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### How to see your changes
#### Typescript:
To continuously monitor the project for changes and automatically trigger a rebuild, start Jupyter in watch mode:
```bash
jupyter lab --watch
```
And in a separate session, begin watching the source directory for changes:
```bash
npm run watch
```

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.