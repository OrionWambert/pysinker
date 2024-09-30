
import yaml

import pytest
from pathlib import Path

from pysinker.core.yaml_parser import parse_yaml_file


def test_yaml_parser_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_yaml_file("non_existent_file.yaml")

def test_yaml_parser_invalid_yaml():
    invalid_yaml_path = Path(__file__).parent / "data" / "invalid_config.yaml"
    invalid_yaml_path.write_text("invalid: yaml: content")
    with pytest.raises(yaml.YAMLError):
        parse_yaml_file(str(invalid_yaml_path))
    invalid_yaml_path.unlink()

def test_yaml_parser_structure():
    result = parse_yaml_file("tests/data/config.yaml")
    assert "source" in result, "Parsed result should contain 'source' key"
    assert isinstance(result["source"], list), "'source' should be a list"
    assert len(result["source"]) > 0, "'source' list should not be empty"
    
    assert "target" in result, "Parsed result should contain 'target' key"
    assert isinstance(result["target"], dict), "'target' should be a dictionary"
    assert "s3" in result["target"], "'target' should contain 's3' key"
    
    assert "action" in result, "Parsed result should contain 'action' key"
    assert "notification" in result["action"], "'action' should contain 'notification' key"
    assert "email" in result["action"]["notification"], "'notification' should contain 'email' key"

def test_yaml_parser():
    result = parse_yaml_file("tests/data/config.yaml")
    assert isinstance(result, dict), "Parsed result should be a dictionary"
    assert "version" in result, "Parsed result should contain 'version' key"
    assert result["version"] == "1.0.0"
