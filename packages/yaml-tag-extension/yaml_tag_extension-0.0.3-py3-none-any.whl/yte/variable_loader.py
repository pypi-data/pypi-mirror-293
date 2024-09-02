import json
import os
from typing import Any

import yaml
from yaml import Loader


class VariableLoader(object):
    var_loader = {}

    def __init__(self):
        self._init_env_vars()

    def set_vars(self, var_files):
        self.variables = {
            **self.variables,
            **{
                var_file: yaml.load(
                    open(loc).read(),
                    yaml.SafeLoader
                )
                for var_file, loc in var_files.items()
            }
        }

    def _init_env_vars(self):
        self.variables = {
            'env': os.environ
        }

    def fetch(self, var):
        set_variables = self.variables
        for step in var[1:].split('.'):
            if step not in set_variables:
                raise ValueError(f'{var} setting not set')
            set_variables = set_variables[step]
        return set_variables


var_loader = VariableLoader()


def variable_constructor(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    if isinstance(node, yaml.SequenceNode):
        node = loader.construct_sequence(node)
        var_loader.set_vars(
            {settings_file.split('/')[-1].split('.')[0]: settings_file for settings_file in node}
        )
    elif isinstance(node, yaml.MappingNode):
        settings = loader.construct_mapping(node)
        var_loader.set_vars(**settings)
    else:
        raise ValueError(f"Unsupported block type detected - Cannot parse \n {node.value}.")

    return {
        "variables_loaded":
            {key: value for key, value in var_loader.variables.items() if key.lower() != 'env'}
    }


def read_variable_constructor(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    if isinstance(node, yaml.ScalarNode):
        return var_loader.fetch(loader.construct_scalar(node))
    else:
        raise ValueError(f"Unsupported block type detected - Cannot parse \n {node.value}.")
