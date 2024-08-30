from PyQt5.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem):
    """
    A QTableWidgetItem subclass for handling numeric values in a QTableWidget.
    """

    def __init__(self, value):
        """
        Initialize the NumericTableWidgetItem with a numeric value.

        Converts the numeric value to a string for display purposes 
        and stores the original value for numeric comparisons.

        Parameters
        ----------
        value : int, float
            The numeric value to initialize the table item with.
        """

        super().__init__(str(value))
        self.value = value

    def __lt__(self, other):
        """
        Less-than comparison operator for numeric sorting.

        Compares the numeric value of this item with another 
        NumericTableWidgetItem to determine their order.

        Parameters
        ----------
        other : NumericTableWidgetItem
            The other table item to compare against.

        Returns
        -------
        bool
            True if this item's value is less than the other item's value, False otherwise.
        """

        if isinstance(other, NumericTableWidgetItem):
            return self.value < other.value
        return super().__lt__(other)