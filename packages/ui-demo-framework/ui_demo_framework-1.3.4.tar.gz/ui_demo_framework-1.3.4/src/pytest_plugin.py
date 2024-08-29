import os
import sys
import pytest
import configparser


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    # Define the site-packages directory
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))

    # Define the paths to pytest.ini and conftest.py
    ini_path = os.path.join(site_packages_dir, 'pytest.ini')
    conftest_path = os.path.join(site_packages_dir, 'conftest.py')

    # Load pytest.ini settings
    if os.path.exists(ini_path):
        parser = configparser.ConfigParser()
        parser.read(ini_path)

        # Apply settings from pytest.ini to pytest config
        for section in parser.sections():
            for key, value in parser.items(section):
                config.addinivalue_line(f"{section}.{key} = {value}")
    else:
        print(f"Warning: {ini_path} does not exist")

    # Dynamically load the conftest.py file
    if os.path.exists(conftest_path):
        sys.path.insert(0, os.path.dirname(conftest_path))
        __import__('conftest')
    else:
        print(f"Warning: {conftest_path} does not exist")
