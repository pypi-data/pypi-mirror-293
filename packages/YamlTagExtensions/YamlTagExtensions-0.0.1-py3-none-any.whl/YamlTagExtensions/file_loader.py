import json
from typing import Any

import yaml
from yaml import Loader
from smart_open import open as sopen


class FileLoader(object):
    def __init__(self, path):
        self.path = path

    def fetch(self):
        with sopen(self.path) as f:
            content = f.read()
        return content


def construct_file_read(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    if isinstance(node, yaml.SequenceNode):
        node = loader.construct_sequence(node)
        raw_file = FileLoader(path=node[0]).fetch()
    elif isinstance(node, yaml.MappingNode):
        settings = loader.construct_mapping(node)
        raw_file = FileLoader(**settings).fetch()
    else:
        raise ValueError(f"Unsupported block type detected - Cannot parse \n {node.value}.")

    return raw_file
