import os
import sys
import pytest


def load_pytest_ini_from_site_packages(config):
    # Get the directory where pytest is installed (site-packages)
    site_packages_dir = os.path.dirname(pytest.__file__)

    # Define the paths to the pytest.ini and conftest.py files in site-packages
    ini_path = os.path.join(site_packages_dir, 'ui_demo_framework', 'src', 'pytest.ini')
    conftest_path = os.path.join(site_packages_dir, 'ui_demo_framework', 'src', 'conftest.py')

    # Load pytest.ini if it exists
    if os.path.exists(ini_path):
        config.inicfg.read(ini_path)  # Load pytest.ini settings
        print(f"Loaded pytest.ini from: {ini_path}")
    else:
        print(f"Warning: {ini_path} does not exist")

    # Load conftest.py if it exists
    if os.path.exists(conftest_path):
        sys.path.insert(0, os.path.dirname(conftest_path))
        __import__('conftest')  # Load the conftest.py file
        print(f"Loaded conftest.py from: {conftest_path}")
    else:
        print(f"Warning: {conftest_path} does not exist")


# Hook to call the function before tests are run
def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)
