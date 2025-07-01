PyHydrate Main Module
====================

This is the main entry point for PyHydrate, providing the primary ``PyHydrate`` class for dot notation access to nested data structures.

.. currentmodule:: pyhydrate

PyHydrate Class
---------------

.. autoclass:: PyHydrate
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getattr__, __getitem__, __call__, __str__, __repr__

   .. rubric:: Methods

   .. autosummary::
      :toctree: generated/

      PyHydrate.__init__
      PyHydrate.__getattr__
      PyHydrate.__getitem__
      PyHydrate.__call__
      PyHydrate.__str__
      PyHydrate.__repr__

Module Contents
---------------

.. automodule:: pyhydrate.pyhydrate
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

   from pyhydrate import PyHydrate

   # Dictionary data
   data = {
       "user-settings": {
           "displayName": "John Doe",
           "preferences": {
               "theme": "dark",
               "notifications": True
           }
       }
   }

   # Create PyHydrate instance
   hydrated = PyHydrate(data, debug=True)

   # Access using dot notation (automatic snake_case conversion)
   name = hydrated.user_settings.display_name()  # "John Doe"
   theme = hydrated.user_settings.preferences.theme()  # "dark"

   # Get different output formats
   yaml_output = hydrated.user_settings.preferences("yaml")
   json_output = hydrated.user_settings.preferences("json")
   element_output = hydrated.user_settings.preferences("element")

   # Graceful error handling for missing keys
   missing = hydrated.user_settings.missing_key()  # None