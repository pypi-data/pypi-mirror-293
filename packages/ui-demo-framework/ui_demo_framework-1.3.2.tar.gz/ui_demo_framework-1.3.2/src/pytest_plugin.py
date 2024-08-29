import os
import sys
import pytest


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    # Define the correct site-packages directory
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))

    # Define the correct paths to the pytest.ini and conftest.py files
    ini_path = os.path.join(site_packages_dir, 'pytest.ini')
    conftest_path = os.path.join(site_packages_dir, 'conftest.py')

    # Check if the paths exist and load the files
    if os.path.exists(ini_path):
        config.inicfg.read(ini_path)  # Load pytest.ini settings
    else:
        print(f"Warning: {ini_path} does not exist")

    if os.path.exists(conftest_path):
        sys.path.insert(0, os.path.dirname(conftest_path))
        __import__('conftest')  # Load the conftest.py file
    else:
        print(f"Warning: {conftest_path} does not exist")
