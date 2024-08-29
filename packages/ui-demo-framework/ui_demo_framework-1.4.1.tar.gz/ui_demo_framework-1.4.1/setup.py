from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read the dependencies from the requirements.txt file
requirements_path = this_directory / "requirements.txt"
with open(requirements_path) as f:
    install_requires = f.read().splitlines()

setup(
    name="ui_demo_framework",
    version="1.4.1",
    author="Mrinal Gautam",
    author_email="mrinalsinghgautam@gmail.com",
    description="A UI Testing Framework",
    url="https://github.com/mrinal2323/UI_Demo_Framework",
    packages=find_packages(),  # Automatically find packages
    include_package_data=True,  # Include data from MANIFEST.in
    package_data={
        '': ['src/pytest.ini', 'src/conftest.py'],  # Ensure these files are included
    },
    entry_points={
        'pytest11': [
            'ui_demo_framework_plugin = src.pytest_plugin',  # Register pytest plugin
        ],
    },
    install_requires=install_requires,  # Dependencies from requirements.txt
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
