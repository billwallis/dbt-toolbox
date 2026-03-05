import pytest

from dbt_toolbox.generate import staging
from tests.dbt_toolbox.generate.fixtures import jaffle_shop__orderlines


@pytest.mark.parametrize(
    "model, expected_file_name",
    [
        (jaffle_shop__orderlines.model, jaffle_shop__orderlines.file_name),
    ],
)
def test__model__file_name_includes_source_and_object(
    model: staging.Model,
    expected_file_name: str,
):
    assert model.file_name == expected_file_name


@pytest.mark.parametrize(
    "model, expected_sql",
    [
        (jaffle_shop__orderlines.model, jaffle_shop__orderlines.sql),
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
        (jaffle_shop__orderlines.model, jaffle_shop__orderlines.yaml),
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
