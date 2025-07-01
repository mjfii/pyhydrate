Error Handling
==============

PyHydrate provides comprehensive error handling with graceful failures and informative warnings.

For complete API reference, see :doc:`api/exceptions`.

Graceful Failures
-----------------

PyHydrate never crashes on invalid access - it returns None primitives instead:

.. code-block:: python

   from pyhydrate import PyHydrate

   data = {"existing": "value"}
   hydrated = PyHydrate(data)

   # Valid access
   result = hydrated.existing()
   print(result)  # "value"

   # Invalid access returns None primitive
   missing = hydrated.nonexistent()
   print(missing)  # None
   print(type(missing))  # NotationPrimitive

Warning System
--------------

PyHydrate uses a structured warning system for different error types.

See :doc:`api/exceptions` for complete warning class documentation.