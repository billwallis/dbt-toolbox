import io

import ruamel.yaml

YAML = ruamel.yaml.YAML()
YAML.default_flow_style = False
YAML.indent(mapping=2, sequence=4, offset=2)


def yaml_dumps(doc: dict) -> str:
    # TODO: Consider switching to:
    #           https://yaml.dev/doc/ruamel.yaml/example/#Output_of_%60dump()%60_as_a_string
    #       ...or only write to a YAML file once all models are collected (and write direct to file)
    with io.StringIO() as buffer:
        YAML.dump(doc, buffer)
        return buffer.getvalue()
