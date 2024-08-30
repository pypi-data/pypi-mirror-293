"""@author: jldupont"""

import pytest
import json
from pygcloud.models import OptionalParam, LazyEnvValue
from pygcloud.utils import (
    flatten,
    split_head_tail,
    prepare_params,
    JsonObject,
    FlexJSONEncoder,
    normalize_for_id
)


@pytest.mark.parametrize(
    "liste,expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, 3]], [1, 2, 3]),
        ([1, (2, 3)], [1, (2, 3)]),
        ([[(1, 2)]], [(1, 2)]),
    ],
)
def test_flatten(liste, expected):
    assert flatten(liste) == expected


@pytest.mark.parametrize(
    "liste,expected",
    [
        (("head", ..., "tail"), (["head"], ["tail"])),
        (
            ("head",),
            (
                [
                    "head",
                ],
                [],
            ),
        ),
        ((...,), ([], [])),
        ((..., "tail"), ([], ["tail"])),
        ((), ([], [])),
    ],
)
def test_split_head_tail_base(liste, expected):
    head, tail = split_head_tail(liste)
    assert head == expected[0]
    assert tail == expected[1]


@pytest.mark.parametrize(
    "inp, expected",
    [
        (("key", "value"), ["key", "value"]),
        (["a", [("c", "d")]], ["a", "c", "d"]),
        ([OptionalParam("whatever", None)], []),
        (
            ["head", OptionalParam("whatever", True), "tail"],
            ["head", "whatever", "True", "tail"],
        ),
    ],
)
def test_prepare_params(inp, expected, env_first_key, env_first_value):
    assert prepare_params(inp) == expected


def test_prepare_params_lazy(env_first_key, env_first_value):
    lv = LazyEnvValue(env_first_key)

    liste = [lv, "tail"]
    result = prepare_params(liste)

    assert result == [env_first_value, "tail"], print(result)


def test_lazy_not_resolved():

    lv = LazyEnvValue("???whatever???")

    liste = [lv, "tail"]

    with pytest.raises(ValueError):
        prepare_params(liste)


@pytest.mark.parametrize(
    "obj, path,expected",
    [
        ({"l1": "v1"}, "l1", "v1"),
        ({"l1": {"l2": "v2"}}, "l1.l2", "v2"),
        ({"l1": {"l2": ["v2"]}}, "l1.l2", ["v2"]),
    ],
)
def test_json_obj(obj, path, expected):

    obj = JsonObject(**obj)
    assert obj[path] == expected


def test_flex_encoder():

    class mock:
        def to_dict(self):
            return "666"

    l = [555, mock()]

    js = json.dumps(l, cls=FlexJSONEncoder)

    assert isinstance(js, str), print(js)

    liste = json.loads(js)
    assert liste == [555, "666"], print(liste)


@pytest.mark.parametrize("input,expected", [
    ("allo", "allo"),
    ("gs://bucket", "gs_bucket"),
    ("first-second", "first_second")
])
def test_normalize_for_id(input, expected):
    assert normalize_for_id(input) == expected
