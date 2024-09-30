from typer.testing import CliRunner
from pysinker.__main__ import app

runner = CliRunner()

def test_dump():
    result = runner.invoke(app, ["dump", "--config", "tests/data/config.yaml"])
    assert result.exit_code == 0   
    print("result ..... ", result.stdout)
    
