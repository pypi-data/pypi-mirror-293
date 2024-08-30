import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

class LoadingPopup(QDialog):
    """
        A class handle Loading Popup. Informs the user of Load
    """

    def __init__(self, parent=None):
        """
        Creates popup with style sheet and disable close and help button.
        """
        super().__init__(parent)

        # Remove Help Button and Disable Close Windows
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        # Add Style to Qdialog
        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        with open(os.path.join(resourcedir, "Style_Application.qss"), 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

        # Set Title and Window Size
        self.setWindowTitle("Loading")
        self.setModal(True)
        self.setFixedSize(200, 100)

        # Add Label for the text
        layout = QVBoxLayout()
        self.label = QLabel("Loading...", self)
        self.label.setProperty("class", "loadingPopup")

        layout.addWidget(self.label)
        self.setLayout(layout)
        