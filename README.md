# opinionated-widget-cookiecutter
#### A cookiecutter template for creating a custom Jupyter widget project

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for a custom
Jupyter widget project.

## What is widget-cookiecutter?

With **widget-cookiecutter** you can create a custom Jupyter interactive
widget project with sensible defaults. widget-cookiecutter helps custom widget
authors get started with best practices for the packaging and distribution
of a custom Jupyter interactive widget library.

## Usage

Install [cookiecutter](https://github.com/audreyr/cookiecutter):

    $ pip install cookiecutter

After installing cookiecutter, use the widget-cookiecutter:

    $ cookiecutter https://github.com/jupyter-widgets/opinionated-widget-cookiecutter.git

As widget-cookiecutter runs, you will be asked for basic information about
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
- `jlab_extension_id`: extension ID to supply to JupyterLab when registering the extension.
  The recommended format is "jupyter.extensions.<Your UNIQUE designator here>".
- `project_short_description` : a short description for your project that will
  be used for both the "back-end" and "front-end" packages.

After this, you will have a directory containing files used for creating a
custom Jupyter widget. To check that eveything is set up as it should be,
you should run the tests:

```bash
# First install the python package. This will also build the JS packages.
pip install -e .

# Run the python tests. This should not give you a few sucessful example tests
py.test

# Run the JS tests. This should again, only give TODO errors (Expected 'Value' to equal 'Expected value'):
cd ts
npm test
```


## Releasing your initial packages:

- Add tests
- Ensure tests pass locally and on CI. Check that the coverage is reasonable.
- Make a release commit, where you remove the `, 'dev'` entry in `_version.py`.
- Relase the npm packages:
  ```bash
  npm login
  cd ts
  npm publish
  # Now, you need to update the entry in /<your python package>/jlextension/package.json
  # from "file:../../ts" to "^<the version of the NPM packge you just released>
  # After this, run:
  cd ../<your python package>/jlextension
  npm publish
  ```
- Bundle the python package: `python setup.py sdist bdist_wheel`
- Publish the package to PyPI:
  ```bash
  pip install twine
  twine upload dist/*
  ```
- Tag the release commit (`git tag <python package version identifier>`)
- Update the version in `_version.py`, and put it back to dev (e.g. 0.1.0 -> 0.2.0.dev).
  Update the versions of the npm packages (without publishing).
- Commit the changes.
- `git push` and `git push --tags`.
