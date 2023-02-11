import sys
from pprint import pprint

from PySide6.QtCore import QPoint
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMessageBox
from qtpy.QtPdf import QPdfDocument
from qtpy.QtPdfWidgets import QPdfView
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import (
    QMainWindow,
    QMenu,
    QAction,
    QFileDialog,
)

from pdf_cutter.splitter import split


class QPdfViewerMainwindow(QMainWindow):
    def __init__(self, pdf_filename=None):
        super().__init__()
        self.scaleFactor = 0.0

        self.document = QPdfDocument(self)
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

        self.cut_points = set()
        self.pdf_doc = QPdfDocument()
        self.pdf_doc.load(file_path)
        self.file_path = file_path

        self.images_clips = []
        self.view = QPdfView()
        self.view.setDocument(self.pdf_doc)
        self.view.setPageMode(QPdfView.SinglePage)
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
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def cut(self):
        if self.view.pageNavigator().currentPage() > 0:
            self.cut_points.add(self.view.pageNavigator().currentPage() - 1)
            print("cut points")
            pprint(self.cut_points)

    def previous(self):
        nav = self.view.pageNavigator()
        if nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())
            self.view.update()

    def next(self):
        nav = self.view.pageNavigator()
        if nav.currentPage() < self.pdf_doc.pageCount() - 1:
            nav.jump(nav.currentPage() + 1, QPoint(), nav.currentZoom())
            self.view.update()

    def process(self):
        text = f"Split into {len(self.cut_points)} files?"
        reply = QMessageBox.question(
            self,
            "Process file",
            text,
            buttons=QMessageBox.StandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ),
            defaultButton=QMessageBox.StandardButton.Yes,
        )
        if reply == QMessageBox.StandardButton.Yes:
            split(self.file_path, self.cut_points)

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
        self.cutAct = QShortcut(QKeySequence("x"), self, self.cut)
        self.nextAct = QShortcut(QKeySequence.fromString(" "), self, self.next)
        self.prevAct = QShortcut(QKeySequence("b"), self, self.previous)
        self.processAct = QShortcut(QKeySequence("p"), self, self.process)

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
        # self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        self.view.setZoomFactor(self.scaleFactor)

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
    imageViewer = QPdfViewerMainwindow(pdf_filename)
    imageViewer.show()
    sys.exit(app.exec_())
