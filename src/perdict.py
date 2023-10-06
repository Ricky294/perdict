import json
from pathlib import Path
from typing import TypeVar, Any

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class PerDict(dict):
    """
    A dictionary-like object that automatically saves its contents to a JSON file.

    Args:
        path (str): The path to the JSON file.
        autosave (bool, optional): Whether to automatically save changes to the file (default is True).
        **defaults: Default key-value pairs to initialize the dictionary.

    Attributes:
        autosave (bool): Whether automatic saving is enabled.
        path (Path): The path to the JSON file.

    Example:
        >>> obj = PerDict('file.json', x=5, y=6)
        >>> print(obj.x)  # Access default values as attributes
        5
        >>> obj.z = 10  # Add or modify dictionary entries
        >>> del obj.y  # Delete dictionary entries
        >>> obj.save()  # Manually save changes to the JSON file
    """

    __slots__ = "autosave", "path"

    def __init__(self, path: str, autosave: bool = True, **defaults: Any) -> None:
        """
        Initialize a PerDict object.

        Args:
            path (str): The path to the JSON file.
            autosave (bool, optional): Whether to automatically save changes to the file (default is True).
            **defaults: Default key-value pairs to initialize the dictionary.
        """
        super().__init__()

        self.autosave = autosave
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()

        if self.path.stat().st_size != 0:
            with open(self.path, 'r') as f:
                data = json.load(f)
                dict.update(self, data)

        self.set_defaults(defaults)
        self._autosave()

    def set_defaults(self, defaults: dict):
        for k, v in defaults.items():
            dict.setdefault(self, k, v)

    def _autosave(self) -> None:
        """
        Save the dictionary to the JSON file if autosave is enabled.
        """
        if self.autosave:
            self.save()

    def __enter__(self) -> 'PerDict':
        """
        Enter the context manager. Returns self for use in 'with' statements.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the context manager and save the dictionary.
        """
        self.save()

    def __setitem__(self, key: _KT, value: _VT) -> None:
        """
        Set a dictionary item using the item assignment operator.

        Args:
            key: The key to set.
            value: The value to assign to the key.
        """
        dict.__setitem__(self, key, value)
        self._autosave()

    def __delitem__(self, key: _KT) -> None:
        """
        Delete a dictionary item by key.

        Args:
            key: The key to delete.
        """
        dict.__delitem__(self, key)
        self._autosave()

    def __repr__(self) -> str:
        """
        Return a string representation of the PerDict object.
        """
        r = dict.__repr__(self)
        return f'{type(self).__name__}({r})'

    def save(self, data: dict = None) -> None:
        """
        Save the dictionary to the JSON file.
        """

        if data is not None:
            for k, v in data.items():
                self[k] = v

        with open(self.path, 'w') as f:
            json.dump(self, f)

    def update(self, __m, **kwargs: _VT) -> None:
        """
        Update the dictionary with key-value pairs from another dictionary.

        Args:
            __m: The dictionary-like object to update from.
            **kwargs: Additional key-value pairs to update with.
        """
        dict.update(self, __m, **kwargs)
        self._autosave()

    def clear(self) -> None:
        """
        Clear all items from the dictionary.
        """
        dict.clear(self)
        self._autosave()

    def pop(self, key: _KT, default: _VT = ...) -> _VT:
        """
        Remove and return the value associated with a key.

        Args:
            key: The key to remove.
            default: The value to return if the key is not found (default is '...').

        Returns:
            _VT: The value associated with the key.

        Raises:
            KeyError: If the key is not found and no default value is provided.
        """
        result = dict.pop(self, key, default)
        self._autosave()
        return result

    def popitem(self) -> tuple[_KT, _VT]:
        """
        Remove and return a (key, value) pair from the dictionary.

        Returns:
            tuple[_KT, _VT]: The removed (key, value) pair.
        """
        result = dict.popitem(self)
        self._autosave()
        return result

    def setdefault(self, key: _KT, default: _VT = ...) -> _VT:
        """
        Set a key to a default value if it does not exist in the dictionary.

        Args:
            key: The key to set.
            default: The default value to assign if the key is not found (default is '...').

        Returns:
            _VT: The existing or newly set value associated with the key.
        """
        result = dict.setdefault(self, key, default)
        if result == default:
            self._autosave()

        return result
