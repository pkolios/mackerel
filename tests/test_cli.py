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
    assert 'SITE_PATH' in result.output


def test_build_success(runner, site_path, template_path, output_path):
    output_path.mkdir()
    result = runner.invoke(cli.cli, ['build', str(site_path)], input='y\n')
    assert result.exit_code == 0
    assert result.output == (
        f'Directory {str(output_path)} already exists, '
        'do you want to overwrite? [y/N]: y\nBuild finished.\n')
    assert len(list(site_path.iterdir()))


def test_init_directory_exists(runner, site_path):
    result = runner.invoke(cli.cli, ['init', str(site_path)])
    assert result.exit_code == 2
    assert f'Initialize failed, file {str(site_path)}' in result.output


def test_init_directory_success(runner, tmpdir, site_path):
    test_dir = tmpdir.join('init_test')
    result = runner.invoke(cli.cli, ['init', str(test_dir)])
    assert result.exit_code == 0
    assert result.output == f'Initialized empty mackerel site in {test_dir}\n'
    assert len(list(site_path.iterdir())) == len(test_dir.listdir())
