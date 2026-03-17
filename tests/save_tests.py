"""
Tests for file save/write functionality in PyHydrate.

Tests cover:
- Saving to JSON, YAML, and TOML files
- Round-trip: load → modify → save → reload → verify
- Save with explicit format override
- Save back to source path (no arg)
- Error cases for missing path and unknown extension
"""

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from pyhydrate import PyHydrate


class TestSaveToFile(unittest.TestCase):
    """Test saving data to various file formats."""

    def test_save_json(self) -> None:
        """Save data to a JSON file."""
        data = PyHydrate({"name": "Alice", "age": 25})
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            path = Path(f.name)

        try:
            data.save(path)
            result = json.loads(path.read_text(encoding="utf-8"))
            assert result["name"] == "Alice"
            assert result["age"] == 25
        finally:
            path.unlink()

    def test_save_yaml(self) -> None:
        """Save data to a YAML file."""
        data = PyHydrate({"name": "Bob", "count": 42})
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            path = Path(f.name)

        try:
            data.save(path)
            result = yaml.safe_load(path.read_text(encoding="utf-8"))
            assert result["name"] == "Bob"
            assert result["count"] == 42
        finally:
            path.unlink()

    def test_save_toml(self) -> None:
        """Save data to a TOML file."""
        data = PyHydrate({"title": "Test", "version": 1})
        with tempfile.NamedTemporaryFile(suffix=".toml", mode="w", delete=False) as f:
            path = Path(f.name)

        try:
            data.save(path)
            content = path.read_text(encoding="utf-8")
            assert "title" in content
            assert "Test" in content
        finally:
            path.unlink()


class TestSaveRoundTrip(unittest.TestCase):
    """Test round-trip: load → modify → save → reload."""

    def test_json_round_trip(self) -> None:
        """Round-trip through JSON file."""
        original = {"name": "Alice", "age": 25}
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump(original, f)
            path = Path(f.name)

        try:
            data = PyHydrate(path=str(path))
            data.age = 26
            data.save(path)

            reloaded = PyHydrate(path=str(path))
            assert reloaded.name() == "Alice"
            assert reloaded.age() == 26
        finally:
            path.unlink()

    def test_yaml_round_trip(self) -> None:
        """Round-trip through YAML file."""
        original = {"name": "Bob", "active": True}
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
            yaml.dump(original, f)
            path = Path(f.name)

        try:
            data = PyHydrate(path=str(path))
            data.active = False
            data.save(path)

            reloaded = PyHydrate(path=str(path))
            assert reloaded.name() == "Bob"
            assert reloaded.active() is False
        finally:
            path.unlink()


class TestSaveSourcePath(unittest.TestCase):
    """Test saving back to source path."""

    def test_save_to_source_path(self) -> None:
        """Save with no args writes back to source path."""
        original = {"key": "value"}
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump(original, f)
            path = Path(f.name)

        try:
            data = PyHydrate(path=str(path))
            data.key = "updated"
            data.save()

            result = json.loads(path.read_text(encoding="utf-8"))
            assert result["key"] == "updated"
        finally:
            path.unlink()

    def test_save_no_path_raises(self) -> None:
        """Save with no path and no source raises ValueError."""
        data = PyHydrate({"key": "value"})
        with self.assertRaises(ValueError):
            data.save()


class TestSaveFormatOverride(unittest.TestCase):
    """Test explicit format override."""

    def test_save_with_format_override(self) -> None:
        """Save with explicit format, ignoring extension."""
        data = PyHydrate({"name": "test"})
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
            path = Path(f.name)

        try:
            data.save(path, output_format="json")
            result = json.loads(path.read_text(encoding="utf-8"))
            assert result["name"] == "test"
        finally:
            path.unlink()

    def test_save_unknown_extension_raises(self) -> None:
        """Save to unknown extension without format override raises."""
        data = PyHydrate({"key": "value"})
        with tempfile.NamedTemporaryFile(suffix=".xyz", mode="w", delete=False) as f:
            path = Path(f.name)

        try:
            with self.assertRaises(ValueError):
                data.save(path)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
