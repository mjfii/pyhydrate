"""
Provides the NotationProxy class for deep auto-creation of nested structures.

NotationProxy is a lightweight proxy returned when accessing a missing key
on a NotationObject. It records a chain of pending keys and materializes
intermediate dicts when a value is assigned via dot notation.

This enables patterns like:
    x = PyHydrate()
    x.a.b.c = 1  # creates {"a": {"b": {"c": 1}}}
"""

from typing import Any, Union

_DEFAULT_MAX_PROXY_DEPTH = 100


class NotationProxy:
    """
    Proxy object for deferred creation of nested dict structures.

    When a missing key is accessed on a NotationObject, a NotationProxy
    is returned instead of NotationPrimitive(None). The proxy records
    the parent object and key, and supports chaining via __getattr__.

    On assignment (__setattr__), the proxy walks up the chain and
    materializes all intermediate dicts in the parent's _raw_value.

    For read operations (__call__, __bool__, etc.), it behaves like
    a None value for backward compatibility.
    """

    __slots__ = ("_proxy_depth", "_proxy_key", "_proxy_max_depth", "_proxy_parent")

    def __init__(
        self,
        *,
        parent: Any,
        parent_key: str,
        depth: int = 1,
        max_depth: int = _DEFAULT_MAX_PROXY_DEPTH,
    ) -> None:
        """
        Initialize with the parent object and the missing key.

        Parameters:
            parent: The parent NotationObject, PyHydrate, or NotationProxy
            parent_key: The key that was not found in the parent
            depth: Current depth of this proxy in the chain
            max_depth: Maximum allowed proxy chain depth
        """
        object.__setattr__(self, "_proxy_parent", parent)
        object.__setattr__(self, "_proxy_key", parent_key)
        object.__setattr__(self, "_proxy_depth", depth)
        object.__setattr__(self, "_proxy_max_depth", max_depth)

    def __getattr__(self, key: str) -> "NotationProxy":
        """
        Chain another level of deferred creation.

        Parameters:
            key (str): The next key in the chain

        Returns:
            NotationProxy: A new proxy linked to this one

        Raises:
            RecursionError: If the proxy chain exceeds max_proxy_depth
        """
        next_depth = self._proxy_depth + 1
        if next_depth > self._proxy_max_depth:
            raise RecursionError(
                f"Maximum proxy chain depth ({self._proxy_max_depth}) exceeded. "
                f"This usually indicates an unintended deep attribute access. "
                f"If intentional, set max_proxy_depth to a higher value."
            )
        return NotationProxy(
            parent=self,
            parent_key=key,
            depth=next_depth,
            max_depth=self._proxy_max_depth,
        )

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Materialize the full chain of intermediate dicts and set the value.

        Walks up the proxy chain collecting keys, then builds the nested
        dict structure and writes it into the root parent's _raw_value.

        Parameters:
            key (str): The final key to set
            value: The value to assign
        """
        from .notation_base import NotationBase

        raw_value = NotationBase._unwrap(value)

        # Collect the chain of keys from leaf to root
        # Start with the final assignment key
        result = raw_value
        keys = [key]

        current = self
        while isinstance(current, NotationProxy):
            keys.append(current._proxy_key)
            current = current._proxy_parent

        # current is now the root parent (NotationObject or PyHydrate)
        # Build nested dict from inside out (keys are leaf-to-root order)
        nested = result
        for k in keys[:-1]:  # All keys except the outermost
            nested = {k: nested}

        # The outermost key assignment goes to the root parent
        outermost_key = keys[-1]

        # Check if root is PyHydrate (has _structure in __slots__)
        from .notation_structures import NotationObject

        if "_structure" in getattr(type(current), "__slots__", ()):
            structure = current._structure
            # If structure is not a NotationObject, promote it
            if not isinstance(structure, NotationObject):
                new_obj = NotationObject({}, 0, **getattr(current, "_kwargs", {}))
                object.__setattr__(current, "_structure", new_obj)
                object.__setattr__(current, "_root_type", dict)
                object.__setattr__(current, "_raw_value", new_obj._raw_value)
                structure = new_obj
            structure._set_value(outermost_key, nested)
        else:
            # Root is a NotationObject
            current._set_value(outermost_key, nested)

    def __call__(
        self, *args: Any
    ) -> Union[dict, list, str, int, float, bool, type, None]:
        """
        Behave like NotationPrimitive(None) for reads.

        Returns:
            None for 'value' calls, appropriate None representations for others
        """
        call_type = args[0] if args else "value"
        if call_type == "value":
            return None
        if call_type == "type":
            return type(None)
        if call_type == "element":
            return {"NoneType": None}
        if call_type == "depth":
            return 0
        if call_type == "map":
            return None
        if call_type == "json":
            import json

            return json.dumps({"NoneType": None}, indent=3)
        if call_type == "yaml":
            import yaml

            from .notation_dumper import NotationDumper

            return yaml.dump(
                {"NoneType": None}, sort_keys=False, Dumper=NotationDumper
            ).rstrip()
        if call_type == "toml":
            return None
        return None

    def __repr__(self) -> str:
        """Return repr consistent with NotationPrimitive(None)."""
        return "PyHydrate(None)"

    def __str__(self) -> str:
        """Return string consistent with NotationPrimitive(None)."""
        return "NoneType: null"

    def __bool__(self) -> bool:
        """Proxy is falsy like None."""
        return False

    def __int__(self) -> int:
        """Cannot convert None to int."""
        raise TypeError("Cannot convert NoneType to int")

    def __float__(self) -> float:
        """Cannot convert None to float."""
        raise TypeError("Cannot convert NoneType to float")

    def __getitem__(self, index: Any) -> "NotationProxy":
        """
        Return a proxy for index access (behaves like None).

        Parameters:
            index: The index

        Returns:
            NotationProxy: A new proxy

        Raises:
            RecursionError: If the proxy chain exceeds max_proxy_depth
        """
        next_depth = self._proxy_depth + 1
        if next_depth > self._proxy_max_depth:
            raise RecursionError(
                f"Maximum proxy chain depth ({self._proxy_max_depth}) exceeded. "
                f"This usually indicates an unintended deep attribute access. "
                f"If intentional, set max_proxy_depth to a higher value."
            )
        return NotationProxy(
            parent=self,
            parent_key=index,
            depth=next_depth,
            max_depth=self._proxy_max_depth,
        )
