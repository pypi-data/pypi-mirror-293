import os
import sys
import pytest


def load_pytest_ini_from_site_packages(config):
    # Define the site-packages directory
    site_packages_dir = os.path.dirname(pytest.__file__)

    # Define the paths to the pytest.ini and conftest.py files in site-packages
    ini_path = os.path.join(site_packages_dir, 'src', 'pytest.ini')
    conftest_path = os.path.join(site_packages_dir, 'src', 'conftest.py')

    # Check if the paths exist
    if os.path.exists(ini_path):
        config.inicfg.read(ini_path)  # Load pytest.ini settings
    else:
        print(f"Warning: {ini_path} does not exist")

    if os.path.exists(conftest_path):
        sys.path.insert(0, os.path.dirname(conftest_path))
        __import__('conftest')  # Load the conftest.py file
    else:
        print(f"Warning: {conftest_path} does not exist")
