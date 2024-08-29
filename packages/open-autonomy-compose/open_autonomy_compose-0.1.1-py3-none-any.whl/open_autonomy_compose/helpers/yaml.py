# pylint: disable=import-error, too-few-public-methods
"""YAML helpers."""

from collections import OrderedDict
from typing import Any, Dict, List, Optional, Sequence, TextIO

import yaml  # type: ignore[import]
from yaml import MappingNode  # type: ignore[import]


class YamlLoader(yaml.SafeLoader):
    """
    Custom yaml.SafeLoader for the AEA framework.

    It extends the default SafeLoader in two ways:
    - loads YAML configurations while *remembering the order of the fields*;
    - resolves the environment variables at loading time.

    This class is for internal usage only; please use
    the public functions of the module 'yaml_load' and 'yaml_load_all'.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the AEAYamlLoader.

        It adds a YAML Loader constructor to use 'OderedDict' to load the files.

        :param args: the positional arguments.
        :param kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)
        YamlLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, self._construct_mapping
        )

    @staticmethod
    def _construct_mapping(loader: "YamlLoader", node: MappingNode) -> OrderedDict:
        """Construct a YAML mapping with OrderedDict."""
        object_pairs_hook = OrderedDict
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))


class YamlDumper(yaml.SafeDumper):
    """
    Custom yaml.SafeDumper for the AEA framework.

    It extends the default SafeDumper so to dump
    YAML configurations while *following the order of the fields*.

    This class is for internal usage only; please use
    the public functions of the module 'yaml_dump' and 'yaml_dump_all'.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the AEAYamlDumper.

        It adds a YAML Dumper representer to use 'OderedDict' to dump the files.

        :param args: the positional arguments.
        :param kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)
        YamlDumper.add_representer(OrderedDict, self._dict_representer)

    @staticmethod
    def _dict_representer(dumper: "YamlDumper", data: OrderedDict) -> MappingNode:
        """Use a custom representer."""
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items()
        )


class Yaml:
    """YAML helpers."""

    @staticmethod
    def load(stream: TextIO) -> Dict[str, Any]:
        """
        Load a yaml from a file pointer in an ordered way.

        :param stream: file pointer to the input file.
        :return: the dictionary object with the YAML file content.
        """
        result = yaml.load(stream, Loader=YamlLoader)  # nosec
        return result if result is not None else {}

    @staticmethod
    def load_all(stream: TextIO) -> List[Dict[str, Any]]:
        """
        Load a multi-paged yaml from a file pointer in an ordered way.

        :param stream: file pointer to the input file.
        :return: the list of dictionary objects with the (multi-paged) YAML file content.
        """
        return list(yaml.load_all(stream, Loader=YamlLoader))  # nosec

    @staticmethod
    def dump(data: Dict, stream: Optional[TextIO] = None) -> None:
        """
        Dump YAML data to a yaml file in an ordered way.

        :param data: the data to write.
        :param stream: (optional) the file to write on.
        """
        yaml.dump(data, stream=stream, Dumper=YamlDumper)  # nosec

    @staticmethod
    def dump_all(data: Sequence[Dict], stream: Optional[TextIO] = None) -> None:
        """
        Dump YAML data to a yaml file in an ordered way.

        :param data: the data to write.
        :param stream: (optional) the file to write on.
        """
        yaml.dump_all(data, stream=stream, Dumper=YamlDumper)  # nosec
