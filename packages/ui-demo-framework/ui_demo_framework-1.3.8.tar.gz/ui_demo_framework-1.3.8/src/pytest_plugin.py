import os
import pytest
import configparser


def pytest_configure(config):
    load_pytest_ini_from_site_packages(config)


def load_pytest_ini_from_site_packages(config):
    # Define the site-packages directory
    site_packages_dir = os.path.abspath(os.path.join(os.path.dirname(pytest.__file__), os.pardir, 'src'))

    # Define the path to pytest.ini
    ini_path = os.path.join(site_packages_dir, 'pytest.ini')

    # Load pytest.ini settings
    if os.path.exists(ini_path):
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
                    config.addinivalue_line(key, value)
                else:
                    print(f"Warning: Key {formatted_key} is not a recognized pytest configuration option")
    else:
        print(f"Warning: {ini_path} does not exist")
