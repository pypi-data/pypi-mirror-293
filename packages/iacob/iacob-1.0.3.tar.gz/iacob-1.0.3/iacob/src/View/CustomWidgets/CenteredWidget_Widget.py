from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QGridLayout, QWidget


class CenteredWidget(QWidget):
    """
    A QWidget subclass that centers a child widget within itself, with dynamic resizing.
    """
    def __init__(self, child, parent=None):
        """
        Initializes the CenteredWidget instance.

        Parameters
        ----------
        child : QWidget
            The child widget to be centered.
        parent : QWidget, optional
            The parent widget of this widget. Default is None.

        Raises
        ------
        ValueError
            If the provided `child` is not an instance of `QWidget`.
        """

        super().__init__(parent=parent)

        self.setContentsMargins(0, 0, 0, 0)

        self.child = child
        self.child.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.child.setMinimumSize(10, 10)

        # Créer un layout vertical
        self.layout = QGridLayout(self)
        # Ajouter le widget au layout, centré

        self.spacerTop = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacerBottom = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacerLeft = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacerRight = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addItem(self.spacerTop, 0, 1)
        self.layout.addItem(self.spacerLeft, 1, 0)
        self.layout.addWidget(child, 1, 1)
        self.layout.addItem(self.spacerRight, 1, 2)
        self.layout.addItem(self.spacerBottom, 2, 1)

        self.needs_invalidation = False

    def resizeEvent(self, e):
        """
        Handles the resize event to adjust the size and position of the child widget and spacers.

        Parameters
        ----------
        e : QResizeEvent
            The resize event containing the new size of the widget.

        Notes
        -----
        This method dynamically adjusts the size of the child widget and the spacer items to ensure
        the child widget remains centered within the available space.
        """
        
        margin = 18
        width = e.size().width()
        height = e.size().height()
        size = min(width, height) - margin

        self.child.resize(size, size)

        verticalSize = max((height - size - margin) // 2, 0)
        horizontalSize = max((width - size - margin) // 2, 0)

        self.spacerTop.changeSize(0, verticalSize)
        self.spacerBottom.changeSize(0, verticalSize)
        self.spacerLeft.changeSize(horizontalSize, 0)
        self.spacerRight.changeSize(horizontalSize, 0)

        self.layout.invalidate()

