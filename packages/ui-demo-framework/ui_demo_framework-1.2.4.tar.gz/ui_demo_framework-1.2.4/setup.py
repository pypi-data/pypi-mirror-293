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
    version="1.2.4",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['conftest.py', 'pytest.ini'],
    },
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Mrinal Gautam",
    author_email="mrinalsinghgautam@gmail.com",
    url="https://github.com/mrinal2323/UI_Demo_Framework",
    description="A demo UI framework for testing purposes.",
    license="MIT",
    keywords="testing ui framework",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'pytest11': [
            'ui_demo_framework_plugin=src.pytest_plugin',
        ],
    },
)
