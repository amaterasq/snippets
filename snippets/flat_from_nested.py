from typing import Any, Hashable, Mapping, Union

NestedMapping = Union[Mapping[Hashable, Any], list[Any], set[Any], tuple[Any, ...]]


def get_flat_dict_from_nested_mapping(
    nested_dict: NestedMapping,
    *,
    sep: str = ".",
    _parent_key: str = "",
) -> dict[str, Any]:
    """
    Преобразует вложенный Mapping или список в плоскую структуру.

    :param nested_dict: Вложенная структура для преобразования.
    :param sep: Разделитель между уровнями вложенности. По умолчанию - ".".
    :param _parent_key: Префикс ключа для текущей вложенности.
    :return: Плоский словарь.
    """
    items = {}

    for key, value in nested_dict.items() if isinstance(nested_dict, Mapping) else enumerate(nested_dict):
        new_key = f"{_parent_key}{sep}{key}" if _parent_key else str(key)
        if isinstance(value, (Mapping, list, tuple, set)):
            items.update(get_flat_dict_from_nested_mapping(value, sep=sep, _parent_key=new_key))
        else:
            items[new_key] = value

    return items


if __name__ == "__main__":
    print(get_flat_dict_from_nested_mapping({"a": {"b": "c"}}))
    print(get_flat_dict_from_nested_mapping({"a": [{"b": "c"}, {"d": "e"}]}))
