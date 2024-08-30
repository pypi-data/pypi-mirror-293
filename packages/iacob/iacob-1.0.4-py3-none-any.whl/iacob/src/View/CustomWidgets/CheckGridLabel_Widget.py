from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QVBoxLayout


class CheckGridLabel_Widget(QWidget):
    """
    A custom QWidget that displays a label with a specified name and color, and allows for rotation.
    """

    name : str
    clicked = pyqtSignal(str)
    orientation : str
    checked : bool = True

    def __init__(self, name, orientation, color, rotation=0):
        """
        Initializes the CheckGridLabel_Widget instance.

        Parameters
        ----------
        name : str
            The name to be displayed on the label.
        orientation : str
            The orientation of the label.
        color : tuple of float
            The RGB color values of the label in the range [0, 1].
        rotation : int, optional
            The rotation angle of the label in degrees. Default is 0.

        Raises
        ------
        ValueError
            If the color parameter does not have exactly three elements.
        """

        super().__init__()

        self.name = name
        self.orientation = orientation

        self.setContentsMargins(0, 0, 0, 0)

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("background: transparent;"
                                "border : 0px;")  # Set QGraphicsView background to transparent
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scene = QGraphicsScene(self.view)
        self.view.setScene(self.scene)

        # Add two spaces around the name
        label = QLabel(f" {name} ")
        label.setProperty("class", "standardLabel")
        label.setStyleSheet("background: transparent;")  # Set QLabel background to transparent

        # Convert 0 to 1 color values into 0 to 255 values
        color = [int(color * 255) for color in color]
        color = f"{color[0]}, {color[1]}, {color[2]}"
        label.setStyleSheet(f"background-color : rgb({color});")
        label.adjustSize()

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(label)

        # Apply rotation transformation
        proxy.setTransformOriginPoint(label.rect().center())
        proxy.setRotation(rotation)

        self.scene.addItem(proxy)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        match rotation :
            case 0 | 180:
                self.setFixedHeight(label.height())
            case 45 | 135 | 225 | 315:
                self.setFixedWidth(label.width() ** (1/2))
                self.setFixedHeight(label.width() ** (1/2))
            case 90 | 270:
                self.setFixedWidth(label.height())

    def mousePressEvent(self, ev):
        """
        Handles mouse press events by emitting the clicked signal with the object's name.

        Parameters
        ----------
        ev : QMouseEvent
            The mouse event containing information about the mouse action.
        """
        
        # Emit object name
        self.clicked.emit(self.objectName())
