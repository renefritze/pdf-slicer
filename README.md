# pdf-slicer

[![Actions Status][actions-badge]][actions-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/renefritze/pdf-slicer/main.svg)](https://results.pre-commit.ci/latest/github/renefritze/pdf-slicer/main)


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/renefritze/pdf-slicer/workflows/CI/badge.svg
[actions-link]:             https://github.com/renefritze/pdf-slicer/actions
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/renefritze/pdf-slicer/discussions
[pypi-link]:                https://pypi.org/project/pdf-slicer/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/pdf-slicer
[pypi-version]:             https://img.shields.io/pypi/v/pdf-slicer
[rtd-badge]:                https://readthedocs.org/projects/pdf-slicer/badge/?version=latest
[rtd-link]:                 https://pdf-slicer.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->

## Usage

```bash
pdf-slicer <pdf-file>
```

## Installation


```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
python3 -m pipx install pdf-slicer
```

### Keys

| Key | Action                           |
| --- |----------------------------------|
| `x` | Slice before this page           |
| `p` | process slice list and save pdfs |
| `Space` | Next page                        |
