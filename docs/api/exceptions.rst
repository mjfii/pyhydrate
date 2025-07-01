Exception Handling
==================

PyHydrate provides a comprehensive standardized error handling system with custom warning classes for different types of errors.

.. currentmodule:: pyhydrate.exceptions

Warning Classes
---------------

PyHydrateWarning
~~~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.exceptions.pyhydrate_warning.PyHydrateWarning
   :members:
   :undoc-members:
   :show-inheritance:

Base warning class for all PyHydrate-related warnings. All other warning classes inherit from this.

TypeConversionWarning
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.exceptions.type_conversion_warning.TypeConversionWarning
   :members:
   :undoc-members:
   :show-inheritance:

Raised when there are issues with type conversion, such as:

* Passing invalid types to notation class constructors
* Type casting failures during magic method operations

AccessPatternWarning
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.exceptions.access_pattern_warning.AccessPatternWarning
   :members:
   :undoc-members:
   :show-inheritance:

Raised when invalid access patterns are attempted, such as:

* Accessing array indices on dictionary objects
* Accessing dictionary keys on array objects  
* Out-of-bounds array access

APIUsageWarning
~~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.exceptions.api_usage_warning.APIUsageWarning
   :members:
   :undoc-members:
   :show-inheritance:

Raised when the API is used incorrectly, such as:

* Invalid call types (e.g., ``obj("invalid_type")``)
* Incorrect parameter values

Utility Functions
-----------------

format_warning_message
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyhydrate.exceptions.format_warning_message.format_warning_message

Standardized warning message formatter that provides consistent, informative error messages with suggestions for fixing issues.

Error Handling Utilities
-------------------------

.. currentmodule:: pyhydrate.error_handling

The error handling module provides utilities for consistent error handling across the PyHydrate library.

.. autofunction:: setup_logger
.. autofunction:: handle_type_conversion_error  
.. autofunction:: handle_access_pattern_error
.. autofunction:: handle_api_usage_error
.. autofunction:: log_debug_access
.. autofunction:: create_none_primitive

Usage Examples
--------------

Basic Warning Handling
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import warnings
   from pyhydrate import PyHydrate, TypeConversionWarning

   # Catch all PyHydrate warnings
   with warnings.catch_warnings(record=True) as w:
       warnings.simplefilter("always")
       
       # This will generate a TypeConversionWarning
       obj = NotationObject("not a dict", 0)
       
       if w:
           print(f"Warning: {w[0].message}")

Filtering Specific Warning Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import warnings
   from pyhydrate import TypeConversionWarning, APIUsageWarning

   # Ignore type conversion warnings but show API usage warnings
   warnings.filterwarnings("ignore", category=TypeConversionWarning)
   warnings.filterwarnings("default", category=APIUsageWarning)

   # This won't show a warning
   obj = NotationObject("invalid", 0)

   # This will show a warning
   hydrated = PyHydrate({"test": "data"})
   result = hydrated("invalid_call_type")

Debug Logging
~~~~~~~~~~~~~

.. code-block:: python

   from pyhydrate import PyHydrate

   # Enable debug mode for detailed logging
   data = {"nested": {"value": 42}}
   hydrated = PyHydrate(data, debug=True)

   # This will generate debug log messages showing the access path
   result = hydrated.nested.value()

Error Handling Features
-----------------------

* **🚨 Structured Warnings**: Custom warning classes for different error types
* **📝 Informative Messages**: Clear error descriptions with suggestions for fixes
* **🔍 Graceful Failures**: Invalid access returns None primitives instead of crashing  
* **📊 Debug Logging**: Structured logging system replaces print statements
* **🎛️ User Control**: Filter warnings by type for customized error handling
* **🔧 Developer-Friendly**: Consistent error patterns across the entire codebase