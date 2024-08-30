"""
@author: jldupont
"""

import json
from collections.abc import Iterable
from typing import List, Any, Tuple, Union


def flatten(*liste: Union[List[Any], Tuple[Any]]):
    """
    Flatten a list of lists
    """
    assert isinstance(liste, tuple), f"Expected list, got: {type(liste)}"

    result = []
    for item in liste:
        if isinstance(item, list):
            result.extend(flatten(*item))
        else:
            result.append(item)
    return result


def split_head_tail(liste: List[Any]) -> Tuple[List[Any], List[Any]]:
    """
    Cases:
    1) head ... tail ---> normal case
    2) ... tail      ---> degenerate
    3) tail          ---> normal case
    4) ...           ---> degenerate
    """
    head: List[Any] = []
    tail: List[Any] = []

    current = head

    for item in liste:

        if item is ...:
            current = tail
            continue

        current.append(item)

    return (head, tail)


def prepare_params(params: Union[List[Any], List[Tuple[str, str]]]) -> List[Any]:
    """
    Prepare a list of parameters for a command line invocation

    Must also ensure there are no whitespace separated entries.

    We use 'str' on all items because of potential special instances
    such as LazyEnvValue.
    """
    from .models import Param, LazyValue

    liste: List[Any] = flatten(params)
    item: Any
    new_liste = []

    for item in liste:

        if isinstance(item, LazyValue):
            try:
                value = item.value
            except ValueError:
                raise ValueError(f"Dependency not resolved on {repr(item)}")
            new_liste.append(value)
            continue

        if isinstance(item, str):

            # We need to have str() on top
            # because of types such as LazyEnvValue
            new_liste.append(str(item))
            continue

        if isinstance(item, Iterable) or isinstance(item, Param):
            for subitem in item:
                new_liste.append(str(subitem))
            continue

        new_liste.append(str(item))

    return new_liste


class DotDict(dict):
    """
    A dictionary like object where values
    can be accessed through nested dot paths

    e.g.
        d = DoctAccessibleDict({"l1": {"l2": "v2"}})
        value = d["l1.l2"]
        assert value == "v2"
    """

    def __getitem__(self, path):
        if "." not in path:
            return super().__getitem__(path)

        result = None
        parts = path.split(".")
        current = self

        for part in parts:
            result = current.get(part, None)
            if result is None:
                break
            if not isinstance(result, dict):
                break
            current = result

        return result


class JsonObject(DotDict):
    """
    Utility class for handling JSON objects
    """

    @classmethod
    def from_string(cls, json_str: str):
        """
        Build an instance from a JSON string
        """
        json_obj = json.loads(json_str)
        return cls(json_obj)


class FlexJSONEncoder(json.JSONEncoder):

    def default(self, o):
        """
        The purpose is to return an object
        that can be JSON serializable
        """
        if not getattr(o, "to_dict", False):
            return json.JSONEncoder.default(self, o)

        return o.to_dict()


ALLOWED_CHARS = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')


def normalize_for_id(input: str) -> str:
    """
    Replace unsupported characters
    """
    input = input.replace("://", "_").replace("-", "_")
    return ''.join(c for c in input if c in ALLOWED_CHARS)
