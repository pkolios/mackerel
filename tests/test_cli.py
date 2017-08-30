from pathlib import Path
from unittest import mock
import shutil

import pytest
from click.testing import CliRunner

import mackerel


@pytest.fixture
def runner():
    return CliRunner()


@pytest.yield_fixture
def template_path():
    yield Path(__file__).parent / 'site' / 'template'


@pytest.yield_fixture
def output_path(site_path):
    path = Path(__file__).parent / 'site' / '_build'
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    yield path
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def test_cli_base(runner):
    result = runner.invoke(mackerel.cli.cli, ['--help'])
    assert result.exit_code == 0
    assert 'build' in result.output


def test_cli_build_error(runner):
    result = runner.invoke(mackerel.cli.cli, ['build'])
    assert result.exit_code == 2
    assert 'SITE_PATH' in result.output


def test_build_success(runner, site_path, template_path, output_path):
    output_path.mkdir()
    result = runner.invoke(
        mackerel.cli.cli, ['build', str(site_path)], input='y\n')
    assert result.exit_code == 0
    assert (f'Directory {str(output_path)} already exists, '
            'do you want to overwrite? [y/N]: y') in result.output
    assert '\nBuild finished.\n' in result.output
    assert len(list(site_path.iterdir()))


def test_init_directory_exists(runner, site_path):
    result = runner.invoke(
        mackerel.cli.cli, ['init', str(site_path)])
    assert result.exit_code == 2
    assert f'Initialize failed, file {str(site_path)}' in result.output


def test_init_directory_success(runner, tmpdir, site_path):
    test_dir = tmpdir.join('init_test')
    result = runner.invoke(mackerel.cli.cli, ['init', str(test_dir)])
    assert result.exit_code == 0
    assert result.output == f'Initialized empty mackerel site in {test_dir}\n'
    assert len(list(site_path.iterdir())) == len(test_dir.listdir())


def test_develop(runner, site):
    with mock.patch('mackerel.cli.Server') as server, mock.patch(
            'mackerel.cli.mackerel.build.Build') as build:
        runner.invoke(
            mackerel.cli.cli,
            ['develop', str(site.path), '-h 0.0.0.0', '-p 8080'])

    server.assert_called_with()
    watch_calls = (mock.call(str(site.template_path), mock.ANY),
                   mock.call(str(site.content_path), mock.ANY))
    server().watch.assert_has_calls(watch_calls, any_order=True)
    server().serve.assert_called_with(
        host='0.0.0.0', port=8080, root=str(site.output_path))

    assert build.called
    build().execute.assert_called_with()
