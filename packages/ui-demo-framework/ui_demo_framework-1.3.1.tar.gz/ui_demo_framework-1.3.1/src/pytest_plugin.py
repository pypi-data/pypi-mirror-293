import os
import sys
import pytest


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    site_packages_dir = os.path.dirname(pytest.__file__)

    ini_path = os.path.join(site_packages_dir, 'src', 'pytest.ini')
    conftest_path = os.path.join(site_packages_dir, 'src', 'conftest.py')

    if os.path.exists(ini_path):
        config.inicfg.read(ini_path)
    else:
        print(f"Warning: {ini_path} does not exist")

    if os.path.exists(conftest_path):
        sys.path.insert(0, os.path.dirname(conftest_path))
        __import__('conftest')
    else:
        print(f"Warning: {conftest_path} does not exist")
