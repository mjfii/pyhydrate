"""
Tests for cloud storage save functionality in PyHydrate.

Tests cover:
- Remote path detection for S3, GCS, and ADLS URIs
- Saving to remote paths via fsspec (mocked)
- Format detection from remote URIs
- ImportError when fsspec is not available
- original_keys support with remote paths
- Local paths remain unaffected
"""

import json
import unittest
from io import StringIO
from pathlib import PurePosixPath
from unittest.mock import MagicMock, patch

import yaml

from pyhydrate import PyHydrate


class TestIsRemotePath(unittest.TestCase):
    """Test remote path detection."""

    def test_s3_path(self) -> None:
        assert PyHydrate._is_remote_path("s3://bucket/key.json") is True

    def test_s3a_path(self) -> None:
        assert PyHydrate._is_remote_path("s3a://bucket/key.json") is True

    def test_gs_path(self) -> None:
        assert PyHydrate._is_remote_path("gs://bucket/key.json") is True

    def test_gcs_path(self) -> None:
        assert PyHydrate._is_remote_path("gcs://bucket/key.json") is True

    def test_abfs_path(self) -> None:
        assert PyHydrate._is_remote_path("abfs://container/key.json") is True

    def test_abfss_path(self) -> None:
        assert PyHydrate._is_remote_path("abfss://container/key.json") is True

    def test_az_path(self) -> None:
        assert PyHydrate._is_remote_path("az://container/key.json") is True

    def test_local_path(self) -> None:
        assert PyHydrate._is_remote_path("/tmp/file.json") is False

    def test_relative_path(self) -> None:
        assert PyHydrate._is_remote_path("output/file.json") is False

    def test_http_not_remote(self) -> None:
        assert PyHydrate._is_remote_path("http://example.com/file.json") is False

    def test_path_object(self) -> None:
        assert PyHydrate._is_remote_path(PurePosixPath("/tmp/file.json")) is False


class TestRemoteFormatDetection(unittest.TestCase):
    """Test format detection from remote URIs."""

    def test_s3_json_extension(self) -> None:
        path = PurePosixPath("s3://bucket/path/output.json")
        assert PyHydrate._detect_format(path) == "json"

    def test_gs_yaml_extension(self) -> None:
        path = PurePosixPath("gs://bucket/path/output.yaml")
        assert PyHydrate._detect_format(path) == "yaml"

    def test_abfss_yml_extension(self) -> None:
        path = PurePosixPath("abfss://container/path/output.yml")
        assert PyHydrate._detect_format(path) == "yaml"

    def test_s3_toml_extension(self) -> None:
        path = PurePosixPath("s3://bucket/path/config.toml")
        assert PyHydrate._detect_format(path) == "toml"

    def test_unknown_extension_raises(self) -> None:
        path = PurePosixPath("s3://bucket/path/output.xyz")
        with self.assertRaises(ValueError):
            PyHydrate._detect_format(path)


class TestCloudSaveS3(unittest.TestCase):
    """Test saving to S3 via mocked fsspec."""

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_json_to_s3(self, mock_write: MagicMock) -> None:
        """Save JSON to an S3 path."""
        data = PyHydrate({"name": "Alice", "age": 25})
        data.save("s3://bucket/test/output.json")

        mock_write.assert_called_once()
        call_args = mock_write.call_args
        assert call_args[0][0] == "s3://bucket/test/output.json"
        result = json.loads(call_args[0][1])
        assert result["name"] == "Alice"
        assert result["age"] == 25

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_yaml_to_s3(self, mock_write: MagicMock) -> None:
        """Save YAML to an S3 path."""
        data = PyHydrate({"name": "Bob", "count": 42})
        data.save("s3://bucket/test/output.yml")

        mock_write.assert_called_once()
        call_args = mock_write.call_args
        assert call_args[0][0] == "s3://bucket/test/output.yml"
        result = yaml.safe_load(call_args[0][1])
        assert result["name"] == "Bob"
        assert result["count"] == 42

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_with_original_keys_to_s3(self, mock_write: MagicMock) -> None:
        """Save with original_keys=True to an S3 path."""
        data = PyHydrate({"firstName": "Alice", "lastName": "Smith"})
        data.save("s3://bucket/test/output.json", original_keys=True)

        mock_write.assert_called_once()
        result = json.loads(mock_write.call_args[0][1])
        assert "firstName" in result
        assert "lastName" in result

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_with_format_override_to_s3(self, mock_write: MagicMock) -> None:
        """Save with explicit format override to S3."""
        data = PyHydrate({"key": "value"})
        data.save("s3://bucket/test/output.dat", output_format="json")

        mock_write.assert_called_once()
        result = json.loads(mock_write.call_args[0][1])
        assert result["key"] == "value"


class TestCloudSaveGCS(unittest.TestCase):
    """Test saving to GCS via mocked fsspec."""

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_json_to_gs(self, mock_write: MagicMock) -> None:
        """Save JSON to a GCS path."""
        data = PyHydrate({"project": "test"})
        data.save("gs://bucket/output.json")

        mock_write.assert_called_once()
        assert mock_write.call_args[0][0] == "gs://bucket/output.json"
        result = json.loads(mock_write.call_args[0][1])
        assert result["project"] == "test"


class TestCloudSaveADLS(unittest.TestCase):
    """Test saving to ADLS via mocked fsspec."""

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_save_json_to_abfss(self, mock_write: MagicMock) -> None:
        """Save JSON to an ADLS path."""
        data = PyHydrate({"resource": "data"})
        data.save("abfss://container@account.dfs.core.windows.net/output.json")

        mock_write.assert_called_once()
        result = json.loads(mock_write.call_args[0][1])
        assert result["resource"] == "data"


class TestWriteRemoteFsspec(unittest.TestCase):
    """Test _write_remote with mocked fsspec."""

    @patch.dict("sys.modules", {"fsspec": MagicMock()})
    def test_write_remote_calls_fsspec_open(self) -> None:
        """_write_remote uses fsspec.open to write content."""
        import sys

        mock_fsspec = sys.modules["fsspec"]
        mock_file = StringIO()
        mock_fsspec.open.return_value.__enter__ = MagicMock(return_value=mock_file)
        mock_fsspec.open.return_value.__exit__ = MagicMock(return_value=False)

        PyHydrate._write_remote("s3://bucket/file.json", '{"key": "value"}\n')

        mock_fsspec.open.assert_called_once_with("s3://bucket/file.json", "w")

    def test_write_remote_import_error(self) -> None:
        """_write_remote raises ImportError when fsspec is not installed."""
        with patch.dict("sys.modules", {"fsspec": None}):
            with self.assertRaises(ImportError) as ctx:
                PyHydrate._write_remote("s3://bucket/file.json", "content")
            assert "fsspec" in str(ctx.exception)
            assert "pip install pyhydrate[cloud]" in str(ctx.exception)


class TestLocalPathUnaffected(unittest.TestCase):
    """Verify local save paths still work normally."""

    @patch("pyhydrate.pyhydrate.PyHydrate._write_remote")
    def test_local_save_does_not_call_write_remote(self, mock_write: MagicMock) -> None:
        """Local paths should not trigger _write_remote."""
        import tempfile

        data = PyHydrate({"key": "value"})
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            from pathlib import Path

            path = Path(f.name)

        try:
            data.save(path)
            mock_write.assert_not_called()
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
