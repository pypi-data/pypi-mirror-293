import pytest
import os
import site


def load_pytest_ini_from_site_packages(config):
    site_packages_paths = site.getsitepackages()
    for site_packages_path in site_packages_paths:
        src_path = os.path.join(site_packages_path, 'src')
        pytest_ini_path = os.path.join(src_path, 'pytest.ini')
        conftest_path = os.path.join(src_path, 'conftest.py')

        if os.path.exists(pytest_ini_path):
            config.read(pytest_ini_path)
            print(f"Found pytest.ini at {pytest_ini_path}")
        else:
            print(f"Warning: {pytest_ini_path} does not exist")

        if os.path.exists(conftest_path):
            pytest.main([conftest_path])
            print(f"Loaded conftest.py from {conftest_path}")
        else:
            print(f"Warning: {conftest_path} does not exist")


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)
