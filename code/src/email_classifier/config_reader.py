import yaml
import os


def load_model_config(config_path: str):
    """
    Loads model configuration from a YAML file.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: Configuration parameters for the models.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def load_categories_config(config_path: str = "src/email_classifier/config/categories_config.yaml"):
    """
    Loads categories and subcategories from a YAML configuration file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        tuple: A tuple containing categories (list) and subcategories (dict).
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config["categories"], config["subcategories"]
