import re
import textwrap

# Not supported by JetBrains :melt:
SOURCE_PATTERN = re.compile(
    r"""{{\s*source\s*\(\s*(?P<q1>['"])(?P<source>\w+)(?P=q1)\s*,\s*(?P<q2>['"])(?P<identifier>\w+)(?P=q2)\s*\)\s*}}""",
    re.MULTILINE | re.IGNORECASE,
)
REF_PATTERN = re.compile(
    r"""{{\s*ref\s*\(\s*(?P<q>['"])(?P<identifier>\w+)(?P=q)\s*\)\s*}}""",
    re.MULTILINE | re.IGNORECASE,
)

# Supported by JetBrains :smile:
_SOURCE_PATTERN = re.compile(
    r"""\{\{\s*source\s*\(\s*['"](\w+)['"]\s*,\s*['"](\w+)['"]\s*\)\s*}}""",
    re.MULTILINE | re.IGNORECASE,
)
# Replace: `DATABASE.$1.$2`
_REF_PATTERN = re.compile(
    r"""\{\{\s*ref\s*\(\s*['"](\w+)['"]\s*\)\s*}}""",
    re.MULTILINE | re.IGNORECASE,
)
# Replace: `DATABASE.SCHEMA.$1`


def extract_sources(text: str) -> list[tuple[str, str]]:
    return [
        (match[1], match[3])
        for match in SOURCE_PATTERN.findall(text)
    ]


def extract_refs(text: str) -> list[str]:
    return [match[1] for match in REF_PATTERN.findall(text)]



EXAMPLE_SQL = textwrap.dedent(
    """\
    select *
    from {{ source("foo", "table_1") }}
    join {{source('foo','table_2')}}
    join {{   SOURCE(  'foo'  ,  "table_3"  )   }}
    join {{ ref("model_1") }}
    join {{ref("model_2")}}
    join {{   REF(  "model_3"  )   }}
    """
)


def test__extract_sources():
    matches = sorted(extract_sources(EXAMPLE_SQL))
    assert matches == [
        ("foo", "table_1"),
        ("foo", "table_2"),
        ("foo", "table_3"),
    ]


def test__extract_refs():
    matches = sorted(extract_refs(EXAMPLE_SQL))
    assert matches == ["model_1", "model_2", "model_3"]


def main() -> int:
    test__extract_sources()
    test__extract_refs()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
