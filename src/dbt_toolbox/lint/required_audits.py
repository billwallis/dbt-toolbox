#!/usr/bin/env python
# TODO: Split the CLI part into `cli.py`

"""
Validate that a given model has the required audits.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
from collections.abc import Sequence
from typing import Literal, TypedDict

RESOURCE_TYPE_MODEL: Literal["model"] = "model"
RESOURCE_TYPE_TEST: Literal["test"] = "test"
NO_MANIFEST_PROVIDED = 1
MANIFEST_NOT_EXISTS = 2


type ManifestNodes = dict[str, ModelNode | TestNode]


class ModelNode(TypedDict):
    unique_id: str
    name: str
    resource_type: Literal["model"]
    depends_on: dict[str, list[str]]


class TestNode(TypedDict):
    unique_id: str
    name: str
    resource_type: Literal["test"]
    file_key_name: str
    test_metadata: dict


@dataclasses.dataclass
class JSONable:
    def asdict(self) -> dict:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Model(JSONable):
    unique_id: str
    name: str
    depends_on: dict[str, list[str]]

    def __str__(self) -> str:
        return f"Model({self.name})"

    @classmethod
    def from_node(cls, node: ModelNode) -> Model:
        return cls(
            unique_id=node.get("unique_id", ""),
            name=node.get("name", ""),
            depends_on=node.get("depends_on", {}),
        )


@dataclasses.dataclass
class ModelTest(JSONable):
    unique_id: str
    name: str
    file_key_name: str
    test_metadata: dict

    def __str__(self) -> str:
        return f"Test({self.name})"

    @classmethod
    def from_node(cls, node: TestNode) -> ModelTest:
        return cls(
            unique_id=node.get("unique_id", ""),
            name=node.get("name", ""),
            file_key_name=node.get("file_key_name", ""),
            test_metadata=node.get("test_metadata", {}),
        )


def _read_manifest(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _get_models(
    manifest_nodes: ManifestNodes,
    model_names: list[str],
) -> dict[str, Model]:
    return {
        node_id: Model.from_node(node)  # type: ignore  # TODO: How to type narrow here?
        for node_id, node in manifest_nodes.items()
        if node.get("name") in model_names
        and node.get("resource_type") == RESOURCE_TYPE_MODEL
    }


def _get_model_tests(
    model: Model,
    manifest_nodes: ManifestNodes,
) -> list[ModelTest]:
    return [
        ModelTest.from_node(node)  # type: ignore  # TODO: How to type narrow here?
        for node in manifest_nodes.values()
        if node.get("file_key_name") == f"models.{model.name}"
        and node.get("resource_type") == RESOURCE_TYPE_TEST
    ]


def _parse_manifest_path(
    args: argparse.Namespace,
) -> tuple[int, pathlib.Path | None]:
    manifest_path = args.manifest_path or os.environ.get("MANIFEST_PATH")
    if manifest_path is None:
        return NO_MANIFEST_PROVIDED, None

    manifest_path = pathlib.Path(manifest_path).resolve()
    if not manifest_path.exists():
        return MANIFEST_NOT_EXISTS, manifest_path

    return 0, manifest_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_names", nargs="*")
    parser.add_argument("--manifest-path", required=False)
    args = parser.parse_args(argv)

    rc, manifest_path = _parse_manifest_path(args)
    if rc == NO_MANIFEST_PROVIDED:
        print(
            "error: specify the manifest path with the `--manifest-path`"
            " flag or the `MANIFEST_PATH` environment variable"
        )
        return rc
    elif rc == MANIFEST_NOT_EXISTS:
        print(f"error: manifest does not exist at path '{manifest_path!s}'")
        return rc
    else:
        assert manifest_path is not None  # noqa: S101
        # print(f"debug: using manifest at path '{manifest_path}'")

    manifest = _read_manifest(manifest_path)
    manifest_nodes: ManifestNodes = manifest.get("nodes", {})
    models = _get_models(manifest_nodes, args.model_names)
    for model in models.values():
        # print(json.dumps(manifest_nodes[model.unique_id], indent=2))
        # print(json.dumps(_make_unit_test(model, manifest_nodes), indent=2))
        # print(model)
        for model_test in _get_model_tests(model, manifest_nodes):
            print(model_test)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
