import os
import pytest
import yaml
from resources.config import load_config


def test_load_config_reads_yaml(tmp_path):
    config_data = {
        "resource_path": str(tmp_path),
        "default_language": "zh",
        "server": {"name": "test", "version": "0.1.0"},
        "scan": {
            "include_prompt_docs": False,
            "max_summary_length": 300,
            "languages": ["zh"],
        },
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data, allow_unicode=True), encoding="utf-8")

    config = load_config(str(config_file))
    assert config["resource_path"] == str(tmp_path)
    assert config["default_language"] == "zh"
    assert config["server"]["name"] == "test"
    assert config["scan"]["languages"] == ["zh"]


def test_load_config_validates_resource_path(tmp_path):
    config_data = {"resource_path": "/nonexistent/path/that/does/not/exist"}
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data), encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        load_config(str(config_file))


def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")


def test_load_config_default_values(tmp_path):
    config_data = {"resource_path": str(tmp_path)}
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data), encoding="utf-8")

    config = load_config(str(config_file))
    assert config["default_language"] == "zh"
    assert config["server"]["name"] == "vibe-coding"
    assert config["server"]["version"] == "1.0.0"
    assert config["scan"]["include_prompt_docs"] is True
    assert config["scan"]["max_summary_length"] == 500
    assert config["scan"]["languages"] == ["zh", "en"]
