import os
import importlib.util
import pytest


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)
    load_conftest_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))
    ini_path = os.path.join(site_packages_dir, 'pytest.ini')

    if os.path.exists(ini_path):
        import configparser
        parser = configparser.ConfigParser()
        parser.read(ini_path)

        for section in parser.sections():
            for key, value in parser.items(section):
                if section == 'pytest':
                    config.addinivalue_line(key, value)
                else:
                    # Handle custom sections if needed
                    config.addinivalue_line(f"{section}.{key}", value)
    else:
        print(f"Warning: {ini_path} does not exist")


def load_conftest_from_site_packages(config):
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))
    conftest_path = os.path.join(site_packages_dir, 'conftest.py')

    if os.path.exists(conftest_path):
        spec = importlib.util.spec_from_file_location("conftest", conftest_path)
        conftest_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conftest_module)

        # Explicitly call pytest_configure if defined in conftest.py
        if hasattr(conftest_module, 'pytest_configure'):
            conftest_module.pytest_configure(config)
    else:
        print(f"Warning: {conftest_path} does not exist")
