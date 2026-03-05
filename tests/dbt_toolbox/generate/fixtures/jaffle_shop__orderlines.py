import textwrap

from dbt_toolbox.generate import staging

file_name = "stg_jaffle_shop__order_lines"

model = staging.Model(
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
)

sql = textwrap.dedent(
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
)

# textwrap.dedent(
#     """\
#     name: stg_jaffle_shop__order_lines
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
yaml = {
    "name": "stg_jaffle_shop__order_lines",
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
}
