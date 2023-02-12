from pathlib import Path
from typing import Union, Optional

import fitz


def split(pdf_file: Union[str, Path], cut_points: list[int]) -> list[Path]:
    """Split a PDF file into multiple files.

    :param pdf_file: The PDF file to split.
    :param pages: A list of page numbers to split the PDF file on.
    """

    pdf_file = Path(pdf_file)
    # Create a new PDF file for each page number in the list.
    last_cut = 0
    outs = []
    for page in cut_points:
        outs.append(_save(last_cut, pdf_file, page))
        last_cut = page + 1
    outs.append(_save(last_cut, pdf_file))
    return [out for out in outs if out is not None]


def _save(
    last_cut: int, pdf_file: Path, page: Optional[int] = None
) -> Union[Path, None]:
    doc = fitz.open(pdf_file)
    if page is None:
        page = doc.page_count - 1
    if page > doc.page_count - 1:
        return None
    # Open the PDF file to split.
    pages = list(range(last_cut, page + 1))
    doc.select(pages)
    output_file = pdf_file.with_name(f"{pdf_file.stem}_{page}.pdf")
    doc.save(output_file)
    doc.close()
    return output_file
