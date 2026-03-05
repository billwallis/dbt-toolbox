"""
Generate dbt staging models.
"""

from __future__ import annotations

import collections
import dataclasses
import textwrap

import wordninja


def _split_name(name: str) -> str:
    # TODO: Should be replaced with some injectable conditions
    if name.startswith("_"):
        return name
    else:
        return "_".join(wordninja.split(name))


@dataclasses.dataclass
class Column:
    column_name: str
    data_type: str
    ordinal_position: int
    alias: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.alias = _split_name(self.column_name)


@dataclasses.dataclass
class Model:
    source_name: str
    model_name: str
    columns: list[Column]
    alias: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.alias = _split_name(self.model_name)

    @property
    def file_name(self) -> str:
        return f"stg_{self.source_name}__{self.alias}"


def generate_staging_model_sql(model: Model) -> str:
    column_aliases = [
        (
            col.column_name
            if col.column_name == col.alias
            else f"{col.column_name} as {col.alias}"
        )
        for col in model.columns
    ]
    return textwrap.dedent(
        f"""\
        with

        {model.alias} as (
            select{"\n" + textwrap.indent(",\n".join(column_aliases), prefix=16 * " ")}
            from {{{{ source('{model.source_name}', '{model.model_name}') }}}}
        )

        select * from {model.alias}
        """  # noqa: S608
    )


def generate_staging_model_yaml(model: Model) -> dict:
    return {
        "name": model.file_name,
        "description": None,
        "columns": [
            {
                "name": col.alias,
                "data_type": col.data_type,
                "description": None,
            }
            for col in sorted(model.columns, key=lambda c: c.ordinal_position)
        ],
    }


def generate_sources_yaml(models: list[Model]) -> dict:
    sources = collections.defaultdict(list)
    for model in models:
        sources[model.source_name].append({"name": model.model_name})

    return {
        "version": 2,
        "sources": [
            {
                "name": source_name,
                "database": None,
                "schema": None,
                "tables": tables,
            }
            for source_name, tables in sources.items()
        ],
    }
