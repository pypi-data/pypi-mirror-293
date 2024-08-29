import os
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.View.ui.ImportWindow_ui import Ui_ImportWindow
from src.Controller.ImportFile_Controller import ImportFile_Controller


class ImportFile_View(QtWidgets.QMainWindow, Ui_ImportWindow):
    """
    A class to initialize the view of ImportFile Window
    """

    def __init__(self, parent=None):
        """
        Initializes all view elements and like actions to buttons
        """
        
        super(ImportFile_View, self).__init__(parent=parent)

        # Load UI Interface
        self.setupUi(self)

        # Load Controler File
        self.importFile_Controller = ImportFile_Controller(self)

        # Action Configuration
        self.InitAction()

        # Hidden Elements
        self.HiddenElements()

        # Images Loading
        self.InitLoadingImages()

        # Graph Preparation
        self.InitGraphPreparation()

    def InitAction(self):
        """
        Associate actions to widgets when the application is opened.

        This method configures various actions such as resizing the window,
        enabling mouse tracking on file list widgets, and assigning actions 
        to tool buttons.
        """

        # Resize the Window (90%)
        self.ResizeWindow()

        # Display Full Path when the mouse entered the item
        self.previousDataFiles_List.setMouseTracking(True)
        self.previousFlutFiles_List.setMouseTracking(True)
        self.previousFiltersFiles_List.setMouseTracking(True)

        # Asssociate Action to ToolButton
        self.importDataFile_Button.setDefaultAction(self.importFile_Controller.OpenDataFile_Qaction)
        self.importNameFile_Button.setDefaultAction(self.importFile_Controller.OpenNameFile_Qaction)
        self.importFlutFile_Button.setDefaultAction(self.importFile_Controller.OpenFlutFile_Qaction)
        self.importFiltersFile_Button.setDefaultAction(self.importFile_Controller.OpenFiltersFile_Qaction)
        self.validation_Button.setDefaultAction(self.importFile_Controller.Validation_Qaction)

    def HiddenElements(self):
        """
        Hide specific elements when the application is opened.

        This method hides labels, buttons, and the graph section that should
        not be visible until certain actions are performed by the user.
        """

        # Label / Button to import Name File
        self.openedNameFile_Label.hide()
        self.importNameFile_Button.hide()

        self.errorDataNameFile_Label.hide()
        self.errorFlutFile_Label.hide()
        self.errorFiltersFile_Label.hide()

        # Graph Section
        self.graphSection_Widget.hide()

    def InitLoadingImages(self):
        """
        Load images and associate them with the tool buttons.

        This method loads an image from the resources directory, scales it, 
        and sets it as an icon for multiple tool buttons.
        """

        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        imagePath = os.path.join(resourcedir, "images", "folder.png")

        # Load image using the variable path
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(self.importDataFile_Button.width(), self.importDataFile_Button.height(),
                               Qt.KeepAspectRatioByExpanding)

        # Check if pixmap loaded successfully
        if not pixmap.isNull():

            # Set pixmap as icon for the tool button
            icon_Qicon = QIcon(pixmap)

            self.importDataFile_Button.setIcon(icon_Qicon)
            self.importDataFile_Button.setIconSize(pixmap.size())
            self.importNameFile_Button.setIcon(icon_Qicon)
            self.importNameFile_Button.setIconSize(pixmap.size())
            self.importFlutFile_Button.setIcon(icon_Qicon)
            self.importFlutFile_Button.setIconSize(pixmap.size())
            self.importFiltersFile_Button.setIcon(icon_Qicon)
            self.importFiltersFile_Button.setIconSize(pixmap.size())

        else:
            print("[ERROR] Image Not Correctly Loaded")
    
    def InitGraphPreparation(self):
        """
        Create a Matplotlib figure and a canvas to display histograms.

        This method initializes a Matplotlib figure and embeds it within the 
        GUI for displaying histograms or other graphical data.
        """

        # Create a Matplotlib figure and a canvas to display it
        self.graph = Figure()
        self.canvas = FigureCanvas(self.graph)
        self.graphDisplay_Layout.addWidget(self.canvas)

    def ResizeWindow(self):
        """
        Resize the window to 90% of the screen size when the application is opened.

        This method calculates the new window dimensions based on the primary screen's 
        size and positions the window centrally.
        """

        # Obtain the Screen Size
        screen = QGuiApplication.primaryScreen().geometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # Define the Window Size (80%)
        widthPercentage = 0.9
        heightPercentage = 0.9

        # Compute the new Window Size
        newWidth = int(screenWidth * widthPercentage)
        newHeight = int(screenHeight * heightPercentage)

        startX = int((screenWidth * (1 - widthPercentage)) / 2)
        startY = int((screenHeight * (1 - widthPercentage)) / 2)

        # Apply new Value
        #self.resize(newWidth, newHeight)
        self.setGeometry(startX, startY, newWidth, newHeight)

    def LoadIcon(self, iconType):
        """
        Load an icon based on the specified type.

        Parameters
        ----------
        iconType : str
            The type of icon to load (warning).

        Returns
        -------
        QIcon
            The loaded QIcon object.
        """

        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        imagePath = os.path.join(resourcedir, "images", iconType + ".png")

        return QIcon(imagePath)


    # ===========================
    # ===== Warnings Popups =====
    # ===========================

    def WarningPopUpFilters(self, filtersToIgnore):
        """
        Display a warning popup about filter incoherences.

        Parameters
        ----------
        filtersToIgnore : list of bool
            List indicating which filters are incoherent.
        """

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Coherence Filters")

        # Display a different text depending of the incoherent (and theirs numbers)
        if filtersToIgnore.count(True) > 1:
            text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Incoherences ?"
        else:
            match filtersToIgnore.index(False)[0]:
                case 0:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Pre-Filter Threshold Incoherence ?"
                case 1:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Relative Threshold Incoherence ?"
                case 2:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Relative Threshold Incoherence ?"
                case 3:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Absolu Threshold Incoherence ?"
                case 4:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Absolu Threshold Incoherence ?"
                case 5:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Rank Threshold Incoherence ?"
                case 6:
                    text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Inter-Region Incoherence(s) ?"
                    
        msgBox.setText(text)
        msgBox.setWindowIcon(self.LoadIcon("warning"))
        
        ignoreButton = QPushButton("Ignore")
        cancelButton = QPushButton("Cancel")

        msgBox.addButton(ignoreButton, QMessageBox.ActionRole)
        msgBox.addButton(cancelButton, QMessageBox.ActionRole)

        # Connect button to ImportFile Controller Methods
        ignoreButton.clicked.connect(self.importFile_Controller.IgnoreFiltersIncoherences)
        cancelButton.clicked.connect(self.importFile_Controller.CancelFilters)

        msgBox.exec_()

    def WarningPopUpNumberRegion(self):
        """
        Displays a warning popup about the number of regions.

        Alerts the user that the number of regions is higher than the recommended 
        limit. The user can choose to display all regions or hide those not present 
        in the data file.
        """

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Region Number")
        msgBox.setText("The number of regions is higher than the recommended number (150 with blanks). \
                       \nDo you want to DISPLAY all regions, or HIDE regions not present in data file ?")
        msgBox.setWindowIcon(self.LoadIcon("warning"))
        
        displayButton = QPushButton("Display")
        hideButton = QPushButton("Hide")

        msgBox.addButton(displayButton, QMessageBox.ActionRole)
        msgBox.addButton(hideButton, QMessageBox.ActionRole)

        # Connect button to ImportFile Controller Methods
        displayButton.clicked.connect(self.importFile_Controller.DisplayAllRegions)
        hideButton.clicked.connect(self.importFile_Controller.HideRegions)

        msgBox.exec_() 
    
    def WarningPopUpDATAFLUT(self):
        """
        Display a warning popup about incoherences between Data and FLUT files.

        This method prompts the user to either ignore the incoherences or cancel 
        the validation process.
        """

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Coherence Verification")
        msgBox.setText("Data and FLUT files are not coherent. \
                       \nDo you want ignore Incoherence(s) ?")
        msgBox.setWindowIcon(self.LoadIcon("warning"))
        
        ignoreButton = QPushButton("Ignore")
        cancelButton = QPushButton("Cancel")

        msgBox.addButton(ignoreButton, QMessageBox.ActionRole)
        msgBox.addButton(cancelButton, QMessageBox.ActionRole)

        # Connect button to ImportFile Controller Methods
        ignoreButton.clicked.connect(self.importFile_Controller.IgnoreDATAFLUTIncoherences)
        cancelButton.clicked.connect(self.importFile_Controller.CancelFLUT)

        msgBox.exec_()


    # =======================
    # ===== Close Event =====
    # =======================
    
    def closeEvent(self, event):
        """
        Handle the event when the window is closed.

        This method ensures that when the application is closed, 
        the controller is called to save necessary data.

        Parameters
        ----------
        event : QCloseEvent
            The close event triggered when the window is closed.
        """

        # when the application is closed, called the control to save some data
        if hasattr(self, 'importFile_Controller'):
            self.importFile_Controller.CloseImportWithoutValidation()
