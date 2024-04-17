import os
from typing import Dict, Set
from configparser import ConfigParser

configer_required_structure = {
    'database': {'host', 'user', 'password', 'database_name', 'port'},
    'redis': {'host', 'port', 'password'},
    'api': {'api_key', 'base_url'},
}


def validate_config(configer: ConfigParser, required_structure: Dict[str, Set[str]]):
    """
    Validates that the provided config has all required sections and keys.

    :param config: ConfigParser object
    :param required_structure: A dict where keys are section names and values are sets of required keys in that section.
    :raises ValueError: If a section or key is missing
    """
    for section, required_keys in required_structure.items():
        if section not in configer.sections():
            raise ValueError(f"Missing required section: {section}")
        available_keys = set(configer[section].keys())
        missing_keys = required_keys - available_keys
        if missing_keys:
            raise ValueError(f"Missing required keys in section {section}: {missing_keys}")


def init_configer() -> ConfigParser:
    configer = ConfigParser()

    # file exists
    if not os.path.exists('config.ini'):
        raise FileNotFoundError("The configuration file 'config.ini' does not exist.")

    # read config
    configer.read('config.ini')

    # validate config
    validate_config(configer, configer_required_structure)

    return configer


config = init_configer()
