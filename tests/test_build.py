from pathlib import Path
from unittest import mock

import pytest

import mackerel


@pytest.yield_fixture
def build(site):
    yield mackerel.build.Build(site=site)


def test_build(site):
    test_build = mackerel.build.Build(site=site)
    assert test_build.site == site
    assert isinstance(test_build.context, mackerel.build.Context)


def test_build_pages(build, site):
    assert len(build.pages) == len(site.documents)

    for page in build.pages:
        assert page.path
        assert page.content

    assert site.template_renderer.render.call_count == len(site.documents)
    for document in site.documents:
        assert (mock.call(ctx=build.context, document=document) in
                site.template_renderer.render.call_args_list)


def test_build_absolute_page_output_path(build, document_mocks):
    document = document_mocks.create(relative_path=Path('document.md'))
    page_path = build._absolute_page_output_path(document)
    assert page_path == build.site.output_path / Path('document.html')


def test_build_execute_dry_run(build):
    build.touch = mock.Mock()
    assert build.execute(dry_run=True) is None
    assert build.touch.called is False


def test_build_execute(build):
    build.touch = mock.Mock()
    with mock.patch('shutil.rmtree') as rm_mock, \
            mock.patch.object(Path, 'write_text') as write_mock, \
            mock.patch('shutil.copyfile') as copy_mock:
        build.execute()

    assert rm_mock.called_with(build.site.output_path)
    assert build.touch.call_count == write_mock.call_count == len(build.pages)
    for page in build.pages:
        assert mock.call(page.path) in build.touch.call_args_list
        assert mock.call(page.content) in write_mock.call_args_list

    assert build.site.logger.info.called

    for file in build.site.other_content_files:
        dst = build._absolute_other_file_output_path(file)
        assert mock.call(src=file, dst=dst) in copy_mock.call_args_list

    for file in build.site.other_template_files:
        dst = build._absolute_template_file_output_path(file)
        assert mock.call(src=file, dst=dst) in copy_mock.call_args_list


@pytest.mark.parametrize('path', [
    'root.html',
    'foo/bar.html',
    'foo/bar/xyz.html',
])
def test_touch(build, tmpdir, path):
    tmp_dir = Path(str(tmpdir.mkdir('_helper_tests')))
    path = Path(tmp_dir, path)
    assert path.exists() is False
    build.touch(path)
    assert path.exists()


def test_build_context(build):
    # TODO: Test something more meaningful
    assert build.context.nav
    assert build.context.cfg


def test_context_url_for(build):
    assert build.context.url_for('css/style.css') == '/css/style.css'
    assert build.context.url_for('app.js') == '/app.js'
    assert build.context.url_for(
        'app.js', external=True) == 'http://localhost:8000/app.js'

    with mock.patch.dict(build.context.cfg,
                         {'user': {'url': 'http://test/blog/'}}):
        assert build.context.url_for('css/style.css') == '/blog/css/style.css'
        assert build.context.url_for('app.js') == '/blog/app.js'
