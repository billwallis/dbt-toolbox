#!/usr/bin/env python
# TODO: Split the CLI part into `cli.py`

"""
Write a basic unit test template.

Once the unit test YAML can be successfully compiled, dbt stored the
compiled SQL at:

- target/compiled/<project-name>/<unit-test-path>.yml/<unit-test-path>.sql

We can then run this directly -- for example, using the Snowflake CLI:

- snow sql --format csv --enable-templating none --filename '<as-above>'
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
from collections.abc import Sequence
from typing import TypedDict

type ManifestNodes = dict[str, ModelNode]


class ModelNode(TypedDict):
    unique_id: str
    name: str
    relation_name: str
    depends_on: dict[str, list[str]]


@dataclasses.dataclass
class Model:
    unique_id: str
    name: str
    relation_name: str
    depends_on: dict[str, list[str]]

    def __str__(self) -> str:
        return f"Model({self.name})"

    @classmethod
    def from_node(cls, node: ModelNode) -> Model:
        return cls(
            unique_id=node.get("unique_id", ""),
            name=node.get("name", ""),
            relation_name=node.get("relation_name", ""),
            depends_on=node.get("depends_on", {}),
        )

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


def _read_manifest(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _get_models(
    manifest_nodes: ManifestNodes,
    model_names: list[str],
) -> dict[str, Model]:
    return {
        node_id: Model.from_node(node)
        for node_id, node in manifest_nodes.items()
        if node.get("name") in model_names
    }


def _get_model_dependencies(
    model: Model,
    manifest_nodes: ManifestNodes,
) -> list[Model]:
    return [
        Model.from_node(manifest_nodes[upstream_model_id])
        for upstream_model_id in model.depends_on.get("nodes", [])
        if upstream_model_id in manifest_nodes.keys()
    ]


def _make_unit_test(model: Model, manifest_nodes: ManifestNodes) -> dict:
    return {
        "unit_tests": [
            {
                "name": f"test__{model.name}",
                "model": model.name,
                "given": [
                    {
                        "input": f'ref("{dep.name}")',
                        "format": "csv",
                        "fixture": f"fixture__{dep.name}",
                    }
                    for dep in _get_model_dependencies(model, manifest_nodes)
                ],
                "expect": {
                    "format": "csv",
                    "fixture": f"fixture__{model.name}",
                },
            },
        ],
    }


def _parse_manifest_path(
    args: argparse.Namespace,
) -> tuple[int, pathlib.Path | None]:
    manifest_path = args.manifest_path or os.environ.get("MANIFEST_PATH")
    if manifest_path is None:
        return 1, None

    manifest_path = pathlib.Path(manifest_path).resolve()
    if not manifest_path.exists():
        return 2, manifest_path

    return 0, manifest_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_names", nargs="*")
    parser.add_argument("--manifest-path", required=False)
    args = parser.parse_args(argv)

    rc, manifest_path = _parse_manifest_path(args)
    if rc == 1:
        print(
            "error: specify the manifest path with the `--manifest-path`"
            " flag or the `MANIFEST_PATH` environment variable"
        )
        return rc
    elif rc == 2:  # noqa: PLR2004
        print(f"error: manifest does not exist at path '{manifest_path!s}'")
        return rc
    else:
        assert manifest_path is not None  # noqa: S101
        # print(f"debug: using manifest at path '{manifest_path}'")

    manifest = _read_manifest(manifest_path)
    manifest_nodes: ManifestNodes = manifest.get("nodes", {})
    models = _get_models(manifest_nodes, args.model_names)
    for model in models.values():
        print(json.dumps(_make_unit_test(model, manifest_nodes), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
