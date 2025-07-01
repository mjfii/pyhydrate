PyHydrate Documentation
=======================

.. include:: ../readme.md
   :parser: myst_parser.sphinx_

PyHydrate is a Python library that enables dot notation access to nested data structures (dicts, lists, JSON, YAML, TOML) with graceful error handling and automatic key normalization.

Features
--------

* 🚀 **Dot Notation Access**: Easy access to nested data using `obj.key.subkey` syntax
* 🔧 **Multiple Format Support**: JSON, YAML, TOML, Python dicts and lists
* 🛡️ **Graceful Error Handling**: Returns None instead of raising exceptions for missing keys
* 🐍 **Snake Case Conversion**: Automatically converts camelCase, PascalCase, and kebab-case to snake_case
* 💾 **Memory Efficient**: Lazy loading with ~67% memory reduction
* 🎯 **Type Safe**: Full type annotations with comprehensive testing
* 📊 **Debug Support**: Built-in debug mode for development and troubleshooting

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install pyhydrate

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from pyhydrate import PyHydrate

   data = {
       "user-info": {
           "firstName": "John",
           "lastName": "Doe",
           "settings": {
               "theme": "dark",
               "notifications": True
           }
       }
   }

   hydrated = PyHydrate(data)

   # Access with dot notation (keys automatically converted to snake_case)
   print(hydrated.user_info.first_name())  # "John"
   print(hydrated.user_info.settings.theme())  # "dark"

   # Graceful handling of missing keys
   print(hydrated.user_info.missing_key())  # None

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   usage
   formats
   error_handling
   performance

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/pyhydrate
   api/notation
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`