Installation
============

PyHydrate can be installed using pip from PyPI.

Requirements
------------

* Python 3.8 or higher
* ``typing-extensions`` (automatically installed)
* ``pyyaml`` (automatically installed)

TOML Support
~~~~~~~~~~~~

PyHydrate automatically handles TOML support based on your Python version:

* **Python 3.11+**: Uses the built-in ``tomllib`` module
* **Python < 3.11**: Automatically installs ``tomli`` for TOML support

Install from PyPI
-----------------

.. code-block:: bash

   pip install pyhydrate

To upgrade to the latest version:

.. code-block:: bash

   pip install pyhydrate --upgrade

Install from Source
-------------------

If you want to install the latest development version:

.. code-block:: bash

   git clone https://github.com/mjfii/pyhydrate.git
   cd pyhydrate
   pip install -e .

Development Installation
------------------------

For development work, install with additional dependencies:

.. code-block:: bash

   git clone https://github.com/mjfii/pyhydrate.git
   cd pyhydrate
   
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Unix/macOS
   # or .venv\Scripts\activate  # Windows
   
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -r requirements.txt

Verification
------------

Verify your installation by importing PyHydrate:

.. code-block:: python

   from pyhydrate import PyHydrate
   
   # Test with simple data
   data = {"test": "value"}
   hydrated = PyHydrate(data)
   print(hydrated.test())  # Should print: value

Docker
------

You can also use PyHydrate in a Docker container. Here's a simple example:

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   RUN pip install pyhydrate
   
   COPY your_script.py .
   CMD ["python", "your_script.py"]

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Errors**
   If you encounter module import errors, ensure you've installed the package in development mode:
   
   .. code-block:: bash
   
      pip install -e .

**TOML Support Issues**
   If TOML parsing fails on Python < 3.11, install tomli manually:
   
   .. code-block:: bash
   
      pip install tomli

**Virtual Environment Issues**
   If dependencies are not found, ensure your virtual environment is activated:
   
   .. code-block:: bash
   
      source .venv/bin/activate  # Unix/macOS
      # or .venv\Scripts\activate  # Windows