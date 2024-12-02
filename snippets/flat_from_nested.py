from typing import Any, Hashable, Iterable, Mapping


def get_flat_dict_from_nested_mapping(
        nested_dict: Mapping[Hashable, Any],
        *,
        sep: str = ".",
        _parent_key: str = "",
) -> dict[Hashable, Any]:
    """
    Преобразует вложенный Mapping в плоскую структуру.

    :param nested_dict: Вложенный словарь, который нужно преобразовать.
    :param sep: Разделитель между уровнями вложенности. По умолчанию - ".".
    :param _parent_key: Ключ верхнего уровня для текущей вложенности. По умолчанию - пустая строка.
    :return: Плоский словарь.
    """
    items = {}
    if isinstance(nested_dict, Mapping):
        for key, value in nested_dict.items():
            new_key = f"{_parent_key}{sep}{key}" if _parent_key else key
            if isinstance(value, (Mapping, Iterable)) and not isinstance(value, (str, bytes)):
                items.update(get_flat_dict_from_nested_mapping(value, sep=sep, _parent_key=new_key))
            else:
                items[new_key] = value
    elif isinstance(nested_dict, Iterable) and not isinstance(nested_dict, (str, bytes)):
        for index, value in enumerate(nested_dict):
            new_key = f"{_parent_key}{sep}{index}" if _parent_key else str(index)
            items.update(get_flat_dict_from_nested_mapping(value, sep=sep, _parent_key=new_key))
    else:
        items[_parent_key] = nested_dict
    return items



if __name__ == "__main__":
    print(get_flat_dict_from_nested_mapping({"a": {"b": "c"}}))
    print(get_flat_dict_from_nested_mapping({"a": [{"b": "c"}, {"d": "e"}]}))