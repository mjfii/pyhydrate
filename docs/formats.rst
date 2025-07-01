Data Formats
============

PyHydrate supports multiple data formats with automatic detection and parsing.

Supported Formats
-----------------

* **Python dictionaries and lists** - Native Python data structures
* **JSON** - JavaScript Object Notation strings and files
* **YAML** - YAML Ain't Markup Language strings and files  
* **TOML** - Tom's Obvious, Minimal Language strings and files

Format Detection
----------------

When you pass a string to PyHydrate, it automatically detects the format in this order:

1. **JSON** (fastest parsing)
2. **TOML** (structured configuration format)
3. **YAML** (most flexible format)

This order ensures optimal performance while maintaining broad compatibility.

JSON Support
------------

.. code-block:: python

   from pyhydrate import PyHydrate

   # JSON string
   json_data = '''
   {
       "api": {
           "version": "1.0",
           "endpoints": [
               {"path": "/users", "method": "GET"},
               {"path": "/users", "method": "POST"}
           ]
       }
   }
   '''

   hydrated = PyHydrate(json_data)
   print(hydrated.api.version())  # "1.0"
   print(hydrated.api.endpoints[0].path())  # "/users"

YAML Support  
------------

.. code-block:: python

   # YAML string with complex structures
   yaml_data = '''
   database:
     primary:
       host: db1.example.com
       port: 5432
       credentials:
         username: admin
         password: secret
     replica:
       host: db2.example.com
       port: 5432
   '''

   hydrated = PyHydrate(yaml_data)
   print(hydrated.database.primary.host())  # "db1.example.com"
   print(hydrated.database.replica.port())  # 5432

TOML Support
------------

PyHydrate provides excellent TOML support with automatic compatibility handling:

.. code-block:: python

   # TOML configuration
   toml_config = '''
   [server]
   host = "api.example.com"
   port = 8080
   debug = true

   [database]
   url = "postgresql://localhost/myapp"
   pool_size = 10

   [[workers]]
   name = "worker1"
   processes = 4

   [[workers]]  
   name = "worker2"
   processes = 2
   '''

   config = PyHydrate(toml_config)
   
   # Access server configuration
   print(config.server.host())     # "api.example.com"
   print(config.server.debug())    # True
   
   # Access database settings
   print(config.database.url())    # "postgresql://localhost/myapp"
   
   # Access worker arrays
   print(config.workers[0].name())      # "worker1"
   print(config.workers[1].processes()) # 2

Python Version Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TOML support is handled automatically:

* **Python 3.11+**: Uses built-in ``tomllib`` module
* **Python < 3.11**: Falls back to ``tomli`` package (auto-installed)

Mixed Data Types
----------------

PyHydrate handles complex nested structures seamlessly:

.. code-block:: python

   complex_data = {
       "metadata": {
           "version": "2.1.0",
           "created": "2024-01-01T00:00:00Z"
       },
       "environments": [
           {
               "name": "production", 
               "config": {
                   "replicas": 3,
                   "resources": {
                       "cpu": "2000m",
                       "memory": "4Gi"
                   }
               }
           },
           {
               "name": "staging",
               "config": {
                   "replicas": 1, 
                   "resources": {
                       "cpu": "500m",
                       "memory": "1Gi"
                   }
               }
           }
       ]
   }

   hydrated = PyHydrate(complex_data)
   
   # Navigate complex structures
   prod_cpu = hydrated.environments[0].config.resources.cpu()
   print(prod_cpu)  # "2000m"
   
   staging_memory = hydrated.environments[1].config.resources.memory()
   print(staging_memory)  # "1Gi"

Output Formats
--------------

Get your data back in any format:

.. code-block:: python

   data = {"server": {"host": "localhost", "port": 8080}}
   hydrated = PyHydrate(data)
   
   server = hydrated.server
   
   # Python dictionary (default)
   print(server())
   # {'host': 'localhost', 'port': 8080}
   
   # YAML format
   print(server("yaml"))
   # host: localhost
   # port: 8080
   
   # JSON format
   print(server("json"))  
   # {
   #    "host": "localhost",
   #    "port": 8080
   # }
   
   # Element format (type information)
   print(server("element"))
   # {'dict': {'host': 'localhost', 'port': 8080}}

File Loading
------------

While PyHydrate focuses on in-memory data structures, you can easily load files:

.. code-block:: python

   import json
   import yaml
   from pathlib import Path

   # Load JSON file
   json_file = Path("config.json").read_text()
   hydrated = PyHydrate(json_file)

   # Load YAML file
   yaml_file = Path("config.yaml").read_text()  
   hydrated = PyHydrate(yaml_file)

   # Load TOML file
   toml_file = Path("config.toml").read_text()
   hydrated = PyHydrate(toml_file)

Best Practices
--------------

Format Selection
~~~~~~~~~~~~~~~~

* **JSON**: Best for APIs and data interchange
* **YAML**: Best for configuration files with comments
* **TOML**: Best for application configuration
* **Python dicts**: Best for programmatic data structures

Performance Tips
~~~~~~~~~~~~~~~

* JSON parsing is fastest, followed by TOML, then YAML
* For large datasets, consider using Python dicts directly
* Use debug mode only during development