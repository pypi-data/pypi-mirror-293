
# Creating a Python Library to Mimic `curl` and Publish It on PyPI

> On my corrent job as a meber of the DevOps team, we were required to create a Python tool developed in-house to use on our CI pipelines. The tool was widely adopted by other engineering teams and they asked for a way to consume it in their projects without having to copy the code around. This tutorial is a step-by-step guide on how to create a simple Python library and publish it on PyPI which was my proposed POC to evaluate the feasibility of distribute and publish the CI tool as a Python library.

This tutorial will guide you through the process of creating a simple Python library that mimics the basic functionalities of the `curl` command. We'll cover everything from setting up your environment, implementing the library, configuring necessary files, setting up a GitHub Actions workflow with OpenID Connect (OIDC) to automate publishing to PyPI, and finally, packaging and publishing the library.

Out of scope for this tutorial are PyPi account creation topics, such as creating a PyPI account, setting up 2FA, and creating an API token. You can find more information on these topics in the [PyPI documentation](https://packaging.python.org/).

## Table of Contents

1. [Setting Up the Environment](#setting-up-the-environment)
2. [Project Structure](#project-structure)
3. [Implementing the Library](#implementing-the-library)
4. [Configuring `pyproject.toml`](#configuring-pyprojecttoml)
5. [Building Wheels and Source Distributions](#building-wheels-and-source-distributions)
6. [Publishing with GitHub Actions Using OIDC](#publishing-with-github-actions-using-oidc)
7. [Using TestPyPI for Testing](#using-testpypi-for-testing)
8. [Signing the Package](#signing-the-package)
9. [Creating Namespace Packages (Optional)](#creating-namespace-packages-optional)
10. [Testing the Published Library](#testing-the-published-library)

## Setting Up the Environment

1. **Create a Directory for Your Project:**

   ```bash
   mkdir pypi-curl-poc
   cd pypi-curl-poc
   ```

2. **Set Up a Virtual Environment:**

   It's recommended to use a virtual environment to isolate your dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

## Project Structure

3. **Create the Necessary Folders and Files:**

   ```bash
   mkdir pypi-curl-poc
   touch pypi-curl-poc/__init__.py
   touch setup.py
   ```

   Your project structure should now look like this:

   ```
   pypi-curl-poc/
   ├── pypi-curl-poc/
   │   └── __init__.py
   └── setup.py
   ```

## Implementing the Library

4. **Add Basic Functionality in `__init__.py`:**

   Let's create a function that sends an HTTP GET request using `requests`.

   ```python
   # pypi-curl-poc/__init__.py

   import requests

   def curl_get(url, params=None):
       """Mimic the curl -G command."""
       response = requests.get(url, params=params)
       return response.text
   ```

   This function uses the `requests` library to perform the HTTP request, similar to what `curl` does.

## Configuring `pyproject.toml`

5. **Create and Configure `pyproject.toml`:**

   The `pyproject.toml` file is essential for defining your build system requirements and project metadata.

   Create a file named `pyproject.toml` in the root of your project directory and add the following content:

   ```toml
   [build-system]
   requires = ["setuptools>=72", "wheel"]
   build-backend = "setuptools.build_meta"

   [project]
   name = "pypi-curl-poc"
   version = "0.1.0"
   authors = [
     { name="Your Name", email="your.email@example.com" },
   ]
   description = "A simple imitation of the curl command in Python"
   readme = "README.md"
   requires-python = ">=3.12"
   dependencies = ["requests"]
   classifiers = [
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
   ]

   [project.urls]
   "Homepage" = "https://github.com/yourusername/pypi-curl-poc"
   "Bug Tracker" = "https://github.com/yourusername/pypi-curl-poc/issues"

   [project.optional-dependencies]
   gui = ["PyQt5"]
   cli = ["rich", "click"]
   ```

   This file includes important metadata about your package, like the name, version, authors, and more. You can also specify optional dependencies, which users can install with `pip install yourpackage[extra]`.

   **Important Considerations:**
   - **Avoid Upper Bounds on `requires-python`:** Avoid setting upper bounds on the Python version in `requires-python` to prevent unnecessary restrictions as new Python versions are released.
   - **Dynamic Metadata:** Some fields can be marked as dynamic, allowing the build backend to determine the final value at build time, which is useful for version numbers.

6. **Configure `setup.py`:**

   To ensure that your package builds correctly, you need to set up `setup.py` with the necessary configuration. This file provides essential metadata about your package and ensures it can be built and distributed properly.

   Create or update `setup.py` with the following content:

   ```python
   from setuptools import setup, find_packages

   setup(
       name="pypi-curl-poc",
       version="0.1.0",
       description="A simple imitation of the curl command in Python",
       author="Your Name",
       author_email="your.email@example.com",
       packages=find_packages(),
       install_requires=["requests"],
       classifiers=[
           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
       ],
       python_requires='>=3.12',
   )

   ```

   This file includes important metadata about your package, like the name, version, authors, and more.

## Building Wheels and Source Distributions

7. **Build the Package:**

   Use `build` to create the package distribution files.

   ```bash
   pip install build
   python3 -m build
   ```

   This will generate a `dist/` directory containing the `.tar.gz` and `.whl` files.

8. **Creating a Universal Wheel:**

   To create a universal wheel that supports Python 3, you can add the following to your `setup.cfg`:

   ```ini
   [bdist_wheel]
   universal=1
   ```

## Publishing with GitHub Actions Using OIDC

9. **Configure GitHub Actions Workflow:**

   Create a file named `publish-to-pypi.yml` in the `.github/workflows/` directory of your repository:

   ```yaml
   name: Publish Python Package to PyPI

   on:
     push:
       tags:
         - 'v*.*.*'  # Trigger only on push tags following the pattern vX.X.X

   permissions:
     contents: read
     id-token: write  # Required for OIDC
     packages: write

   jobs:
     build-and-publish:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout code
           uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.x'  # Adjust the Python version as needed

         - name: Install dependencies
           run: pip install setuptools wheel twine

         - name: Build package
           run: python setup.py sdist bdist_wheel

         - name: Publish to PyPI
           env:
             TWINE_USERNAME: __token__
             TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
           run: twine upload dist/* --non-interactive

       publish-to-testpypi:
         name: Publish Python distribution to TestPyPI
         runs-on: ubuntu-latest
         environment: testpypi
         permissions:
           id-token: write  # Mandatory for trusted publishing
         steps:
           - name: Checkout code
             uses: actions/checkout@v4
           - name: Set up Python
             uses: actions/setup-python@v5
             with:
               python-version: '3.12'
           - name: Install dependencies
             run: pip install setuptools wheel twine
           - name: Build package
             run: python setup.py sdist bdist_wheel
           - name: Publish to TestPyPI
             env:
               TWINE_USERNAME: __token__
               TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
             run: twine upload --repository testpypi dist/* --non-interactive
   ```

## Using TestPyPI for Testing

10. **Testing with TestPyPI:**

    It's good practice to first upload to TestPyPI to ensure everything works as expected.

    ```bash
    python3 -m twine upload --repository testpypi dist/*
    ```

    Install it using:

    ```bash
    pip install --index-url https://test.pypi.org/simple/ --no-deps pypi-curl-poc
    ```

## Signing the Package

11. **Sign the Distribution Packages:**

    You can sign your distribution packages using Sigstore:

    ```yaml
    - name: Sign the dists with Sigstore
      uses: sigstore/gh-action-sigstore-python@v3.0.0
      with:
        inputs: >-
          ./dist/*.tar.gz
          ./dist/*.whl
    ```

    This ensures the integrity and authenticity of your package.

## Creating Namespace Packages (Optional)

12. **Creating Namespace Packages:**

    If your project involves multiple related packages, you might consider using namespace packages.

    Example `pyproject.toml` for a namespace package:

    ```toml
    [project]
    name = "mynamespace-subpackage-a"
    version = "0.1.0"

    [tool.setuptools.packages.find]
    where = ["src/"]
    include = ["mynamespace.subpackage_a"]
    ```

## Testing the Published Library

13. **Install and Test Your Library:**

    Once published, you can test by installing your library from PyPI:

    ```bash
    pip install pypi-curl-poc
    ```

    Then, in a Python file:

    ```python
    from pypi-curl-poc import curl_get

    response = curl_get("https://google.com")
    print(response)
    ```

14. **Uploading to PyPI:**

    Finally, upload the package to PyPI:

    ```bash
    python3 -m twine upload dist/*
    ```

---

Congratulations! You've successfully created and published a Python package to PyPI.
