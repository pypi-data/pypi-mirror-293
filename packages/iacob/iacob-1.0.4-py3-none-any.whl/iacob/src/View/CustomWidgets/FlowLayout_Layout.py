from PyQt5.QtCore import QMargins, Qt, QRect, QSize, QPoint
from PyQt5.QtWidgets import QLayout, QSizePolicy


class FlowLayout(QLayout):
    """
    A class to manage and arrange child widgets in a flow layout, wrapping them to the next line when the available width is exceeded.
    """
    def __init__(self, parent=None):
        """
        Initializes the FlowLayout instance.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget of this layout. If provided, the layout's contents margins are set to zero.
        """

        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        """
        Destructor for FlowLayout.

        Ensures that all items are properly removed and deleted.
        """

        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        """
        Adds an item (widget) to the layout.

        Parameters
        ----------
        item : QLayoutItem
            The layout item to be added.
        """

        self._item_list.append(item)

    def count(self):
        """
        Returns the number of items in the layout.

        Returns
        -------
        int
            The number of items in the layout.
        """

        return len(self._item_list)

    def itemAt(self, index):
        """
        Returns the item at the specified index.

        Parameters
        ----------
        index : int
            The index of the item to retrieve.

        Returns
        -------
        QLayoutItem or None
            The layout item at the specified index, or None if the index is out of range.
        """

        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        """
        Removes and returns the item at the specified index.

        Parameters
        ----------
        index : int
            The index of the item to be removed.

        Returns
        -------
        QLayoutItem or None
            The removed layout item, or None if the index is out of range.
        """

        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        """
        Specifies that the layout does not expand in any direction.

        Returns
        -------
        Qt.Orientations
            A flag indicating no expansion in either horizontal or vertical directions.
        """

        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        """
        Indicates that the layout's height depends on its width.

        Returns
        -------
        bool
            Always returns True, as the layout adapts its height based on its width.
        """

        return True

    def heightForWidth(self, width):
        """
        Returns the preferred height for the given width.

        Parameters
        ----------
        width : int
            The width available for the layout.

        Returns
        -------
        int
            The calculated height required to accommodate the layout within the given width.
        """

        height = self._doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        """
        Sets the geometry of the layout within the specified rectangle.

        Parameters
        ----------
        rect : QRect
            The rectangle defining the layout's geometry.
        """

        super(FlowLayout, self).setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        """
        Returns the preferred size of the layout.

        Returns
        -------
        QSize
            The minimum size hint for the layout.
        """

        return self.minimumSize()

    def minimumSize(self):
        """
        Returns the minimum size needed by the layout.

        Returns
        -------
        QSize
            The minimum size needed by the layout to accommodate all items.
        """

        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _doLayout(self, rect, test_only):
        """
        Performs the layout of items within the specified rectangle.

        Parameters
        ----------
        rect : QRect
            The rectangle within which to lay out the items.
        test_only : bool
            If True, the function only calculates the layout without actually setting the geometry of items.

        Returns
        -------
        int
            The total height used by the layout within the specified width.
        """

        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()

    def clear(self):
        """
        Clears the layout by removing and deleting all items.
        """

        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()