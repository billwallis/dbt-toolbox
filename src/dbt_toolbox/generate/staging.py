"""
Generate dbt staging models.
"""

from __future__ import annotations

import collections
import dataclasses
import textwrap

import wordninja

from dbt_toolbox import utils


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
        self.column_name = utils.lower_identifier(self.column_name)
        self.data_type = self.data_type.lower()
        self.ordinal_position = int(self.ordinal_position)
        self.alias = _split_name(self.column_name).lower()


@dataclasses.dataclass
class Model:
    source_name: str
    model_name: str
    columns: list[Column]
    alias: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.model_name = utils.lower_identifier(self.model_name)
        self.alias = _split_name(self.model_name).lower()

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
