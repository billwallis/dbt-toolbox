import textwrap

import pytest

from dbt_toolbox import utils


@pytest.mark.parametrize(
    "doc, expected_yaml",
    [
        (
            {
                "foo": "Qapla'!",
                "bar": {
                    "foo": "",
                    "bar": False,
                    "baz": 0,
                    "qux": None,
                },
                "baz": [
                    "yes",
                    True,
                    42,
                    {"x": ("y", "z")},
                ],
            },
            textwrap.dedent(
                """\
                foo: Qapla'!
                bar:
                  foo: ''
                  bar: false
                  baz: 0
                  qux:
                baz:
                  - yes
                  - true
                  - 42
                  - x:
                      - y
                      - z
                """
            ),
        ),
    ],
)
def test__yaml_dumps__happy_path(doc: dict, expected_yaml: str):
    assert utils.yaml_dumps(doc) == expected_yaml
