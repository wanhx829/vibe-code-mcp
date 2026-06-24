import os
import yaml


DEFAULTS = {
    "default_language": "zh",
    "server": {"name": "vibe-coding", "version": "1.0.0"},
    "scan": {
        "include_prompt_docs": True,
        "max_summary_length": 500,
        "languages": ["zh", "en"],
    },
}


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config or "resource_path" not in config:
        raise ValueError("config.yaml must contain 'resource_path'")

    resource_path = config["resource_path"]
    # Handle relative paths - resolve relative to config file location
    if not os.path.isabs(resource_path):
        config_dir = os.path.dirname(os.path.abspath(config_path))
        resource_path = os.path.join(config_dir, resource_path)

    if not os.path.isdir(resource_path):
        raise FileNotFoundError(f"resource_path does not exist: {resource_path}")

    config["resource_path"] = resource_path

    for key, value in DEFAULTS.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_key not in config[key]:
                    config[key][sub_key] = sub_value

    return config
