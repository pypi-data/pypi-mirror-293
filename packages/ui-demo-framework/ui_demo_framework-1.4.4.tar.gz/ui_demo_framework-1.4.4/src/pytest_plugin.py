import os
import importlib.util


def pytest_configure(config):
    # Determine the directory where the plugin is located
    package_dir = os.path.dirname(__file__)
    print(f"Plugin directory: {package_dir}")  # Print the plugin directory

    # Path to conftest.py and pytest.ini
    conftest_path = os.path.join(package_dir, "conftest.py")
    pytest_ini_path = os.path.join(package_dir, "pytest.ini")

    # Load conftest.py manually if it exists
    if os.path.exists(conftest_path):
        print(f"Loading conftest.py from {conftest_path}")  # Print message when loading conftest.py
        load_conftest(conftest_path)
    else:
        print("conftest.py not found")  # Print message if conftest.py is not found

    # Load pytest.ini configuration if it exists
    if os.path.exists(pytest_ini_path):
        print(f"Loading pytest.ini from {pytest_ini_path}")  # Print message when loading pytest.ini
        config.inicfg.read(pytest_ini_path)
    else:
        print("pytest.ini not found")  # Print message if pytest.ini is not found


def load_conftest(conftest_path):
    """
    Load conftest.py manually by executing it.
    """
    spec = importlib.util.spec_from_file_location("conftest", conftest_path)
    conftest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conftest_module)
    print(f"conftest.py loaded successfully from {conftest_path}")  # Print message after loading conftest.py
