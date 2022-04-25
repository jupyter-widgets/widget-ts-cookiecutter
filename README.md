# widget-ts-cookiecutter

![Github Actions Status](https://github.com/jupyter-widgets/widget-ts-cookiecutter/workflows/Build/badge.svg)

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a custom
Jupyter widget project.

## What is widget-ts-cookiecutter?

With **widget-ts-cookiecutter** you can create a custom Jupyter interactive
widget project with sensible defaults. widget-ts-cookiecutter helps custom widget
authors get started with best practices for the packaging and distribution
of a custom Jupyter interactive widget library.

## Usage

Install [cookiecutter](https://github.com/audreyr/cookiecutter):

    pip install cookiecutter

After installing cookiecutter, use widget-ts-cookiecutter:

    cookiecutter https://github.com/jupyter-widgets/widget-ts-cookiecutter.git

As widget-ts-cookiecutter runs, you will be asked for basic information about
your custom Jupyter widget project. You will be prompted for the following
information:

- `author_name`: your name or the name of your organization,
- `author_email`: your project's contact email,
- `github_project_name`: name of your custom Jupyter widget's GitHub repository,
- `github_organization_name`: name of your custom Jupyter widget's GitHub user or organization,
- `python_package_name`: name of the Python "back-end" package used in your custom widget.
- `npm_package_name`: name for the npm "front-end" package holding the JavaScript
  implementation used in your custom widget.
- `npm_package_version`: initial version of the npm package.
- `project_short_description` : a short description for your project that will
  be used for both the "back-end" and "front-end" packages.

After this, you will have a directory containing files used for creating a
custom Jupyter widget. To check that eveything is set up as it should be,
you should run the tests:

Create a dev environment:
```bash
conda create -n {{ cookiecutter.python_package_name }}-dev -c conda-forge nodejs yarn python jupyterlab
conda activate {{ cookiecutter.python_package_name }}-dev
```

Install the python. This will also build the TS package.

```bash
# First install the python package. This will also build the JS packages.
pip install -e ".[test, examples]"

# Run the python tests. This should not give you a few sucessful example tests
py.test

# Run the JS tests. This should again, only give TODO errors (Expected 'Value' to equal 'Expected value'):
yarn test
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```
jupyter labextension develop --overwrite .
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

Every time you make a change in the TypeScript code, you will need to rebuild it then refresh the browser page:

```
yarn run build
```


### How to see your changes
#### Typescript:
If you use JupyterLab to develop then you can watch the source directory and run JupyterLab at the same time in different
terminals to watch for changes in the extension's source and automatically rebuild the widget.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

## Releasing your initial packages:

- Add tests
- Ensure tests pass locally and on CI. Check that the coverage is reasonable.
- Make a release commit, where you remove the `, 'dev'` entry in `_version.py`.
- Update the version in `package.json`
- Relase the npm packages:
  ```bash
  npm login
  npm publish
  ```
- Install publish dependencies:
```bash
pip install build twine
```
- Build the assets and publish
  ```bash
  python -m build .
  twine check dist/*
  twine upload dist/*
  ```
- Tag the release commit (`git tag <python package version identifier>`)
- Update the version in `_version.py`, and put it back to dev (e.g. 0.1.0 -> 0.2.0.dev).
  Update the versions of the npm packages (without publishing).
- Commit the changes.
- `git push` and `git push --tags`.
