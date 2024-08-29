import os


def pytest_configure(config):
    # Determine the directory where the package is installed
    package_dir = os.path.dirname(__file__)

    # Path to pytest.ini and conftest.py
    pytest_ini_path = os.path.join(package_dir, "pytest.ini")
    conftest_path = os.path.join(package_dir, "conftest.py")

    # Load pytest.ini
    if os.path.exists(pytest_ini_path):
        config.inicfg.read(pytest_ini_path)

    # Load conftest.py manually
    if os.path.exists(conftest_path):
        load_conftest(config, conftest_path)


def load_conftest(config, conftest_path):
    """
    Load conftest.py manually by executing it.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("conftest", conftest_path)
    conftest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conftest_module)

    # Register the plugins and hooks
    for plugin in getattr(conftest_module, 'pytest_plugins', []):
        config.pluginmanager.import_plugin(plugin)
