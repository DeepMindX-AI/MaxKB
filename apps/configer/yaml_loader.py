import yaml
from yaml.loader import SafeLoader


def validate_config(config, required_structure):
    """
    Validates that the provided config has all required sections and keys.

    :param config: Dictionary representing the YAML loaded configuration
    :param required_structure: A dict where keys are section names and values are sets of required keys in that section.
    :raises ValueError: If a section or key is missing
    """
    # Check for required sections
    for section, keys in required_structure.items():
        if section not in config:
            raise ValueError(f"Missing required section: {section}")

        # Check for required keys in each section
        available_keys = set(config[section].keys())
        missing_keys = keys - available_keys
        if missing_keys:
            raise ValueError(f"Missing keys in '{section}': {', '.join(missing_keys)}")


# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Define required structure of the config file
required_structure = {
    'database': {'host', 'user', 'password', 'database_name', 'port'},
    'redis': {'host', 'port', 'password'},
    'mail': {'smtp_server', 'smtp_port', 'smtp_user', 'smtp_password'}
}

# Validate the configuration
validate_config(config, required_structure)
