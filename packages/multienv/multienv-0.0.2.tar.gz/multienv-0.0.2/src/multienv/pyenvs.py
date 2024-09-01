"""
pyenvs command entrypoint
"""
import logging
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

import yaml

LOG = logging.getLogger(__name__)

@dataclass(frozen=True)
class Dependency:
    """Representation of dependency features."""

    id: str
    version: str | None
    environments: list[str] | None
    source: str | None
    sha: str | None

    @staticmethod
    def from_dict(source: dict):
        """Builds a Dependency from a configuration dict."""

        return Dependency(
            id=source['id'],
            version=str(source['version']) if 'version' in source else None,
            environments=source['environments'] if 'environments' in source else None,
            source=source['source'] if 'source' in source else None,
            sha=source['sha'] if 'sha' in source else None
        )

@dataclass(frozen=True)
class Configuration:
    """Representation of pyenvs configuration content."""

    formatters: list[dict, str]
    """Each formatter either can be a single character string of one of supported formatters or a key/value pair with 
    the key referencing to the formatter name and the value referencing to its specific configuration."""

    environments: list[str] | None
    """A reference list of the environments referenced by dependencies. If the list is provided, dependencies 
    referencing an unknown environment raise an error. If the list is not provided, it is inferred from the dependency
    environments. If an empty list is provided, no dependency is supposed to reference any specific environment."""

    dependencies: list[Dependency]
    """The list of the dependencies."""

    @staticmethod
    def from_dict(source: dict):
        """Builds a Configuration from a configuration dict."""
        return Configuration(
            formatters=source['configuration']['formatters'],
            environments=source['environments'] if 'environments' in source else None,
            dependencies=[Dependency.from_dict(d) for d in source['dependencies']]
        )

@dataclass(frozen=True)
class CondaConfiguration:
    """The specific conda configuration model."""

    default_environment: bool
    prefix: str
    encoding: str

    @staticmethod
    def from_configuration(formatter: dict | str):
        """Builds a conda configuration object form a dict or a default one form a string"""
        if isinstance(formatter, str):
            return _DEFAULT_CONDA_CONFIGURATION

        return CondaConfiguration(
            default_environment=formatter['default_environment'] if 'default_environment' in formatter
            else _DEFAULT_CONDA_CONFIGURATION.default_environment,
            prefix=formatter['prefix'] if 'prefix' in formatter else _DEFAULT_CONDA_CONFIGURATION.prefix,
            encoding=formatter['encoding'] if 'encoding' in formatter else _DEFAULT_CONDA_CONFIGURATION.encoding
        )

_DEFAULT_CONDA_CONFIGURATION = CondaConfiguration(
    default_environment=True,
    prefix='environment',
    encoding='utf-8'
)

def _info(ns: Namespace):
    """info
    """
    LOG.info("info")
    print("print info")
    print(ns)


def _conda_dep_formatter(d: Dependency) -> str:
    """Formats a dependency to a conda dependency string."""
    result : str = d.id
    if d.version is not None:
        result += '=' + d.version
        if d.sha is not None:
            result += d.sha
    return result


def conda_writer(configuration: Configuration):
    """Writes a configuration as conda configuration environment files."""

    formatter_configuration: CondaConfiguration = Formatters.CONDA.get_formatter_configuration(configuration)

    # default environment includes all dependencies
    if formatter_configuration.default_environment:

        output = {
            'name': 'default',
            'dependencies': [_conda_dep_formatter(d) for d in configuration.dependencies]
        }
        with open(f'{formatter_configuration.prefix}_.yml', "w", encoding=formatter_configuration.encoding) as o:
            yaml.dump(output, o, sort_keys=False)

    if configuration.environments is None:
        return

    for e in configuration.environments:

        output = {
            'name': e,
            'dependencies': [_conda_dep_formatter(d) for d in configuration.dependencies
                             if d.environments is None or e in d.environments]
        }
        with open(f'{formatter_configuration.prefix}_{e}.yml', "w", encoding=formatter_configuration.encoding) as o:
            yaml.dump(output, o, sort_keys=False)

@dataclass
class _FormatterValue[C]:
    name: str
    write: Callable[[Configuration], None]
    configuration: Callable[[dict | str], C]


class Formatters(Enum):
    """The enumeration of the supported formatters."""
    CONDA = _FormatterValue[CondaConfiguration](name='conda',
                                                write=conda_writer,
                                                configuration=CondaConfiguration.from_configuration)

    def test(self, formatter: dict | str) -> bool:
        """Checks if a formatter configuration dict refers to the current Formatter value."""
        return (isinstance(formatter, str) and self.value.name == formatter
                or isinstance(formatter, dict) and self.value.name in formatter)

    def get_formatter_configuration(self, configuration: Configuration):
        """Builds a specific formatter configuration from the main configuration related to the current Formatter value.
        """
        for formatter in configuration.formatters:
            if self.test(formatter):
                return self.value.configuration(formatter)
        raise ValueError


def _config(ns: Namespace):
    """config
    """
    LOG.info("config")

    extension = ns.file.split('.')[-1]

    if extension in ['yml']:
        with open(ns.file, encoding=ns.encoding) as s:
            content = yaml.safe_load(s)
            print(content)
            configuration = Configuration.from_dict(content)

            for req_formatter in configuration.formatters:
                for supported_formatter in Formatters:
                    if supported_formatter.test(req_formatter):
                        supported_formatter.value.write(configuration)


    else:
        raise ValueError(f'unsupported configuration format {extension}')

    print("print config")
    print(ns)


def _config_parser() -> ArgumentParser:

    # parse argument line
    parser = ArgumentParser(description='Multi environment management.')

    subparsers = parser.add_subparsers(dest='CMD', help='available commands')

    subparsers.add_parser('info', help='get general info')

    parser_config = subparsers.add_parser('config', help='generates environment configurations')
    parser_config.add_argument('file',
                               nargs='?',
                               help="path to the configuration file",
                               default="multienv.yml")
    parser_config.add_argument('--encoding',
                               nargs='?',
                               help='the configuration file encoding (default to utf-8)',
                               default='utf-8')

    return parser


def entrypoint():
    """The pyenvs command entrypoint."""

    commands = {
        'info': _info,
        'config': _config
    }

    ns: Namespace = _config_parser().parse_args()

    commands[ns.CMD](ns)
