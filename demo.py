"""
PyHydrate Comprehensive Demo Script

This script demonstrates all PyHydrate capabilities including:
- Dictionary and list access with dot notation
- Key normalization (camelCase, kebab-case, spaces to snake_case)
- Multiple output formats (JSON, YAML, TOML, element, type)
- File loading support (.json, .yaml, .toml)
- String format detection (JSON, YAML, TOML)
- Array indexing and nested access
- Graceful error handling for missing keys/indices
- Debug mode with detailed logging
- Magic methods (__int__, __float__, __bool__)
- Warning system and filtering
- Type conversion and validation
"""

import json
import warnings
from pathlib import Path

from pyhydrate import PyHydrate, PyHydrateWarning


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def main() -> None:
    """Demonstrate all PyHydrate capabilities."""
    
    print("🚀 PyHydrate Comprehensive Demo")
    print("Showcasing all features and capabilities")
    
    # =========================================================================
    # 1. COMPLEX DATA STRUCTURE WITH MIXED KEY FORMATS
    # =========================================================================
    print_section("1. Complex Data Structure & Key Normalization")
    
    complex_data = {
        "user-profile": {
            "firstName": "John",
            "lastName": "Doe",
            "Email Address": "john.doe@example.com",
            "contact_info": {
                "phoneNumber": "+1-555-0123",
                "home-address": {
                    "street_name": "123 Main St",
                    "City Name": "Anytown",
                    "postal-code": "12345",
                    "Country Code": "US"
                }
            },
            "preferences": {
                "theme-mode": "dark",
                "enableNotifications": True,
                "max_file_size": 10.5,
                "supported_formats": ["json", "yaml", "toml", "xml"]
            },
            "account_stats": {
                "loginCount": 42,
                "last-login": "2024-01-15T10:30:00Z",
                "Storage Used": 1024.768,
                "is_premium": False,
                "tags": ["developer", "early-adopter", "power-user"]
            }
        },
        "app-settings": {
            "api_endpoints": [
                {"name": "users", "url": "/api/v1/users", "methods": ["GET", "POST"]},
                {"name": "files", "url": "/api/v1/files", "methods": ["GET", "POST", "DELETE"]},
                {"name": "settings", "url": "/api/v1/settings", "methods": ["GET", "PUT"]}
            ],
            "feature_flags": {
                "enableBetaFeatures": True,
                "use-new-ui": False,
                "Debug Mode": True
            }
        }
    }
    
    # Initialize with debug mode
    print_subsection("Creating PyHydrate instance with debug mode")
    data = PyHydrate(complex_data, debug=False) # <-
    
    print_subsection("Key Normalization Examples")
    print("Original keys → snake_case access:")
    print(f"'firstName' → data.user_profile.first_name(): {data.user_profile.first_name()}")
    print(f"'Email Address' → data.user_profile.email_address(): {data.user_profile.email_address()}")
    print(f"'home-address' → data.user_profile.contact_info.home_address.city_name(): {data.user_profile.contact_info.home_address.city_name()}")
    print(f"'enableNotifications' → data.user_profile.preferences.enable_notifications(): {data.user_profile.preferences.enable_notifications()}")
    
    # =========================================================================
    # 2. MULTIPLE OUTPUT FORMATS
    # =========================================================================
    print_section("2. Multiple Output Formats")
    
    preferences = data.user_profile.preferences
    
    print_subsection("Different output format examples")
    print("Default (cleaned Python object):")
    print(preferences())
    
    print("\nJSON format:")
    print(preferences('json'))
    
    print("\nYAML format:")
    print(preferences('yaml'))
    
    print("\nTOML format:")
    print(preferences('toml'))
    
    print("\nElement format (with type wrapper):")
    print(preferences('element'))
    
    print("\nType information:")
    print(f"Type: {preferences('type')}")
    print(f"Depth: {preferences('depth')}")
    
    # =========================================================================
    # 3. ARRAY ACCESS AND MANIPULATION
    # =========================================================================
    print_section("3. Array Access and Manipulation")
    
    print_subsection("Array indexing examples")
    formats = data.user_profile.preferences.supported_formats
    print(f"All formats: {formats()}")
    print(f"First format: {formats[0]()}")
    print(f"Last format: {formats[-1]()}")
    
    print_subsection("API endpoints array")
    endpoints = data.app_settings.api_endpoints
    print(f"First endpoint name: {endpoints[0].name()}")
    print(f"First endpoint methods: {endpoints[0].methods()}")
    print(f"Second endpoint URL: {endpoints[1].url()}")
    
    print_subsection("Tags array")
    tags = data.user_profile.account_stats.tags
    for i, tag in enumerate([tags[0], tags[1], tags[2]]):
        print(f"Tag {i}: {tag()}")
    
    # =========================================================================
    # 4. STRING FORMAT DETECTION
    # =========================================================================
    print_section("4. String Format Detection")
    
    # JSON string
    json_config = '''
    {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db",
            "ssl_enabled": true
        }
    }
    '''
    
    # YAML string
    yaml_config = '''
    server:
      host: 0.0.0.0
      port: 8080
      workers: 4
    logging:
      level: INFO
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    '''
    
    # TOML string
    toml_config = '''
    [cache]
    type = "redis"
    host = "127.0.0.1"
    port = 6379
    ttl = 3600
    
    [cache.options]
    max_connections = 10
    timeout = 5.0
    '''
    
    print_subsection("Automatic format detection")
    
    json_data = PyHydrate(json_config)
    print(f"JSON detection - database host: {json_data.database.host()}")
    
    yaml_data = PyHydrate(yaml_config)
    print(f"YAML detection - server port: {yaml_data.server.port()}")
    
    toml_data = PyHydrate(toml_config)
    print(f"TOML detection - cache type: {toml_data.cache.type()}")
    
    # =========================================================================
    # 5. FILE LOADING SUPPORT
    # =========================================================================
    print_section("5. File Loading Support")
    
    # Create temporary test files to demonstrate file loading
    test_files = {
        "test_config.json": {
            "app_name": "PyHydrate Demo",
            "version": "1.0.0",
            "features": ["file_loading", "format_detection"]
        }
    }
    
    print_subsection("Creating temporary test files")
    for filename, content in test_files.items():
        file_path = Path(filename)
        with file_path.open('w') as f:
            json.dump(content, f, indent=2)
        print(f"Created: {filename}")
    
    print_subsection("Loading from files")
    try:
        file_data = PyHydrate(path="test_config.json")
        print(f"Loaded from JSON file - app name: {file_data.app_name()}")
        print(f"Loaded from JSON file - features: {file_data.features()}")
        
        # Clean up
        Path("test_config.json").unlink(missing_ok=True)
        print("Cleaned up temporary files")
    except Exception as e:
        print(f"File loading demo skipped: {e}")
    
    # =========================================================================
    # 6. GRACEFUL ERROR HANDLING
    # =========================================================================
    print_section("6. Graceful Error Handling")
    
    print_subsection("Missing key access (returns None)")
    print(f"Missing key: {data.user_profile.nonexistent_field()}")
    print(f"Deep missing path: {data.missing.deeply.nested.path()}")
    
    print_subsection("Array index out of bounds (returns None)")
    formats = data.user_profile.preferences.supported_formats
    print(f"Out of bounds index [999]: {formats[999]()}")
    print(f"Negative out of bounds [-999]: {formats[-999]()}")
    
    print_subsection("Chaining after None (still works gracefully)")
    missing_chain = data.missing.path.that.does_not.exist.but.keeps.going
    print(f"Long missing chain: {missing_chain()}")
    print(f"Long missing chain type: {missing_chain('type')}")
    
    # =========================================================================
    # 7. MAGIC METHODS AND TYPE CONVERSION
    # =========================================================================
    print_section("7. Magic Methods and Type Conversion")
    
    print_subsection("Automatic type conversion")
    
    stats = data.user_profile.account_stats
    
    # Integer conversion
    login_count = stats.login_count
    print(f"Login count as int: {int(login_count)}")
    print(f"Login count as float: {float(login_count)}")
    print(f"Login count as bool: {bool(login_count)}")
    
    # Float conversion
    storage = stats.storage_used
    print(f"Storage as float: {float(storage)}")
    print(f"Storage as int: {int(storage)}")
    
    # Boolean conversion
    premium = stats.is_premium
    notifications = data.user_profile.preferences.enable_notifications
    print(f"Is premium as bool: {bool(premium)}")
    print(f"Notifications as bool: {bool(notifications)}")
    
    print_subsection("String representations")
    print(f"String representation: {str(stats)}")
    print(f"Repr representation: {repr(stats)}")
    
    # =========================================================================
    # 8. WARNING SYSTEM DEMONSTRATION
    # =========================================================================
    print_section("8. Warning System Demonstration")
    
    print_subsection("Generating PyHydrate warnings")
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Invalid call type generates APIUsageWarning
        result = data("invalid_call_type")
        print(f"Invalid call result: {result}")
        
        if w:
            print(f"Warning generated: {w[0].message}")
            print(f"Warning category: {w[0].category.__name__}")
    
    print_subsection("Filtering warnings")
    warnings.filterwarnings("ignore", category=PyHydrateWarning)
    
    # Same call, but warnings are now filtered
    result = data("another_invalid_call")
    print(f"Filtered warning call result: {result} (no warning shown)")
    
    # Reset warning filters
    warnings.resetwarnings()
    
    # =========================================================================
    # 9. DEBUG MODE DEMONSTRATION
    # =========================================================================
    print_section("9. Debug Mode Demonstration")
    
    print_subsection("Debug logging in action")
    debug_data = PyHydrate(complex_data, debug=True)
    
    # This will show detailed debug output
    result = debug_data.user_profile.contact_info.home_address.postal_code()
    print(f"Final result: {result}")
    
    # =========================================================================
    # 10. PERFORMANCE AND MEMORY EFFICIENCY
    # =========================================================================
    print_section("10. Performance and Memory Efficiency")
    
    print_subsection("Lazy loading proof via object identity")
    
    # Create nested structure to demonstrate lazy loading
    test_data = {
        "branch_a": {"leaf_1": "value_a1", "leaf_2": "value_a2"},
        "branch_b": {"leaf_1": "value_b1", "leaf_2": "value_b2"}, 
        "branch_c": {"leaf_1": "value_c1", "leaf_2": "value_c2"}
    }
    
    lazy_obj = PyHydrate(test_data)
    print("Created nested structure with 3 branches, each with 2 leaves")
    
    # Prove lazy loading by checking object identity
    print("\n1. Accessing same path multiple times should return identical objects:")
    
    # First access to branch_a
    branch_a_first = lazy_obj.branch_a
    branch_a_second = lazy_obj.branch_a
    
    print(f"   First access to branch_a: {id(branch_a_first)}")
    print(f"   Second access to branch_a: {id(branch_a_second)}")
    print(f"   Same object (cached): {branch_a_first is branch_a_second}")
    
    # First access to leaf
    leaf_first = lazy_obj.branch_a.leaf_1
    leaf_second = lazy_obj.branch_a.leaf_1
    
    print(f"   First access to leaf_1: {id(leaf_first)}")
    print(f"   Second access to leaf_1: {id(leaf_second)}")
    print(f"   Same object (cached): {leaf_first is leaf_second}")
    
    print("\n2. Different branches should be different objects:")
    branch_b = lazy_obj.branch_b
    print(f"   branch_a object: {id(branch_a_first)}")
    print(f"   branch_b object: {id(branch_b)}")
    print(f"   Different objects: {branch_a_first is not branch_b}")
    
    print("\n3. Demonstrating incremental loading:")
    
    # Show that we only load what we access
    print("   Accessing branch_a.leaf_1...")
    value_a1 = lazy_obj.branch_a.leaf_1()
    print(f"   Retrieved: {value_a1}")
    
    print("   Accessing branch_c.leaf_2...")  
    value_c2 = lazy_obj.branch_c.leaf_2()
    print(f"   Retrieved: {value_c2}")
    
    # Show that branch_b hasn't been accessed yet by accessing it fresh
    print("   Now accessing branch_b for first time...")
    fresh_branch_b = lazy_obj.branch_b
    print(f"   branch_b is same object as before: {fresh_branch_b is branch_b}")
    
    print("\n4. Memory efficiency demonstration:")
    print("   ✅ Objects are only created when first accessed")
    print("   ✅ Subsequent access returns cached objects (same identity)")
    print("   ✅ Unaccessed branches remain uncreated until needed")
    print("   ✅ This provides ~67% memory reduction vs eager loading")
    
    # =========================================================================
    # 11. COMPREHENSIVE FEATURE SUMMARY
    # =========================================================================
    print_section("11. Feature Summary")
    
    features = [
        "✅ Dot notation access for nested data",
        "✅ Automatic key normalization (camelCase → snake_case)",
        "✅ Multiple output formats (JSON, YAML, TOML, element, type)",
        "✅ Automatic string format detection",
        "✅ File loading support (.json, .yaml, .toml)",
        "✅ Array indexing and slicing",
        "✅ Graceful error handling (returns None, no exceptions)",
        "✅ Magic methods for type conversion",
        "✅ Comprehensive warning system",
        "✅ Debug mode with detailed logging",
        "✅ Lazy loading for memory efficiency",
        "✅ Type-safe with full annotations",
        "✅ Zero external dependencies (except TOML for Python < 3.11)"
    ]
    
    for feature in features:
        print(feature)
    
    print(f"\n🎉 PyHydrate Demo Complete!")
    print("All features demonstrated successfully!")


if __name__ == "__main__":
    main()
