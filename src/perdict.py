import json
import os
from pathlib import Path
from typing import TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class PerDict(dict):

    def __init__(self, path, autosave=True) -> None:
        super().__init__()

        self.path = Path(path)
        self.path.touch()

        self.autosave = autosave

        if self.path.stat().st_size > 0:
            with open(self.path, 'r') as f:
                dict.update(self, json.load(f))

    def __setitem__(self, __key: _KT, __val: _VT) -> None:
        dict.__setitem__(self, __key, __val)
        if self.autosave:
            self._dump()

    def __delitem__(self, __key: _KT) -> None:
        dict.__delitem__(self, __key)
        if self.autosave:
            self._dump()

    def __repr__(self) -> str:
        r = dict.__repr__(self)
        return f'{type(self).__name__}({r})'

    def _dump(self):
        with open(self.path, 'w') as f:
            json.dump(self, f)

    def save(self) -> None:
        self._dump()

    def update(self, __m, **kwargs: _VT) -> None:
        dict.update(self, __m, **kwargs)
        if self.autosave:
            self._dump()

    def clear(self) -> None:
        dict.clear(self)
        os.truncate(self.path, 0)

    def pop(self, key: _KT, default: _VT = ...) -> _VT:
        result = dict.pop(self, key, default)
        if self.autosave:
            self._dump()
        return result

    def popitem(self) -> tuple[_KT, _VT]:
        result = dict.popitem(self)
        if self.autosave:
            self._dump()
        return result

    def setdefault(self, key: _KT, default: _VT = ...) -> _VT:
        result = dict.setdefault(self, key, default)
        if self.autosave and result == default:
            self._dump()
        return result
