
import os
import sys

import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(HERE)

pytest_plugins = "pytester"

use_shell = os.name == 'nt'


@pytest.fixture(scope='session')
def example_instance(tmpdir_factory):
    from cookiecutter.main import cookiecutter
    import pip

    tmpdir = tmpdir_factory.mktemp('example_instance')

    with tmpdir.as_cwd():
        cookiecutter(PROJECT_ROOT, no_input=True, config_file=os.path.join(HERE, 'testconfig.yaml'))
        instance_path = tmpdir.join('jupyter-widget-testwidgets')
        with instance_path.as_cwd():
            print(str(instance_path))
            try:
                pip.main(['install', '-v', '-e', '.[test]'])
                yield instance_path
            finally:
                try:
                    pip.main(['uninstall', 'jupyter_widget_testwidgets', '-y'])
                except Exception:
                    pass


def test_python_tests(example_instance, testdir):
    with example_instance.as_cwd():
        testdir.runpytest()


def test_js_tests(example_instance):
    from subprocess import check_call

    cmd = ['npm', 'test']
    with example_instance.as_cwd():
        check_call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=use_shell)
