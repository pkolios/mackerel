from unittest import mock

import pytest

from mackerel.renderers import base


def test_document_renderer():
    with pytest.raises(NotImplementedError):
        base.DocumentRenderer(site=mock.Mock())

    dr = base.DocumentRenderer
    for func in (dr.extract_metadata, dr.render):
        with pytest.raises(NotImplementedError):
            func(self=0, text='')


def test_template_renderer():
    with pytest.raises(NotImplementedError):
        base.TemplateRenderer(site=mock.Mock())

    with pytest.raises(NotImplementedError):
        base.TemplateRenderer.render(self=0, ctx='', document='')
