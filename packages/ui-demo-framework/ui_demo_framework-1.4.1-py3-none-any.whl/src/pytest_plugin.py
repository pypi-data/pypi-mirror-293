import os
import importlib.util
import pytest


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)
    load_conftest_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    # Define the site-packages directory
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))

    # Define the path to pytest.ini
    ini_path = os.path.join(site_packages_dir, 'pytest.ini')

    # Load pytest.ini settings
    if os.path.exists(ini_path):
        import configparser
        parser = configparser.ConfigParser()
        parser.read(ini_path)

        # Apply settings from pytest.ini to pytest config
        for section in parser.sections():
            for key, value in parser.items(section):
                # Ensure the key follows the format: [section.key]
                formatted_key = f"{section}.{key}"
                # Debug print to verify keys being set
                print(f"Setting pytest config: {formatted_key} = {value}")

                # Only set known keys
                if section == 'pytest' and key in ['markers']:  # Example: adjust as needed
                    config.addinivalue_line(f"{key}", value)
                else:
                    print(f"Warning: Key {formatted_key} is not a recognized pytest configuration option")
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
