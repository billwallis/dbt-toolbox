import io

import ruamel.yaml

YAML = ruamel.yaml.YAML()
YAML.default_flow_style = False
YAML.indent(mapping=2, sequence=4, offset=2)
IDENTIFIER_QUOTES = [
    ('"', '"'),  # Snowflake, PostgreSQL, DuckDB
    ("`", "`"),  # BigQuery, Databricks
    ("[", "]"),  # T-SQL
]


def yaml_dumps(doc: dict) -> str:
    # TODO: Consider switching to:
    #           https://yaml.dev/doc/ruamel.yaml/example/#Output_of_%60dump()%60_as_a_string
    #       ...or only write to a YAML file once all models are collected (and write direct to file)
    with io.StringIO() as buffer:
        YAML.dump(doc, buffer)
        return buffer.getvalue()


def _is_quoted(identifier: str) -> bool:
    """
    Return ``True`` if the identifier is quoted, and ``False`` otherwise.
    """

    for left, right in IDENTIFIER_QUOTES:
        if identifier.startswith(left) and identifier.endswith(right):
            return True
    return False


def lower_identifier(identifier: str) -> str:
    # This assumes that if an identifier _is_ case-sensitive, that it is
    # quoted before reaching this application. This may not always be the
    # case, so we might need to do some dialect-specific fudging later
    if _is_quoted(identifier):
        return identifier

    return identifier.lower()
