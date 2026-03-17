"""
Test cases for proxy chain depth limiting (Issue #3).

Covers:
- Default max depth of 100 raises RecursionError
- Custom max_proxy_depth via kwargs
- Depth tracking through __getattr__ and __getitem__ chains
- Normal usage well within the limit
- Depth limit applies to PyHydrate primitive proxy entry point
- Error message content and actionable guidance
"""

import unittest

from pyhydrate import PyHydrate


class TestDefaultProxyDepthLimit(unittest.TestCase):
    """Test that the default proxy depth of 100 is enforced."""

    def test_exceeding_default_depth_raises_recursion_error(self) -> None:
        """Test that accessing 101 levels deep raises RecursionError."""
        data = PyHydrate({})
        ref = data.a  # depth 1
        for _ in range(99):
            ref = ref.b  # depths 2..100
        # depth 100 is the last allowed; next access should fail
        with self.assertRaises(RecursionError):
            ref.c  # noqa: B018 — depth 101

    def test_exactly_at_default_depth_does_not_raise(self) -> None:
        """Test that accessing exactly 100 levels deep does not raise."""
        data = PyHydrate({})
        ref = data.a  # depth 1
        for _ in range(98):
            ref = ref.b  # depths 2..99
        # depth 99 from loop + 1 more = 100, should not raise
        result = ref.final
        assert result() is None

    def test_shallow_access_unaffected(self) -> None:
        """Test that normal shallow proxy access works fine."""
        data = PyHydrate({})
        assert data.x.y.z() is None

    def test_single_missing_key_unaffected(self) -> None:
        """Test that a single missing key works fine."""
        data = PyHydrate({"a": 1})
        assert data.missing() is None


class TestCustomProxyDepthLimit(unittest.TestCase):
    """Test that max_proxy_depth can be configured via kwargs."""

    def test_custom_lower_limit(self) -> None:
        """Test that a custom lower limit is enforced."""
        data = PyHydrate({}, max_proxy_depth=5)
        ref = data.a  # depth 1
        ref = ref.b  # depth 2
        ref = ref.c  # depth 3
        ref = ref.d  # depth 4
        ref = ref.e  # depth 5
        with self.assertRaises(RecursionError):
            ref.f  # noqa: B018 — depth 6

    def test_custom_limit_of_1(self) -> None:
        """Test that a max_proxy_depth of 1 allows only one level."""
        data = PyHydrate({}, max_proxy_depth=1)
        proxy = data.missing  # depth 1, allowed
        assert proxy() is None
        with self.assertRaises(RecursionError):
            proxy.deeper  # noqa: B018 — depth 2

    def test_custom_higher_limit(self) -> None:
        """Test that a custom higher limit allows deeper access."""
        data = PyHydrate({}, max_proxy_depth=200)
        ref = data.a
        for _ in range(198):
            ref = ref.b  # up to depth 199
        result = ref.final  # depth 200, should be allowed
        assert result() is None

    def test_custom_higher_limit_still_enforced(self) -> None:
        """Test that exceeding the custom higher limit raises."""
        data = PyHydrate({}, max_proxy_depth=200)
        ref = data.a
        for _ in range(199):
            ref = ref.b  # up to depth 200
        with self.assertRaises(RecursionError):
            ref.c  # noqa: B018 — depth 201

    def test_custom_limit_on_existing_data(self) -> None:
        """Test that max_proxy_depth works with populated data."""
        data = PyHydrate({"a": {"b": 1}}, max_proxy_depth=3)
        # Accessing existing keys doesn't consume proxy depth
        assert data.a.b() == 1
        # Accessing a missing key starts a proxy chain
        ref = data.a.missing  # depth 1
        ref = ref.deeper  # depth 2
        ref = ref.more  # depth 3
        with self.assertRaises(RecursionError):
            ref.too_deep  # noqa: B018 — depth 4


class TestProxyDepthWithGetitem(unittest.TestCase):
    """Test that __getitem__ also respects depth limits."""

    def test_getitem_increments_depth(self) -> None:
        """Test that bracket access on proxy increments depth."""
        data = PyHydrate({}, max_proxy_depth=3)
        ref = data.a  # depth 1
        ref = ref[0]  # depth 2
        ref = ref[1]  # depth 3
        with self.assertRaises(RecursionError):
            ref[2]

    def test_mixed_getattr_getitem_depth(self) -> None:
        """Test that mixed attr/index access accumulates depth."""
        data = PyHydrate({}, max_proxy_depth=4)
        ref = data.a  # depth 1
        ref = ref[0]  # depth 2
        ref = ref.b  # depth 3
        ref = ref[1]  # depth 4
        with self.assertRaises(RecursionError):
            ref.c  # noqa: B018 — depth 5


class TestProxyDepthFromPrimitive(unittest.TestCase):
    """Test depth limiting when proxy originates from PyHydrate primitive."""

    def test_primitive_proxy_respects_default_limit(self) -> None:
        """Test proxy from PyHydrate(None) respects depth limit."""
        data = PyHydrate(None)
        ref = data.a  # depth 1
        for _ in range(98):
            ref = ref.b  # depths 2..99
        result = ref.final  # depth 100
        assert result() is None
        with self.assertRaises(RecursionError):
            result.overflow  # noqa: B018 — depth 101

    def test_primitive_proxy_respects_custom_limit(self) -> None:
        """Test proxy from PyHydrate(None) respects custom limit."""
        data = PyHydrate(None, max_proxy_depth=3)
        ref = data.a  # depth 1
        ref = ref.b  # depth 2
        ref = ref.c  # depth 3
        with self.assertRaises(RecursionError):
            ref.d  # noqa: B018 — depth 4

    def test_empty_pyhydrate_proxy_respects_custom_limit(self) -> None:
        """Test proxy from PyHydrate() respects custom limit."""
        data = PyHydrate(max_proxy_depth=2)
        ref = data.a  # depth 1
        ref = ref.b  # depth 2
        with self.assertRaises(RecursionError):
            ref.c  # noqa: B018 — depth 3


class TestProxyDepthErrorMessage(unittest.TestCase):
    """Test that the RecursionError message is informative."""

    def test_error_message_includes_depth(self) -> None:
        """Test error message contains the configured max depth."""
        data = PyHydrate({}, max_proxy_depth=10)
        ref = data.a
        for _ in range(9):
            ref = ref.b
        with self.assertRaises(RecursionError) as ctx:
            ref.c  # noqa: B018
        msg = str(ctx.exception)
        assert "10" in msg

    def test_error_message_includes_guidance(self) -> None:
        """Test error message suggests increasing max_proxy_depth."""
        data = PyHydrate({}, max_proxy_depth=5)
        ref = data.a
        for _ in range(4):
            ref = ref.b
        with self.assertRaises(RecursionError) as ctx:
            ref.c  # noqa: B018
        msg = str(ctx.exception)
        assert "max_proxy_depth" in msg


class TestProxyDepthWriteThrough(unittest.TestCase):
    """Test that write-through still works within depth limits."""

    def test_deep_write_within_limit(self) -> None:
        """Test that deep auto-creation works within the depth limit."""
        data = PyHydrate({}, max_proxy_depth=10)
        data.a.b.c.d = "value"
        assert data.a.b.c.d() == "value"

    def test_write_at_custom_limit(self) -> None:
        """Test that writing exactly at the custom limit works."""
        data = PyHydrate({}, max_proxy_depth=3)
        data.a.b.c = 42
        assert data.a.b.c() == 42


if __name__ == "__main__":
    unittest.main()
