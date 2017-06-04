import pytest
from click.testing import CliRunner

from mackerel import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_base(runner):
    result = runner.invoke(cli.cli, ['--help'])
    assert result.exit_code == 0
    assert 'build' in result.output


def test_cli_build_error(runner):
    result = runner.invoke(cli.cli, ['build'])
    assert result.exit_code == 2
    assert 'SOURCE_PATH' in result.output


def test_build_success(runner, source_path, template_path, output_path):
    result = runner.invoke(cli.cli, ['build', str(source_path)])
    assert result.exit_code == 0
