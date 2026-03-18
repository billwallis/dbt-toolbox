from __future__ import annotations

import argparse
import collections
import csv
import importlib.metadata
import pathlib
from collections.abc import Sequence

from dbt_toolbox import generate, utils

SUCCESS = 0
FAILURE = 1


def _get_version() -> str:
    return f"%(prog)s {importlib.metadata.version('dbt-toolbox')}"


def _read_csv_as_json(filepath: pathlib.Path) -> list[dict]:
    reader = csv.reader(filepath.read_text().strip().split("\n"))
    headers = [h.lower() for h in next(reader)]
    return [
        {k: v for k, v in zip(headers, line, strict=True)} for line in reader
    ]


def _generate(args: argparse.Namespace) -> int:
    from_csv_path = pathlib.Path(args.from_csv_path).resolve()
    if not (from_csv_path.exists() and from_csv_path.is_file()):
        raise FileNotFoundError(f"File not found: {from_csv_path}")

    models_json = collections.defaultdict(list)
    for line in _read_csv_as_json(from_csv_path):
        models_json[line["table_name"]].append(
            {
                "column_name": line["column_name"],
                "data_type": line["data_type"],
                "ordinal_position": line["ordinal_position"],
            }
        )

    models = [
        generate.Model(
            source_name=args.source_name,
            model_name=model_name,
            columns=[
                generate.Column(
                    column_name=column["column_name"],
                    data_type=column["data_type"],
                    ordinal_position=column["ordinal_position"],
                )
                for column in columns
            ],
        )
        for model_name, columns in models_json.items()
    ]

    target_dir_path = pathlib.Path(args.target_dir_path).resolve()
    target_dir_path.mkdir(parents=True, exist_ok=True)
    (target_dir_path / "_sources.yml").write_text(
        utils.yaml_dumps(generate.generate_sources_yaml(models))
    )

    all_yamls = {"version": 2, "models": []}
    for model in models:
        model_root_path = target_dir_path / model.file_name
        model_root_path.with_suffix(".sql").write_text(
            generate.generate_staging_model_sql(model)
        )
        all_yamls["models"].append(generate.generate_staging_model_yaml(model))

    (target_dir_path / "_schema.yml").write_text(utils.yaml_dumps(all_yamls))

    return SUCCESS


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the command.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=_get_version(),
    )
    subparsers = parser.add_subparsers(dest="command")

    parser__foo = subparsers.add_parser("generate")
    parser__foo.add_argument("--from-csv-path", required=True)
    parser__foo.add_argument("--target-dir-path", required=True)
    parser__foo.add_argument("--source-name", required=True)

    args = parser.parse_args(argv)
    if args.command == "generate":
        return _generate(args)

    parser.print_help()
    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
