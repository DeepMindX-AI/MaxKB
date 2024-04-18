import yaml

# Load the YAML file
with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)  # Use `safe_load` to load YAML safely

print(data)
