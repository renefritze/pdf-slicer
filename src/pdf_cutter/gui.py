import sys
from pathlib import Path

import fitz
from PIL import Image, ImageQt
from qtpy.QtPdf import QPdfDocument, QPdfBookmarkModel
from qtpy.QtPdfWidgets import QPdfView
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap, QPalette, QPainter
from qtpy.QtPrintSupport import QPrintDialog, QPrinter
from qtpy.QtWidgets import (
    QLabel,
    QSizePolicy,
    QScrollArea,
    QMessageBox,
    QMainWindow,
    QMenu,
    QAction,
    QFileDialog,
)


class QImageViewer(QMainWindow):
    def __init__(self, pdf_filename=None):
        super().__init__()
        self.scaleFactor = 0.0

        self.document = QPdfDocument(self)
        # bookmark_model = QPdfBookmarkModel(self)
        # bookmark_model.setDocument(self.document)
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

        if pdf_filename:
            self.preload_images(pdf_filename)

    def open(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "PDF (*.pdf )", options=options
        )
        if fileName:
            self.preload_images(fileName)

    def preload_images(self, file_path):

        self.pdf_doc = QPdfDocument()
        self.pdf_doc.load(file_path)
        # self.pdf_doc.setPageSize(QPrinter.A4)
        # self.pdf_doc.setPageOrientation(QPrinter.Portrait)
        # self.pdf_doc.render(0, (self.pdf_doc.pageSize().width(), self.pdf_doc.pageSize().height()))

        self.images_clips = []
        self.view = QPdfView()
        self.view.setDocument(self.pdf_doc)
        self.view.setPageMode(QPdfView.SinglePage)
        # self.view.setPageLayout(QPdfView.OneColumn)
        # self.view.setPageNavigation(QPdfView.ScrollBarNavigation)
        self.view.show()
        self.setCentralWidget(self.view)

        self.setWindowTitle("Image Viewer : " + file_path)
        self.scaleFactor = 1.0

        self.fitToWidthAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        self.scaleImage(1.0)

    def fitToWidth(self):
        if self.scrollArea.width() > 0 and self.imageLabel.pixmap().width() > 0:
            zoomfactor = self.scrollArea.width() / self.imageLabel.pixmap().width()
        else:
            zoomfactor = 1

        self.imageLabel.adjustSize()
        self.scaleFactor = zoomfactor
        self.scaleImage(1.0)

        self.updateActions()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction(
            "Zoom &In (25%)",
            self,
            shortcut="Ctrl++",
            enabled=False,
            triggered=self.zoomIn,
        )
        self.zoomOutAct = QAction(
            "Zoom &Out (25%)",
            self,
            shortcut="Ctrl+-",
            enabled=False,
            triggered=self.zoomOut,
        )
        self.normalSizeAct = QAction(
            "&Normal Size",
            self,
            shortcut="Ctrl+S",
            enabled=False,
            triggered=self.normalSize,
        )
        self.fitToWidthAct = QAction(
            "&Fit to Width",
            self,
            shortcut="Ctrl+S",
            enabled=False,
            triggered=self.fitToWidth,
        )
        self.fitToWindowAct = QAction(
            "&Fit to Window",
            self,
            enabled=False,
            checkable=True,
            shortcut="Ctrl+F",
            triggered=self.fitToWindow,
        )

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addAction(self.fitToWidthAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.fitToWidthAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(
            int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep() / 2))
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        pdf_filename = sys.argv[1]
    except IndexError:
        pdf_filename = None
    imageViewer = QImageViewer(pdf_filename)
    imageViewer.show()
    sys.exit(app.exec_())
