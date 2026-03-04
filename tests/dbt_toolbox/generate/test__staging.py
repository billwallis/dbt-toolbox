import textwrap

import pytest

from dbt_toolbox.generate import staging


def test__model__file_name_includes_source_and_object():
    model = staging.Model(
        source_name="jaffle_shop",
        model_name="orderlines",
        columns=[],
    )

    assert model.file_name == "stg_jaffle_shop__order_lines"


@pytest.mark.parametrize(
    "model, expected_sql",
    [
        (
            staging.Model(
                source_name="jaffle_shop",
                model_name="orderlines",
                columns=[
                    staging.Column(
                        column_name="id",
                        data_type="text",
                        ordinal_position=1,
                    ),
                    staging.Column(
                        column_name="type",
                        data_type="text",
                        ordinal_position=2,
                    ),
                    staging.Column(
                        column_name="amount",
                        data_type="numeric",
                        ordinal_position=3,
                    ),
                    staging.Column(
                        column_name="createddate",
                        data_type="date",
                        ordinal_position=4,
                    ),
                    staging.Column(
                        column_name="updateddate",
                        data_type="date",
                        ordinal_position=5,
                    ),
                    staging.Column(
                        column_name="_airbyte_raw_id",
                        data_type="date",
                        ordinal_position=6,
                    ),
                ],
            ),
            textwrap.dedent(
                """\
                with

                order_lines as (
                    select
                        id,
                        type,
                        amount,
                        createddate as created_date,
                        updateddate as updated_date,
                        _airbyte_raw_id
                    from {{ source('jaffle_shop', 'orderlines') }}
                )

                select * from order_lines
                """
            ),
        ),
    ],
)
def test__generate_staging_model_sql__happy_path(
    model: staging.Model,
    expected_sql: str,
):
    assert staging.generate_staging_model_sql(model) == expected_sql


@pytest.mark.parametrize(
    "model, expected_yaml",
    [
        (
            staging.Model(
                source_name="jaffle_shop",
                model_name="orderlines",
                columns=[
                    staging.Column(
                        column_name="id",
                        data_type="text",
                        ordinal_position=1,
                    ),
                    staging.Column(
                        column_name="type",
                        data_type="text",
                        ordinal_position=2,
                    ),
                    staging.Column(
                        column_name="amount",
                        data_type="numeric",
                        ordinal_position=3,
                    ),
                    staging.Column(
                        column_name="createddate",
                        data_type="date",
                        ordinal_position=4,
                    ),
                    staging.Column(
                        column_name="updateddate",
                        data_type="date",
                        ordinal_position=5,
                    ),
                    staging.Column(
                        column_name="_airbyte_raw_id",
                        data_type="text",
                        ordinal_position=6,
                    ),
                ],
            ),
            # textwrap.dedent(
            #     """\
            #     name: order_lines
            #     description:
            #     columns:
            #       - name: id
            #         data_type: text
            #         description:
            #       - name: type
            #         data_type: text
            #         description:
            #       - name: amount
            #         data_type: numeric
            #         description:
            #       - name: created_date
            #         data_type: date
            #         description:
            #       - name: updated_date
            #         data_type: date
            #         description:
            #       - name: _airbyte_raw_id
            #         data_type: text
            #         description:
            #     """
            # ),
            {
                "name": "order_lines",
                "description": None,
                "columns": [
                    {
                        "name": "id",
                        "data_type": "text",
                        "description": None,
                    },
                    {
                        "name": "type",
                        "data_type": "text",
                        "description": None,
                    },
                    {
                        "name": "amount",
                        "data_type": "numeric",
                        "description": None,
                    },
                    {
                        "name": "created_date",
                        "data_type": "date",
                        "description": None,
                    },
                    {
                        "name": "updated_date",
                        "data_type": "date",
                        "description": None,
                    },
                    {
                        "name": "_airbyte_raw_id",
                        "data_type": "text",
                        "description": None,
                    },
                ],
            },
        ),
    ],
)
def test__generate_staging_model_yaml__happy_path(
    model: staging.Model,
    expected_yaml: dict,
):
    assert staging.generate_staging_model_yaml(model) == expected_yaml


@pytest.mark.parametrize(
    "models, expected_yaml",
    [
        (
            [
                staging.Model(source_name="foo", model_name="a", columns=[]),
                staging.Model(source_name="foo", model_name="b", columns=[]),
                staging.Model(source_name="foo", model_name="c", columns=[]),
                staging.Model(source_name="bar", model_name="a", columns=[]),
                staging.Model(source_name="bar", model_name="b", columns=[]),
                staging.Model(source_name="baz", model_name="c", columns=[]),
            ],
            {
                "version": 2,
                "sources": [
                    {
                        "name": "foo",
                        "database": None,
                        "schema": None,
                        "tables": [
                            {"name": "a"},
                            {"name": "b"},
                            {"name": "c"},
                        ],
                    },
                    {
                        "name": "bar",
                        "database": None,
                        "schema": None,
                        "tables": [
                            {"name": "a"},
                            {"name": "b"},
                        ],
                    },
                    {
                        "name": "baz",
                        "database": None,
                        "schema": None,
                        "tables": [
                            {"name": "c"},
                        ],
                    },
                ],
            },
        ),
    ],
)
def test__generate_sources_yaml__happy_path(
    models: list[staging.Model],
    expected_yaml: dict,
):
    assert staging.generate_sources_yaml(models) == expected_yaml
