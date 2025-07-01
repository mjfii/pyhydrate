Notation System
===============

The notation system provides the core classes for representing and accessing nested data structures.

.. currentmodule:: pyhydrate.notation

Base Classes
------------

NotationBase
~~~~~~~~~~~~

.. autoclass:: pyhydrate.notation.notation_base.NotationBase
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getattr__, __getitem__, __call__, __str__, __repr__, __int__, __float__, __bool__

Structure Classes
-----------------

NotationObject
~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.notation.notation_structures.NotationObject
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getattr__, __getitem__, __int__, __float__, __bool__

NotationArray
~~~~~~~~~~~~~

.. autoclass:: pyhydrate.notation.notation_structures.NotationArray
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getattr__, __getitem__, __int__, __float__, __bool__

Primitive Classes
-----------------

NotationPrimitive
~~~~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.notation.notation_primitive.NotationPrimitive
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getattr__, __getitem__, __int__, __float__, __bool__

Utility Classes
---------------

NotationDumper
~~~~~~~~~~~~~~

.. autoclass:: pyhydrate.notation.notation_dumper.NotationDumper
   :members:
   :undoc-members:
   :show-inheritance:

Architecture Overview
--------------------

The notation system uses a simplified inheritance hierarchy:

* **NotationBase**: Provides shared functionality including debug logging, key normalization, output formatting, and magic methods
* **NotationObject**: Handles dictionary structures with lazy loading and key mapping
* **NotationArray**: Handles list structures with indexed access
* **NotationPrimitive**: Handles primitive values (str, int, float, bool, None)

Memory Efficiency
~~~~~~~~~~~~~~~~~

The notation system uses several optimization techniques:

* **Lazy Loading**: Child objects are created only when accessed
* **__slots__**: Memory optimization for all notation classes  
* **Smart Caching**: Frequently accessed objects are cached for performance
* **On-demand Computation**: Cleaned values are computed only when requested

Key Features
~~~~~~~~~~~~

* **Automatic Key Normalization**: Converts camelCase, PascalCase, kebab-case to snake_case
* **Graceful Error Handling**: Returns None primitives instead of raising exceptions
* **Debug Support**: Comprehensive logging for development and troubleshooting
* **Type Safety**: Full type annotations throughout the codebase
* **Multiple Output Formats**: YAML, JSON, Python types, and element dictionaries