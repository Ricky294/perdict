import os
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.perdict import PerDict


@pytest.fixture
def temp_perdict():
    with TemporaryDirectory() as temp_dir:
        yield PerDict(os.path.join(temp_dir, "test.json"))


def test_initialization(temp_perdict):
    assert isinstance(temp_perdict, PerDict)
    assert temp_perdict.autosave
    assert isinstance(temp_perdict.path, Path)


def test_loading_defaults(temp_perdict):
    defaults = {"key1": "value1", "key2": "value2"}
    temp_perdict = PerDict(temp_perdict.path, **defaults)

    assert temp_perdict["key1"] == "value1"
    assert temp_perdict["key2"] == "value2"


def test_save_explicit(temp_perdict):
    temp_perdict["key3"] = "value3"
    temp_perdict.save()

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert data["key3"] == "value3"


def test_save_autosave_off(temp_perdict):
    temp_perdict.autosave = False
    temp_perdict["key4"] = "value4"

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert "key4" not in data


def test_context_manager(temp_perdict):
    temp_perdict.autosave = False
    with temp_perdict as pd:
        pd["key5"] = "value5"

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert "key5" in data


def test_clear_no_autosave(temp_perdict):
    temp_perdict["key6"] = "value6"
    temp_perdict.autosave = False
    temp_perdict.clear()

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert len(data) > 0


def test_clear_autosave(temp_perdict):
    temp_perdict["key1"] = "value1"
    temp_perdict["key2"] = "value2"

    temp_perdict.clear()

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert len(data) == 0


def test_popitem_empty(temp_perdict):
    with pytest.raises(KeyError):
        temp_perdict.popitem()


def test_pop_default(temp_perdict):
    result = temp_perdict.pop("nonexistent_key", "default_value")
    assert result == "default_value"


def test_setdefault_no_autosave(temp_perdict):
    temp_perdict.autosave = False
    temp_perdict.setdefault("key7", "value7")

    with open(temp_perdict.path, "r") as f:
        data = json.load(f)
        assert "key7" not in data
