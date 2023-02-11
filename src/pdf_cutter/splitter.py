from pathlib import Path

import fitz


def split(pdf_file, cut_points):
    """Split a PDF file into multiple files.

    :param pdf_file: The PDF file to split.
    :param pages: A list of page numbers to split the PDF file on.
    """

    pdf_file = Path(pdf_file)
    # Create a new PDF file for each page number in the list.
    last_cut = 0
    for page in cut_points:
        _save(last_cut, pdf_file, page)
        last_cut = page + 1
    _save(last_cut, pdf_file)


def _save(last_cut, pdf_file, page=None):
    doc = fitz.open(pdf_file)
    if page is None:
        page = doc.page_count - 1
    if page > doc.page_count - 1:
        return
    # Open the PDF file to split.
    pages = list(range(last_cut, page + 1))
    doc.select(pages)
    output_file = pdf_file.with_name(f"{pdf_file.stem}_{page}.pdf")
    doc.save(output_file)
    doc.close()
