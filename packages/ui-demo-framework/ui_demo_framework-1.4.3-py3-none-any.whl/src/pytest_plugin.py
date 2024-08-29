import pytest
import os
import importlib.util


def pytest_configure(config):
    # Determine the directory where the plugin is located
    package_dir = os.path.dirname(__file__)

    # Path to conftest.py
    conftest_path = os.path.join(package_dir, "conftest.py")

    # Load conftest.py manually if it exists
    if os.path.exists(conftest_path):
        load_conftest(conftest_path)


def load_conftest(conftest_path):
    """
    Load conftest.py manually by executing it.
    """
    spec = importlib.util.spec_from_file_location("conftest", conftest_path)
    conftest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conftest_module)

    # You can register additional plugins or hooks here if needed
    for plugin in getattr(conftest_module, 'pytest_plugins', []):
        pytest.config.pluginmanager.import_plugin(plugin)
