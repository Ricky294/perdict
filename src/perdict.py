import json
from pathlib import Path
from typing import TypeVar, Any, Self

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class PerDict(dict):

    def __init__(self, path, autosave=True, **defaults: Any) -> None:
        super().__init__()

        self.autosave = autosave
        self.path = Path(path)
        self.path.touch()

        if self.path.stat().st_size == 0:
            with open(self.path, 'w') as f:
                json.dump({}, f)
        else:
            with open(self.path, 'r') as f:
                data = json.load(f)
                dict.update(self, data)

        for key, value in defaults.items():
            dict.setdefault(self, key, value)

        self._autosave()

    def _autosave(self):
        if self.autosave:
            self.save()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.save()

    def __setitem__(self, __key: _KT, __val: _VT) -> None:
        dict.__setitem__(self, __key, __val)
        self._autosave()

    def __delitem__(self, __key: _KT) -> None:
        dict.__delitem__(self, __key)
        self._autosave()

    def __repr__(self) -> str:
        r = dict.__repr__(self)
        return f'{type(self).__name__}({r})'

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self, f)

    def update(self, __m, **kwargs: _VT) -> None:
        dict.update(self, __m, **kwargs)
        self._autosave()

    def clear(self) -> None:
        dict.clear(self)
        self._autosave()

    def pop(self, key: _KT, default: _VT = ...) -> _VT:
        result = dict.pop(self, key, default)
        self._autosave()
        return result

    def popitem(self) -> tuple[_KT, _VT]:
        result = dict.popitem(self)
        self._autosave()
        return result

    def setdefault(self, key: _KT, default: _VT = ...) -> _VT:
        result = dict.setdefault(self, key, default)
        if result == default:
            self._autosave()

        return result
