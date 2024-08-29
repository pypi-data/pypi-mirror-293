import os
from pathlib import Path

from src.globals import colorPalettes

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.Controller.MainWindow_Controller import MainWindow_Controller
from src.View.ui.MainWindow_ui import Ui_IACOB


class MainWindowView(QMainWindow, Ui_IACOB):
    """
    A class to initialize the view of MainController Window
    """

    def __init__(self):
        """
        Initializes the MainWindow_View
        """
        
        super().__init__()

        self.setupUi(self)

        self.openRecentProjects_menu = None
        self.openRecentFilters_menu = None

        self.mainWindow_controller = MainWindow_Controller(self)
        self.menuBar.setNativeMenuBar(False)

        self.InitView()
        self.InitActions()
        self.InitLoadingImages()
        self.InitGraphPreparation()
        self.InitColorPaletteChoice()

    def InitView(self):
        """
        Initializes the View
            -> Hide (or Show) some element
        """

        # Hide the dock widget for the "FileInfo" tab only
        if self.mainTabWidget.currentIndex() == 0:
            self.dockWidget.hide()
        else:
            self.dockWidget.show()

        # Tab1 : File Infos
        self.fileInfosSupport_Frame.hide()
        self.noInfoTab1_Label.show()

        # Tab2 : Circular
        self.circularTabSupport_Frame.hide()
        self.noInfoTab2_Label.show()

        # Tab3 : Pie
        self.pieTabWidget.hide()
        self.noInfoTab3_Label.show()

        # Tab4 : List
        self.listSupport_Frame.hide()
        self.noInfoTab4_Label.show()

        # Tab5 : GT
        self.tabGT_TableWidget.hide()
        self.noInfoTab5_Label.show()

    def InitGraphPreparation(self):
        """
        Initializes the File Infos Graphic
            -> Canvas Creation
        """

        # Create a Matplotlib figure and a canvas to display it
        self.graph_curve = Figure()
        self.canvas = FigureCanvas(self.graph_curve)
        self.graphDisplay_Layout.addWidget(self.canvas)

        # Add two custom QLineEdit for discardWeight and discardAbsWeight inputs
    
    def InitActions(self):
        """
        Initializes the slot for the toolbar from the View

        Sets up the Menu / Button for creating, opening, and closing projects, as well as managing filters. 
        Connects slots to theirs corresponding actions.
        """

        # ====================================
        # ===== Project / Filters Files ======
        # ====================================

        # ----- Project Files -----

        # & define a quick key to jump to this menu by pressing alt+F
        self.file_toolBarMenu = self.menuBar.addMenu("&Files")
        self.file_toolBarMenu.addAction(self.mainWindow_controller.createProject_action)
        self.file_toolBarMenu.addAction(self.mainWindow_controller.openProject_action)

        # Open Recent Project
        self.openRecentProjects_menu = self.file_toolBarMenu.addMenu("Open Recent Project")

        self.separatorRecentProject = self.openRecentProjects_menu.addSeparator()
        self.openRecentProjects_menu.addAction(self.mainWindow_controller.clearRecentProjects_action)

        self.file_toolBarMenu.addAction(self.mainWindow_controller.exportProject_action)
        self.file_toolBarMenu.addAction(self.mainWindow_controller.closeProject_action)

        # ----- Filters Files -----
        self.separator = self.file_toolBarMenu.addSeparator()
        self.openFilters = self.file_toolBarMenu.addAction(self.mainWindow_controller.openFilters_action)

        # Open Recent Filters
        self.openRecentFilters = self.openRecentFilters_menu = self.file_toolBarMenu.addMenu("Open Recent Filters")

        self.separatorRecentFilters = self.openRecentFilters_menu.addSeparator()
        self.exportFilters = self.openRecentFilters_menu.addAction(self.mainWindow_controller.clearRecentFilters_action)

        self.file_toolBarMenu.addAction(self.mainWindow_controller.exportFilters_action)

        # ===== Other Buttons ======
        self.help_toolBarAction = self.menuBar.addAction(self.mainWindow_controller.help_action)
        self.about_toolBarAction = self.menuBar.addAction(self.mainWindow_controller.about_action)

        self.resetFilter_button.setDefaultAction(self.mainWindow_controller.resetFilter_action)
        self.resetGraphicFilter_button.setDefaultAction(self.mainWindow_controller.resetGraphicFilter_action)
        self.exportCircular_button.setDefaultAction(self.mainWindow_controller.exportCircularGraphic_action)
        self.exportList_button.setDefaultAction(self.mainWindow_controller.exportList_action)

        self.mainWindow_controller.InitToolBar()

    def InitLoadingImages(self):
        """
        Loads and sets icons for various buttons in the UI.

        Loads a specific image from the resources directory and applies 
        it as an icon to several buttons related to graphics.
        """
        
        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        imagePath = os.path.join(resourcedir, "images", "plus.png")

        # Load image using the variable path
        pixmap_plus = QPixmap(imagePath)
        pixmap_plus = pixmap_plus.scaled(self.addGraphic_button.width(), self.addGraphic_button.height(),
                               Qt.KeepAspectRatioByExpanding)

        # Check if pixmap loaded successfully
        if not pixmap_plus.isNull():

            # Set pixmap as icon for the tool button
            icon_Qicon = QIcon(pixmap_plus)

            self.addGraphic_button.setIcon(icon_Qicon)
            self.addGraphic_button.setIconSize(pixmap_plus.size())
            self.addGraphic2_button.setIcon(icon_Qicon)
            self.addGraphic2_button.setIconSize(pixmap_plus.size())
            self.addGraphic3_button.setIcon(icon_Qicon)
            self.addGraphic3_button.setIconSize(pixmap_plus.size())
            self.addGraphic4_button.setIcon(icon_Qicon)
            self.addGraphic4_button.setIconSize(pixmap_plus.size())
            self.addGraphic5_button.setIcon(icon_Qicon)
            self.addGraphic5_button.setIconSize(pixmap_plus.size())
            self.addGraphGT_button.setIcon(icon_Qicon)
            self.addGraphGT_button.setIconSize(pixmap_plus.size())

        else:
            print("[ERROR] Image Not Correctly Loaded")

    def InitColorPaletteChoice(self):
        """
        Initializes the color palette selection.

        Populates the colorPalette_comboBox with available color palettes 
        from the `colorPalettes` dictionary (globals variable) and initializes the displayColorPalette_Label 
        with a gradient style to visualize the selected palette.
        """

        for palette_name, colors in colorPalettes.items():
            # Ajouter le texte et associer les couleurs comme data
            self.colorPalette_comboBox.addItem(palette_name, colors)

        self.displayColorPalette_Label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \
                                                     stop:0 rgba(255, 0, 0, 255), \
                                                     stop:0.5 rgba(200, 200, 200, 255), \
                                                     stop:1 rgba(0, 0, 255, 255));")

    def LoadIcon(self, iconType):
        """
        Loads and returns an icon based on the provided icon type.

        Parameters
        ----------
        iconType : str
            The name of the icon file (warning or error) to load.

        Returns
        -------
        QIcon
            The loaded QIcon object to be used in the UI.
        """
        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        imagePath = os.path.join(resourcedir, "images", iconType + ".png")

        return QIcon(imagePath)
 

    # ====================================
    # ===== Warnings / Errors Popups =====
    # ====================================

    def WarningPopUpFilters(self, filtersToIgnore):
        """
        Displays a warning popup about filter incoherence.

        Based on the provided filtersToIgnore list, shows a message box 
        indicating which filter incoherences exist. The user can choose 
        to ignore these incoherences or cancel the operation.

        Parameters
        ----------
        filtersToIgnore : list of bool
            A list indicating which filters are incoherent (True) or coherent (False).
        """

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Coherence Filters")

        # Display a different text depending of the incoherent (and theirs numbers)
        if filtersToIgnore.count(True) > 1:
            text = "Data and FLUT files are not coherent. \
                        \nDo you want ignore Incoherences ?"
        else:
            match filtersToIgnore.index(True):
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
        ignoreButton.clicked.connect(self.mainWindow_controller.IgnoreFiltersIncoherences)
        cancelButton.clicked.connect(self.mainWindow_controller.CancelFilters)

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
        displayButton.clicked.connect(self.mainWindow_controller.DisplayAllRegions)
        hideButton.clicked.connect(self.mainWindow_controller.HideRegions)

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
        ignoreButton.clicked.connect(self.mainWindow_controller.IgnoreDATAFLUTIncoherences)
        cancelButton.clicked.connect(self.mainWindow_controller.CancelFLUT)

        msgBox.exec_()

    def ErrorLoading(self, text):
        """
        Displays an error popup.

        Shows a message box to inform the user of an error during loading 
        or processing. The user can acknowledge the message by clicking OK.

        Parameters
        ----------
        text : str
            The error message to display in the popup.
        """

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Error Display")
        msgBox.setText(text)
        msgBox.setWindowIcon(self.LoadIcon("error"))

        okButton = QPushButton("OK")
        msgBox.addButton(okButton, QMessageBox.ActionRole)
        okButton.clicked.connect(msgBox.accept)

        msgBox.exec_()
    

    # =======================
    # ===== Close Event =====
    # =======================

    def closeEvent(self, event):
        """
        Handles the window close event.

        Ensures that when the application window is closed, any necessary 
        data is saved by invoking the `SaveData` method of the controller.

        Parameters
        ----------
        event : QCloseEvent
            The close event triggered by the user or system.
        """

        # when the application is closed, called the control to save some data
        if hasattr(self, 'mainWindow_controller'):
            self.mainWindow_controller.SaveData()