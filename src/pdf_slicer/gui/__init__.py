import typer

from pdf_slicer.gui.window import run


def main():
    """Entry point for the application script."""
    return typer.run(run)


if __name__ == "__main__":
    typer.run(run)
