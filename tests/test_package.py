from __future__ import annotations

import packaging

import pdf_slicer as m


def test_version():
    assert m.__version__
    ver = packaging.version.parse(m.__version__)
    assert ver
