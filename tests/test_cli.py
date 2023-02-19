from pdf_slicer.splitter import split

from diff_pdf_visually import pdf_similar


def _test(file_regression, shared_datadir, cut_list):
    files = split(
        shared_datadir / "4_pages.pdf",
        cut_list,
    )
    assert len(files) == len(cut_list) + 1
    for fn in files:
        assert fn.exists()
        file_regression.check(
            fn.read_bytes(), extension=".pdf", binary=True, check_fn=pdf_similar
        )


def test_slice_single(file_regression, shared_datadir):
    _test(file_regression, shared_datadir, [2])


def test_slice_multiple(file_regression, shared_datadir):
    _test(file_regression, shared_datadir, range(0, 3))
