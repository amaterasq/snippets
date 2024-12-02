from types import MappingProxyType

from snippets.flat_from_nested import get_flat_dict_from_nested_mapping


def test_empty_mapping():
    assert get_flat_dict_from_nested_mapping({}) == {}, "empty mapping failed"


def test_simpe_nested():
    inp = {"a": "b", "c": {"d": "e"}, "f": {"y": {"z": 1}}}
    expected = {"a": "b", "c.d": "e", "f.y.z": 1}
    assert get_flat_dict_from_nested_mapping(inp) == expected, "simple nested fail"


def test_flat_dict_not_changed():
    inp = {"a": 1, "b": 2, "c": "3", "d": "4"}
    assert get_flat_dict_from_nested_mapping(inp) == inp, "flat dict not changed fail"


def test_real_data():
    inp = {
        "name": "Ravagh",
        "type": "Persian",
        "address": {
            "street": {
                "line1": "11 E 30th St",
                "line2": "APT 1",
            },
            "city": "New York",
            "state": "NY",
            "zip": 10016,
        }
    }
    expected = {
        "name": "Ravagh",
        "type": "Persian",
        "address.street.line1": "11 E 30th St",
        "address.street.line2": "APT 1",
        "address.city": "New York",
        "address.state": "NY",
        "address.zip": 10016,
    }
    assert get_flat_dict_from_nested_mapping(inp) == expected, "real data fail"


def test_real_data_with_custom_sep():
    inp = {
        "name": "Ravagh",
        "type": "Persian",
        "address": {
            "street": {
                "line1": "11 E 30th St",
                "line2": "APT 1",
            },
            "city": "New York",
            "state": "NY",
            "zip": 10016,
        }
    }
    expected = {
        "name": "Ravagh",
        "type": "Persian",
        "address/street/line1": "11 E 30th St",
        "address/street/line2": "APT 1",
        "address/city": "New York",
        "address/state": "NY",
        "address/zip": 10016,
    }
    assert get_flat_dict_from_nested_mapping(inp, sep="/") == expected, "real data with custom sep fail"


def test_nested_lists():
    nested = {
        "x": [[[{"y": "z"}]]],
        "a": [1, 2, {"b": [3, 4]}],
    }
    expected = {
        "x.0.0.0.y": "z",
        "a.0": 1,
        "a.1": 2,
        "a.2.b.0": 3,
        "a.2.b.1": 4,
    }
    assert get_flat_dict_from_nested_mapping(nested) == expected, "nested lists fail"


def test_any_type_and_nested():
    # Тест 3: Списки, строки, числа
    nested = {
        "key": [
            {"subkey1": "value1", "subkey2": [10, 20]},
            "string",
            123,
        ],
        "another_key": {"nested_key": "nested_value"},
    }
    expected = {
        "key.0.subkey1": "value1",
        "key.0.subkey2.0": 10,
        "key.0.subkey2.1": 20,
        "key.1": "string",
        "key.2": 123,
        "another_key.nested_key": "nested_value",
    }
    assert get_flat_dict_from_nested_mapping(nested) == expected, "any type and nested fail"


def test_deep_nested():
    nested = {"a": {"b": {"c": {"d": {"e": {"f": "g"}}}}}}
    expected = {"a.b.c.d.e.f": "g"}
    assert get_flat_dict_from_nested_mapping(nested) == expected, "deep nested fail"


def test_immutable_mapping():
    inp = MappingProxyType({"a": "b", "c": {"d": "e"}, "f": {"y": {"z": 1}}})
    expected = {"a": "b", "c.d": "e", "f.y.z": 1}
    assert get_flat_dict_from_nested_mapping(inp) == expected, "immutable mapping fail"
