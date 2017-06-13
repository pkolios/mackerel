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
    output_path.mkdir()
    result = runner.invoke(cli.cli, ['build', str(source_path)], input='y\n')
    assert result.exit_code == 0
    assert result.output == (
        'Directory {o} already exists, '
        'do you want to overwrite? [y/N]: y\n'.format(o=str(output_path)))


def test_init_directory_exists(runner, source_path):
    result = runner.invoke(cli.cli, ['init', str(source_path)])
    assert result.exit_code == 2
    assert 'Directory {s} already exists.'.format(
        s=str(source_path)) in result.output


def test_init_directory_success(runner, tmpdir, source_path):
    test_dir = tmpdir.join('init_test')
    result = runner.invoke(cli.cli, ['init', str(test_dir)])
    assert result.exit_code == 0
    assert result.output == 'Initialized empty mackerel site in {}\n'.format(
        test_dir)
    assert len(list(source_path.iterdir())) == len(test_dir.listdir())
