import json
from typing import Any

import yaml
from jinja2 import Template
from yaml import Loader


class Jinja2Loader(object):
    def __init__(self, path, params, **kwargs):
        self.path = path
        self.params = params
        self.kwargs = kwargs

    def render(self):
        with open(self.path) as f:
            template = Template(f.read()).render(self.params)
        return {
            **yaml.load(template, Loader=yaml.SafeLoader),
            **self.kwargs
        }


def construct_template(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    if isinstance(node, yaml.SequenceNode):
        node = loader.construct_sequence(node)
        path = node[0]
        params = json.loads(node[1])
        template = Jinja2Loader(path=path, params=params)
    elif isinstance(node, yaml.MappingNode):
        settings = loader.construct_mapping(node, deep=True)
        template = Jinja2Loader(**settings)
    else:
        raise ValueError(f"Unsupported block type detected - Cannot parse \n {node.value}.")

    return template.render()
