import pytest

from faas_framework.utils.collections import CaseInsensitiveDict

case_insensitive_dict = CaseInsensitiveDict(**{"hello": "world", "WoRlD": "hello"})


class TestCaseInsensitiveDict:
    @pytest.mark.parametrize(
        "key,value",
        [
            ("hello", "world"),
            ("HeLlO", "world"),
            ("world", "hello"),
            ("wORld", "hello"),
        ],
    )
    def test_get(self, key, value):
        assert case_insensitive_dict.get(key) == value

    def test_items(self):
        items = case_insensitive_dict.items()
        assert len(items) == 2

    def test_keys(self):
        keys = case_insensitive_dict.keys()
        for k in ["hello", "world"]:
            assert k in keys

    def test_values(self):
        values = case_insensitive_dict.values()
        for v in ["hello", "world"]:
            assert v in values

    def test_eq(self):
        d = {"HellO": "world", "wOrLd": "hello"}
        assert d == case_insensitive_dict

    def test_not_eq(self):
        _copy = case_insensitive_dict.copy()
        _copy["a"] = "b"
        assert case_insensitive_dict != _copy

    def test_not_comparable(self):
        assert NotImplemented == case_insensitive_dict.__eq__(
            "{'hello': 'world', 'WoRlD': 'hello'}"
        )

    def test_copy(self):
        assert case_insensitive_dict.copy() == case_insensitive_dict

    def test_len(self):
        assert len(case_insensitive_dict) == 2

    def test_del(self):
        _copy = case_insensitive_dict.copy()
        _copy.pop("hello")
        assert len(_copy) == 1

    def test_repr(self):
        assert repr(case_insensitive_dict) == "{'hello': 'world', 'WoRlD': 'hello'}"
