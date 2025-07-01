Quick Start
===========

This guide will get you up and running with PyHydrate in minutes.

Basic Usage
-----------

PyHydrate enables dot notation access to nested data structures with automatic key normalization.

.. code-block:: python

   from pyhydrate import PyHydrate

   # Sample nested data
   data = {
       "user-info": {
           "firstName": "John",
           "lastName": "Doe", 
           "userSettings": {
               "theme": "dark",
               "notifications": True,
               "preferences": {
                   "language": "en",
                   "timezone": "UTC"
               }
           }
       }
   }

   # Create PyHydrate instance
   hydrated = PyHydrate(data)

   # Access with dot notation (automatic snake_case conversion)
   print(hydrated.user_info.first_name())  # "John"
   print(hydrated.user_info.user_settings.theme())  # "dark"
   print(hydrated.user_info.user_settings.preferences.language())  # "en"

Key Features Demo
-----------------

Graceful Error Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Missing keys return None instead of raising exceptions
   result = hydrated.user_info.missing_key()
   print(result)  # None
   print(type(result))  # <class 'pyhydrate.notation.notation_primitive.NotationPrimitive'>

Multiple Output Formats
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get data in different formats
   settings = hydrated.user_info.user_settings
   
   # Default: cleaned Python value
   print(settings())
   # {'theme': 'dark', 'notifications': True, 'preferences': {...}}
   
   # YAML format
   print(settings("yaml"))
   # theme: dark
   # notifications: true
   # preferences:
   #   language: en
   #   timezone: UTC
   
   # JSON format  
   print(settings("json"))
   # {
   #    "theme": "dark",
   #    "notifications": true,
   #    "preferences": {
   #       "language": "en",
   #       "timezone": "UTC"
   #    }
   # }
   
   # Element format (type + value)
   print(settings("element"))
   # {'dict': {'theme': 'dark', 'notifications': True, ...}}
   
   # Type information
   print(settings("type"))  # <class 'dict'>

Working with Arrays
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   array_data = {
       "users": [
           {"name": "Alice", "age": 30},
           {"name": "Bob", "age": 25}, 
           {"name": "Charlie", "age": 35}
       ]
   }

   hydrated = PyHydrate(array_data)

   # Access array elements by index
   print(hydrated.users[0].name())  # "Alice"
   print(hydrated.users[1].age())   # 25
   
   # Out of bounds returns None
   print(hydrated.users[999]())     # None

String Input Support
~~~~~~~~~~~~~~~~~~~

PyHydrate automatically detects and parses JSON, YAML, and TOML strings:

.. code-block:: python

   # JSON string
   json_str = '{"name": "John", "age": 30}'
   hydrated = PyHydrate(json_str)
   print(hydrated.name())  # "John"

   # YAML string  
   yaml_str = """
   database:
     host: localhost
     port: 5432
   """
   hydrated = PyHydrate(yaml_str)
   print(hydrated.database.host())  # "localhost"

   # TOML string
   toml_str = """
   [server]
   host = "example.com"
   port = 8080
   """
   hydrated = PyHydrate(toml_str)
   print(hydrated.server.host())  # "example.com"

Debug Mode
~~~~~~~~~~

Enable debug mode to see detailed access logging:

.. code-block:: python

   data = {"nested": {"deep": {"value": 42}}}
   hydrated = PyHydrate(data, debug=True)

   # This will show debug output
   result = hydrated.nested.deep.value()
   
   # Debug output shows:
   # >>> Object :: Get == nested :: Depth == 1
   #    >>> Object :: Get == deep :: Depth == 2  
   #       >>> Object :: Get == value :: Depth == 3
   #          >>> Primitive :: Call == value :: Depth == 4 :: Output == 42

Key Normalization
~~~~~~~~~~~~~~~~

PyHydrate automatically converts various key formats to snake_case:

.. code-block:: python

   mixed_keys = {
       "camelCase": "value1",
       "PascalCase": "value2", 
       "kebab-case": "value3",
       "snake_case": "value4",
       "UPPER_CASE": "value5",
       "mixed Key": "value6"
   }

   hydrated = PyHydrate(mixed_keys)

   # All accessed with snake_case
   print(hydrated.camel_case())    # "value1"
   print(hydrated.pascal_case())   # "value2"
   print(hydrated.kebab_case())    # "value3"
   print(hydrated.snake_case())    # "value4"
   print(hydrated.upper_case())    # "value5"  
   print(hydrated.mixed_key())     # "value6"

Next Steps
----------

* Read the :doc:`usage` guide for more detailed examples
* Check out :doc:`formats` for format-specific features
* Learn about :doc:`error_handling` for robust applications
* Explore the :doc:`api/pyhydrate` for complete API reference