import os
import math
import statistics

import networkx as nx

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QListWidgetItem, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt, QStandardPaths, QTimer

from src.Controller.LoadingPopup import LoadingPopup

from src.Model.ImportData_Files import ParserData_Files
from src.Model.ImportName_Files import ParserName_Files
from src.Model.ImportFlut_Files import ParserFlut_Files
from src.Model.ImportFilters_Files import ParserFilters_Files

from src.Model.Data_Storage.ConnGraph_Model import ConnGraph_Infos
from src.Model.Data_Storage.ConnGraphSave_Model import ConnGraphSave_Infos
from src.Model.Data_Storage.Filters_Model import Filters_Infos
from src.Model.Data_Storage.FiltersSave_Model import FiltersSave_Infos
from src.Model.Data_Storage.Project_Model import Project_Infos

from copy import deepcopy

class ImportFile_Controller:
    """
        Import File Controller
    """

    connGraph: ConnGraph_Infos
    connGraphSave: ConnGraphSave_Infos
    filters: Filters_Infos
    filtersSave: FiltersSave_Infos
    project: Project_Infos

    def __init__(self, ImportFile_View):

        self.importFile_View = ImportFile_View

        self.connGraph = ConnGraph_Infos()
        self.connGraphSave = ConnGraphSave_Infos()
        self.connGraphSave.LoadCurrentConnGraph(self.connGraph.SaveCurrentConnGraph())

        self.filters = Filters_Infos()
        self.filtersSave = FiltersSave_Infos()
        self.filtersSave.LoadCurrentFilters(self.filters.SaveCurrentFilters())

        self.project = Project_Infos()
        self.projectSave = deepcopy(self.project)

        # Loaded File
        self.flutFile: str = None
        self.dataFile: str = None
        self.nameFile: str = None

        self.threshold: float = None
        self.rank: int = None

        # Validation Part
        self.filtersToIgnore = [False, False, False, False, False, False, False]
        self.validation = False

        # Create all actions used by wingets
        self._ActionCreation()

        # Other Initial Value
        self._OtherInit()

        self.connGraph.InitReset()
        self.filters.InitReset()
        self.project.InitReset()


    # ===========================
    # ===== INITIALIZATION ======
    # ===========================

    def _ActionCreation(self):
        """
        Creates actions for file operations and connects them to their corresponding slots.

        Actions created:
        - Open Data File
        - Open Name File
        - Open Flut File
        - Open Filters File
        - Validation
        - Slider and SpinBox value change
        - Table item click
        """

        # Action Creation - Open Data File
        self.OpenDataFile_Qaction = QtWidgets.QAction('ImportDataFile', self.importFile_View)
        self.OpenDataFile_Qaction.triggered.connect(self.OpenDataFile)

        # Action Creation - Open Name File
        self.OpenNameFile_Qaction = QtWidgets.QAction('ImportNameFile', self.importFile_View)
        self.OpenNameFile_Qaction.triggered.connect(self.OpenNameFile)

        # Action Creation - Open Name File
        self.OpenFlutFile_Qaction = QtWidgets.QAction('ImportFlutFile', self.importFile_View)
        self.OpenFlutFile_Qaction.triggered.connect(self.OpenFlutFile)

        # Action Creation - Open Filters File
        self.OpenFiltersFile_Qaction = QtWidgets.QAction('ImportFiltersFile', self.importFile_View)
        self.OpenFiltersFile_Qaction.triggered.connect(self.OpenFiltersFile)

        # Action Creation - Data/Filter Validation
        self.Validation_Qaction = QtWidgets.QAction('Validation', self.importFile_View)
        self.Validation_Qaction.triggered.connect(self.Validation)

        # Action when Slider / Spin value change
        self.importFile_View.threshold_Slider.sliderReleased.connect(self.SliderValue)
        self.importFile_View.thresholdValue_DoubleSpinBox.valueChanged.connect(self.SpinValue)

        # Action when row in the Table is clicked
        self.importFile_View.percentageTable_TableWidget.itemClicked.connect(self.TablePercentageValue)
        self.importFile_View.nbTable_TableWidget.itemClicked.connect(self.TableNbValue)

    def _OtherInit(self):
        """
        Initializes file lists and sets up item double-click actions.
        """

        # Widget List Initialization

        # For each File (Data / Flut / Filters / Project)
        for dataFile_fullPath, fileType in self.project.previousFiles["DataFiles"].items():

            # Check if the Data File is associated with a Name File
            if dataFile_fullPath in self.project.previousFiles["NameFiles"]:

                nameFile = self.project.previousFiles["NameFiles"][dataFile_fullPath]
                newItem = QListWidgetItem("".join(["\u21A6    (Data File) ", os.path.basename(dataFile_fullPath), "\n", \
                                                    "\u21AA    (Name File) ", os.path.basename(nameFile)]))
                newItem.setData(Qt.UserRole, [dataFile_fullPath, nameFile])
                newItem.setToolTip("".join(["\u21A6 (Data File) ", dataFile_fullPath, "\n", \
                                            "\u21AA (Name File) ", nameFile]))

            else:
                newItem = QListWidgetItem("\u21A6    ({}) {}".format(fileType, os.path.basename(dataFile_fullPath)))
                newItem.setData(Qt.UserRole, [dataFile_fullPath])
                newItem.setToolTip("\u21A6 ({}) {}".format(fileType, dataFile_fullPath))

            self.importFile_View.previousDataFiles_List.addItem(newItem)

        for flutFile in self.project.previousFiles["FlutFiles"]:

            newItem = QListWidgetItem("\u21A6    {}".format(os.path.basename(flutFile)))
            newItem.setData(Qt.UserRole, flutFile)
            newItem.setToolTip(flutFile)
            self.importFile_View.previousFlutFiles_List.addItem(newItem)

        for filtersFile in self.project.previousFiles["FiltersFiles"]:

            newItem = QListWidgetItem("\u21A6    {}".format(os.path.basename(filtersFile)))
            newItem.setData(Qt.UserRole, filtersFile)
            self.importFile_View.previousFiltersFiles_List.addItem(newItem)

        # Other Initialization
        self.importFile_View.limitedGraph_TabWidget.setCurrentIndex(0)

        # Makes All Label in the QListWidget double Clickable
        self.importFile_View.previousDataFiles_List.itemDoubleClicked.connect(self.PreviousDataFile_Click)
        self.importFile_View.previousFlutFiles_List.itemDoubleClicked.connect(self.PreviousFlutFile_Click)
        self.importFile_View.previousFiltersFiles_List.itemDoubleClicked.connect(self.PreviousFiltersFile_Click)


    # ======================
    # ===== Open Files =====
    # ======================

    def OpenDataFile(self):
        """
        Opens a file dialog to load a data file (MAT files, text files).
        
        Calls:
            LoadData(fileName): if a file is selected.
        """

        userDirectory = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        fileName, _ = QFileDialog.getOpenFileName(self.importFile_View,
                                                "Open Data File",
                                                userDirectory,
                                                "Supported Files (*.mat *.txt)")

        if fileName:
            self.LoadData(fileName)

    def OpenNameFile(self):
        """
        Opens a file dialog to load a name file (TXT files).
        
        Calls:
        - LoadName(fileName) if a file is selected.
        """

        userDirectory = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        fileName, _ = QFileDialog.getOpenFileName(self.importFile_View,
                                                "Open Name File",
                                                userDirectory,
                                                "Supported Files (*.txt)")

        if fileName:
            self.LoadName(fileName)

    def OpenFlutFile(self):
        """
        Opens a file dialog to load a flut file (FLUT files).
        
        Calls:
            LoadFlut(fileName) if a file is selected.
        """

        userDirectory = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        fileName, _ = QFileDialog.getOpenFileName(self.importFile_View,
                                                "Open Flut File",
                                                userDirectory,
                                                "Supported Files (*.flut)")

        if fileName:
            self.LoadFlut(fileName)

    def OpenFiltersFile(self):
        """
        Opens a file dialog to load a filters file (JSON files) if both data and flut files are loaded.
        
        Shows an error if data or flut files are missing.
        
        Calls:
            LoadFilters(fileName) if a file is selected and both data and flut files are available.
        """

        if not self.dataFile or not self.flutFile:
            self.importFile_View.errorFiltersFile_Label.show()
            self.importFile_View.errorFiltersFile_Label.setText("Require Data and FLUT")
            return

        userDirectory = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        fileName, _ = QFileDialog.getOpenFileName(self.importFile_View,
                                                "Open Filters File",
                                                userDirectory,
                                                "Supported Files (*.json)")

        if fileName:
            self.LoadFilters(fileName)


    # =========================
    # ===== Update Object =====
    # =========================

    def UpdateConnGraph(self):
        """
        Updates the connection graph by removing edges with values below the threshold and updating graph information.
        """

        nxGraph = nx.Graph()
        for areaInfoName in self.connGraph.areaInfos.keys():
            nxGraph.add_node(areaInfoName)

        edgesValuesCopy = deepcopy(self.connGraph.edgesValues)
        for id_source, DestValue in edgesValuesCopy.items():
                
            for id_dest, value in DestValue.items():

                if abs(value) < self.threshold:
                    del self.connGraph.edgesValues[id_source][id_dest]
                    continue

            if len(self.connGraph.edgesValues[id_source]) == 0:
                del self.connGraph.edgesValues[id_source]

        self.connGraph.SetGraph(nxGraph)

        edgesValues_withoutDuplicata_Copy = deepcopy(self.connGraph.edgesValues_withoutDuplicata)
        for nodeIDnodeDest, value in edgesValues_withoutDuplicata_Copy.items():
            if abs(value) < self.threshold:
                del self.connGraph.edgesValues_withoutDuplicata[nodeIDnodeDest]

        self.connGraph.numberOfEdges = len(self.connGraph.edgesValues_withoutDuplicata)
        
    def UpdateFilters(self):
        """
        Updates filter settings based on current graph and threshold values.
        """

        # Initialize Filters Object if the attribut isn't None
        self.filters.valueRound = self.valueRound
        self.filters.thresholdPostFiltering = self.threshold

        if not self.filters.weightBetween_threshold[1]:
            self.filters.SetWeightMax(self.connGraph.minMax[1])
        if not self.filters.weightBetween_threshold[0]:
            self.filters.SetWeightMin(self.connGraph.minMax[0])

        self.filters.SetAbsWeightMin(self.RoundInitialization(self.threshold))
        if not self.filters.absWeightBetween_threshold[1]:
            self.filters.SetAbsWeightMax(self.connGraph.absMinMax[1])

        self.filters.SetRankMax(self.rank)
        self.filters.SetRankMin(0)

        # Only one filter of this type can be active at the same time
        if self.filters.discardWeight:
            self.filters.discardRank = self.filters.discardAbsWeight = False
        if self.filters.discardAbsWeight:
            self.filters.discardRank = self.filters.discardWeight = False
        if self.filters.discardRank:
            self.filters.discardWeight = self.filters.discardAbsWeight = False

    def UpdateProject(self):
        """
        Updates the project with the current data, name, and flut files.
        """

        self.project.currentDataFile = self.dataFile
        self.project.currentNameFile = self.nameFile
        self.project.currentFlutFile = self.flutFile


    # ======================
    # ===== Validation =====
    # ======================

    def Validation(self):
        """
        Validates the presence of required files and initiates loading process if validation passes.
        Shows warnings or error messages as needed.
        """

        # Handle Data File Missing
        if self.dataFile is None:
            self.importFile_View.errorValidation_Label.show()
            self.importFile_View.errorValidation_Label.setText("Data File Missing")
            return

        # Handle FLUT File Missing
        elif self.flutFile is None:
            self.importFile_View.errorValidation_Label.show()
            self.importFile_View.errorValidation_Label.setText("FLUT File Missing")
            return

        # Handle Name File Missing
        elif self.nameFile is None:
            self.importFile_View.errorValidation_Label.show()
            self.importFile_View.errorValidation_Label.setText("Name File Missing")
            return

        if len(self.connGraph.areasOrder) > 150:
            self.importFile_View.WarningPopUpNumberRegion()

        self.loadingPopup = LoadingPopup(self.importFile_View)
        self.loadingPopup.show()
        QTimer.singleShot(100, self.LoadingExecute)

    def LoadingExecute(self):
        """
        Performs long-running operations, including updating graph, filters, and project.
        Finalizes the loading process and updates the main window.
        """

        # Perform long-running operations
        self.connGraph.SetTypeConnexion()
        self.UpdateConnGraph()
        self.UpdateFilters()
        self.UpdateProject()

        self.validation = True

        # Finalize operations
        self.importFile_View.parent().mainWindow_controller.LoadDataMainWindow()
        self.loadingPopup.accept()
        self.importFile_View.close()

    def HideRegions(self):
        """
        Updates the area order and information by removing unused areas.
        """

        idName_Inversed = {str(name): ID for ID, name in self.connGraph.idName.items()}
        newAreaOrder = []

        # Delete unused area between Data File and Flut File
        for item in self.connGraph.areasOrder:
            if item[0] in idName_Inversed or str(item[1]) in idName_Inversed:
                newAreaOrder.append(item)
            elif item[0] == 'xxxx':
                newAreaOrder.append(item)

        self.connGraph.areasOrder = newAreaOrder
        self.connGraph.areaInfos = self.limitedAreaInfo

        self.connGraph.numberOfNodes = len(self.connGraph.areaInfos)

    def DisplayAllRegions(self):
        """
        Displays all regions.
        Do nothing (don't delete anything)
        """

        # Display all regions
        pass


    # ==================================
    # ===== Previous Files Actions =====
    # ==================================

    def PreviousDataFile_Click(self, item: QListWidgetItem):
        """
        Load data and optionally name file based on the clicked item.

        Parameters
        ----------
        item : QListWidgetItem
            The item representing the data file and optionally name file.
        """
        
        # Recovert the full path
        dataItem = item.data(Qt.UserRole)

        # Len = 1 -> Only Data File
        if len(dataItem) == 1:
            self.LoadData(dataItem[0])

        # Len = 2 -> Data File + Name File
        else:
            self.LoadData(dataItem[0])
            self.LoadName(dataItem[1])

    def PreviousFlutFile_Click(self, item: QListWidgetItem):
        """
        Load the FLUT file based on the clicked item.

        Parameters
        ----------
        item : QListWidgetItem
            The item representing the FLUT file.
        """
        
        # Recovert the full path
        self.LoadFlut(item.data(Qt.UserRole))

    def PreviousFiltersFile_Click(self, item: QListWidgetItem):
        """
        Load the filters file if data and FLUT files are already loaded.

        Parameters
        ----------
        item : QListWidgetItem
            The item representing the filters file.
        """

        if not self.dataFile or not self.flutFile:
            self.importFile_View.errorFiltersFile_Label.show()
            self.importFile_View.errorFiltersFile_Label.setText("Require Data and FLUT")

        else:
            # Recovert the full path
            self.LoadFilters(item.data(Qt.UserRole))


    # ==========================
    # ===== FILES LOADING ======
    # ==========================

    def LoadData(self, fileName: str):
        """
        Load and parse the data file, and initialize the graph.

        Parameters
        ----------
        fileName : str
            The path to the data file.

        Raises
        ------
        Exception
            If the parser raise an Exception
        """

        self.importFile_View.errorDataNameFile_Label.hide()
        self.importFile_View.errorValidation_Label.setText("")

        try:
            # Parser the File
            parserDataFile = ParserData_Files()
            parserDataFile.GraphCreation(fileName)

        except Exception as exception:
            print("[ERROR]", exception.args[0])
            self.importFile_View.errorDataNameFile_Label.show()
            self.importFile_View.errorDataNameFile_Label.setText(exception.args[0])
            return
        
        if self.flutFile:

            # Verify the coherence between Data and FLUT Files
            if not self.CoherenceVerification_NAMEFLUT():

                # Popup for warning
                self.importFile_View.WarningPopUpDATAFLUT()

        self.dataFile = fileName
        self.nameFile = None

        # Update Display Label
        self.UpdateOpenedDataFile(fileName)
        self.UpdatePreviousDataFiles(fileName)
        self.importFile_View.currentDataFile_Label.setText(os.path.basename(fileName))

        # Graph Initialization and Display Graph Informations
        self.SetUpGraphValues()
        self.GraphPreparation()
        self.InformationsInitialization()

    def LoadName(self, fileName: str):
        """
        Load and parse the name file, and verify coherence with data file.

        Parameters
        ----------
        fileName : str
            The path to the name file.

        Raises
        ------
        Exception
            If the parser raise an Exception
        """

        self.importFile_View.errorDataNameFile_Label.hide()
        self.importFile_View.errorValidation_Label.setText("")

        try:
            self.parserNameFile = ParserName_Files()
            self.parserNameFile.NameFile_Parser(fileName)
            self.CoherenceVerification_NAMEDATA()

        except Exception as exception:
            print("[ERROR]", exception.args[0])
            self.importFile_View.errorDataNameFile_Label.show()
            self.importFile_View.errorDataNameFile_Label.setText(exception.args[0])
            return

        self.nameFile = fileName
        self.project.previousFiles["NameFiles"][self.dataFile] = self.nameFile

        # Update other element
        self.DisplayImportNamePart()
        self.UpdateOpenedNameFile(fileName)
        self.UpdatePreviousNameFiles(fileName)

        # Update other element (Current File Infos)
        previousFileName_basename = os.path.basename(self.dataFile)
        fileName_basename = os.path.basename(fileName)

        self.importFile_View.currentDataFile_Label.setText("".join([previousFileName_basename, "\n", fileName_basename]))

    def CoherenceVerification_NAMEDATA(self):
        """
        Verify the coherence between data and name files.

        Raises
        ------
        ValueError
            If the number of names and nodes do not match.
        """

        # Verify the correct relation between the Connectivity Matrix and Names
        if self.connGraph.numberOfNodesInData != len(self.connGraph.idName):
            raise Exception("Wrong Format - Different Number of Name/Nodes")

    def LoadFlut(self, fileName: str):
        """
        Load and parse the FLUT file, and verify coherence with data file.

        Parameters
        ----------
        fileName : str
            The path to the FLUT file.

        Raises
        ------
        Exception
            If the parser raise an Exception
        """

        self.importFile_View.errorFlutFile_Label.hide()
        self.importFile_View.errorValidation_Label.setText("")

        try:
            
            # Parser the File
            parserFlutFile = ParserFlut_Files()
            parserFlutFile.FlutFile_Parser(fileName)

        except Exception as exception:
            print("[ERROR]", exception.args[0])
            self.importFile_View.errorFlutFile_Label.show()
            self.importFile_View.errorFlutFile_Label.setText(exception.args[0])
            return

        if self.dataFile:
            # Verify the coherence between Data and FLUT Files
            if not self.CoherenceVerification_NAMEFLUT():

                # Popup for warning
                self.importFile_View.WarningPopUpDATAFLUT()

                if not self.validation:
                    return
            
        self.flutFile = fileName

        # Update other element (Last File Opened)
        self.UpdateOpenedFlutFile(fileName)
        self.UpdatePreviousFlutFiles(fileName)

        self.importFile_View.currentFlutFile_Label.setText(os.path.basename(fileName))
        self.importFile_View.nbNodesValue_Label.setText(str(self.connGraph.numberOfNodes))
    
    def CoherenceVerification_NAMEFLUT(self):
        """
        Verify coherence between name and FLUT files.

        Returns
        -------
        bool
            True if the coherence is valid, False otherwise.
        """

        # Verify the Correlation between Name and Flut (Name and Number of Name)
        areaInfo_idName = {str(ID['ID']): name for name, ID in self.connGraph.areaInfos.items()}
        self.limitedAreaInfo = {}
        self.dataToRemove = []

        # For each Name, compare with Flut Name
        for id, nameOrID in self.connGraph.idName.items():

            if nameOrID in self.connGraph.areaInfos:
                self.limitedAreaInfo[nameOrID] = self.connGraph.areaInfos[nameOrID]
                continue

            elif nameOrID in areaInfo_idName:
                newName = areaInfo_idName[nameOrID]
                self.connGraph.idName[id] = newName
                self.limitedAreaInfo[newName] = self.connGraph.areaInfos[newName]
                continue

            self.dataToRemove.append(id)
            print("This ID or Name is different between DATA and FLUT", nameOrID)

        return self.dataToRemove == []

    def IgnoreDATAFLUTIncoherences(self):
        """
        Remove incoherences between data and FLUT files.
        """

        for id_source in self.dataToRemove:

            del self.connGraph.idName[id_source]

            if id_source in self.connGraph.edgesValues:
                for id_dest in self.connGraph.edgesValues[id_source]:
                    del self.connGraph.edgesValues[id_dest][id_source]


                    minMax = (min(id_source, id_dest), max(id_source, id_dest))
                    if minMax in self.connGraph.edgesValues_withoutDuplicata:
                        del self.connGraph.edgesValues_withoutDuplicata[minMax]
                    else:
                        del self.connGraph.edgesValues_withoutDuplicata[(minMax[1], minMax[0])]

                del self.connGraph.edgesValues[id_source]

        self.validation = True

    def CancelFLUT(self):
        """
        Cancel the FLUT file and update the UI.
        """

        # Coherence after DataFile Loading
        if self.dataFile:

            self.validation = False

        # Coherence after FlutFile Loading
        if self.flutFile:

            self.flutFile = None

            self.importFile_View.currentFlutFile_Label.setText("")
            self.importFile_View.nbNodesValue_Label.setText("...")
            self.importFile_View.openedFlutFile_Label.setText("No Flut File Opened")

    def LoadFilters(self, fileName: str):
        """
        Load and parse the filters file, and verify coherence with data and FLUT files.

        Parameters
        ----------
        fileName : str
            The path to the filters file.

        Raises
        ------
        Exception
            If the parser raise an Exception
        """

        self.importFile_View.errorFiltersFile_Label.hide()
        self.importFile_View.errorValidation_Label.setText("")

        try:

            # Parser the File
            parserFiltersFile = ParserFilters_Files()
            parserFiltersFile.FiltersFile_Parser(fileName)

        except Exception as exception:
            print("[ERROR]", exception.args[0])
            self.importFile_View.errorFiltersFile_Label.show()
            self.importFile_View.errorFiltersFile_Label.setText(exception.args[0])
            return


        # Verify the coherence between Data and FLUT Files
        if not self.CoherenceVerification_DATAFILTERS():

            # Popup for warning
            self.importFile_View.WarningPopUpFilters(self.filtersToIgnore)

            if not self.filtersIgnored:
                return
            
        self.threshold = self.filters.thresholdPostFiltering
        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(self.threshold)

        # Update other element (Last File Opened)
        self.UpdateOpenedFiltersFile(fileName)
        self.UpdatePreviousFiltersFiles(fileName)

    def CoherenceVerification_DATAFILTERS(self):
        """
        Verify coherence between data and filters files.

        Returns
        -------
        bool
            True if the filters are coherent with the data, False otherwise.
        """

        # Coherence Verification between data and threshold
        if self.filters.thresholdPostFiltering < self.absMinMax[0]:
            self.filtersToIgnore[0] = True

        if self.filters.weightBetween_threshold[0] < self.connGraph.minMax[0]:
            self.filtersToIgnore[1] = True

        if self.filters.weightBetween_threshold[1] != self.connGraph.minMax[1]:
            self.filtersToIgnore[2] = True

        if self.filters.absWeightBetween_threshold[0] < self.connGraph.absMinMax[0]:
            self.filtersToIgnore[3] = True

        if self.filters.absWeightBetween_threshold[1] != self.connGraph.absMinMax[1]:
            self.filtersToIgnore[4] = True

        if self.filters.rankBetween_threshold[1] > self.connGraph.numberOfEdges:
            self.filtersToIgnore[5] = True

        allInterRegConnCorrect = True
        allRegionsNames = []

        for namesPair in self.filters.discardInterRegConn.keys():
            for name in namesPair:

                if name not in self.connGraph.colorMajorRegions:
                    allInterRegConnCorrect = False
                    break

            allRegionsNames.append(name)

            if not allInterRegConnCorrect:
                break

        allRegionsNames = list(set(allRegionsNames))
        if len(allRegionsNames) != len(self.connGraph.colorMajorRegions):
            self.filtersToIgnore[6] = True

        allCombinaisonPossible = True

        for region1 in allRegionsNames:
            for region2 in allRegionsNames:
                if (region1, region2) not in self.filters.discardInterRegConn:
                    allCombinaisonPossible = False
                    break

            if not allCombinaisonPossible:
                break

        if not allInterRegConnCorrect or not allCombinaisonPossible:
            self.filtersToIgnore[6] = True

        return self.filtersToIgnore == [False, False, False, False, False, False, False]

    def IgnoreFiltersIncoherences(self):
        """
        Ignore incoherences in filters.
        """

        self.filtersIgnored = True

        for indexFilter, toIgnore in enumerate(self.filtersToIgnore):
            if toIgnore:
                match indexFilter:
                    case 0:
                        self.filters.thresholdPostFiltering = self.absMinMax[0]
                    case 1:
                        self.filters.weightBetween_threshold[0] = None
                    case 2:
                        self.filters.weightBetween_threshold[1] = None
                    case 3:
                        self.filters.absWeightBetween_threshold[0] = None
                    case 4:
                        self.filters.absWeightBetween_threshold[1] = None
                    case 5:
                        self.filters.rankBetween_threshold[1] = None
                    case 6:
                        self.filters.discardInterRegConn = {}

    def CancelFilters(self):
        """
        Cancel the filters file and reset to default.
        """

        self.filtersIgnored = False

        self.importFile_View.openedFiltersFile_Label.setText("No Filters File Opened (Optional File)")
        self.filters.LoadSaveFilters(self.filtersSave.RecovertFiltersSave())

        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(self.absMinMax[0])


    # ====================================
    # ===== INTERFACE INITIALIZATION =====
    # ====================================

    def RoundInitialization(self, value: float):
        """
        Round the given value based on the current rounding setting.

        Parameters
        ----------
        value : float
            The value to round.

        Returns
        -------
        int or float
            The rounded value.
        """

        return round(value) if self.valueRound == 0 else round(value, self.valueRound)

    def SetUpGraphValues(self):
        """
        Initialize and set up graph values including min, max, and thresholds.
        """

        self.graphValues = list(self.connGraph.GetAllValues())
        self.connGraph.allGraphValues = self.graphValues
        self.sortedGraphValues = sorted(self.graphValues, key=abs)

        nbValues = len(self.graphValues)
        self.valuesRank = {value: nbValues - rank for rank, value in enumerate(self.sortedGraphValues)}
        self.connGraph.valuesRank = self.valuesRank

        # Min / Max
        self.connGraph.minMax = (min(self.graphValues), max(self.graphValues))

        self.plotMinMax = (min(self.graphValues, key=abs), max(self.graphValues, key=abs))
        self.connGraph.plotMinMax = self.plotMinMax

        self.absMinMax = (abs(self.plotMinMax[0]), abs(self.plotMinMax[1]))
        self.connGraph.absMinMax = self.absMinMax
        
        self.threshold = self.absMinMax[0]
        difference = self.absMinMax[1] - self.absMinMax[0]

        if difference < 2:
            self.valueRound = 5
        elif difference < 5:
            self.valueRound = 4
        elif difference < 20:
            self.valueRound = 3
        elif difference < 50:
            self.valueRound = 2
        elif difference < 100:
            self.valueRound = 1
        else:
            self.valueRound = 0

    def GraphPreparation(self):
        """
        Prepare the graph and initialize UI elements related to the graph.
        """
         
        self.importFile_View.graphSection_Widget.show()

        self.DisplayInitialGraph()

        minValue = self.absMinMax[0]
        maxValue = self.absMinMax[1]

        # Set up the Spin / Slider Parameters
        factor = math.pow(10, self.valueRound)
        minValueInt = math.floor(minValue * factor)
        maxValueInt = math.floor(maxValue * factor)

        # Round Value Spin Box
        if self.valueRound == 0:
            roundMinValue = round(minValue)
        else:
            roundMinValue = round(minValue, self.valueRound) - math.pow(10, -(self.valueRound))

        roundMaxValue = round(maxValue, self.valueRound)

        self.importFile_View.threshold_Slider.setRange(minValueInt, maxValueInt)
        self.importFile_View.threshold_Slider.setTickInterval(math.floor(factor))
        self.importFile_View.threshold_Slider.setValue(minValueInt)

        minText = f"Min :<span style='font-weight: bold; text-decoration: none;'> {roundMinValue}</span>"
        self.importFile_View.minSlider_Label.setText(minText)

        maxText = f"Max :<span style='font-weight: bold; text-decoration: none;'> {roundMaxValue}</span>"
        self.importFile_View.maxSlider_Label.setText(maxText)

        self.importFile_View.thresholdValue_DoubleSpinBox.blockSignals(True)
        self.importFile_View.thresholdValue_DoubleSpinBox.setRange(roundMinValue, roundMaxValue)
        self.importFile_View.thresholdValue_DoubleSpinBox.setSingleStep(math.pow(10, -(self.valueRound)))
        self.importFile_View.thresholdValue_DoubleSpinBox.setDecimals(self.valueRound)
        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(roundMinValue)
        self.importFile_View.thresholdValue_DoubleSpinBox.blockSignals(False)

        self.PercentageTableLoading()
        self.NbTableLoading()

    def PercentageTableLoading(self):
        """
        Load and display percentage-based data in the table widget.
        """

        self.importFile_View.percentageTable_TableWidget.setRowCount(0)  # Reset Table between File
        self.importFile_View.percentageTable_TableWidget.setColumnCount(2)
        self.importFile_View.percentageTable_TableWidget.setHorizontalHeaderLabels(['Percentage', 'Corresponding\nValue'])
        self.importFile_View.percentageTable_TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # Action when Row clicked
        self.importFile_View.percentageTable_TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable Modification
        self.importFile_View.percentageTable_TableWidget.verticalHeader().setVisible(False)

        header = self.importFile_View.percentageTable_TableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        sizeValues = len(self.graphValues)
        sortedValues = sorted(self.graphValues, reverse=True, key=abs)
        absSortedValues = [abs(value) for value in sortedValues]

        # Insert Row in the Table
        percentages = [1, 10, 25, 50, 75, 90, 95]
    
        for indexPercentage, percentage in enumerate(percentages):
            self.importFile_View.percentageTable_TableWidget.insertRow(indexPercentage)
            
            itemPercent = QTableWidgetItem(f"{percentage}%")
            itemPercent.setData(Qt.UserRole, absSortedValues[math.ceil(sizeValues * (percentage / 100)) - 1])  # Graph Threshold
            itemPercent.setTextAlignment(Qt.AlignCenter)
            self.importFile_View.percentageTable_TableWidget.setItem(indexPercentage, 0, itemPercent)

            itemFmValue = absSortedValues[math.ceil(sizeValues * (percentage / 100)) - 1]
            itemFm = QTableWidgetItem(str(self.RoundInitialization(itemFmValue)))
            itemFm.setTextAlignment(Qt.AlignCenter)
            self.importFile_View.percentageTable_TableWidget.setItem(indexPercentage, 1, itemFm)

    def NbTableLoading(self):
        """
        Load and display rank-based data in the table widget.
        """

        # Fill Number Table
        self.importFile_View.nbTable_TableWidget.setRowCount(0)  # Reset Table between File
        self.importFile_View.nbTable_TableWidget.setColumnCount(2)
        self.importFile_View.nbTable_TableWidget.setHorizontalHeaderLabels(['Rank', 'Corresponding\nValue'])
        self.importFile_View.nbTable_TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # Action when Row clicked
        self.importFile_View.nbTable_TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable Modification
        self.importFile_View.nbTable_TableWidget.verticalHeader().setVisible(False)

        header = self.importFile_View.nbTable_TableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        sizeValues = len(self.graphValues)
        sortedValues = sorted(self.graphValues, reverse=True, key=abs)
        absSortedValues = [abs(value) for value in sortedValues]

        ranks = [10, 25, 50, 100, 200, 300, 400, 500]

        # Insert Row in the Table
        for indexRank, threshold in enumerate(ranks):
            if sizeValues > threshold:
                self.importFile_View.nbTable_TableWidget.insertRow(indexRank)
                
                itemNb = QTableWidgetItem(f"{threshold}th")
                itemNb.setData(Qt.UserRole, absSortedValues[threshold - 1])  # Graph Threshold
                itemNb.setTextAlignment(Qt.AlignCenter)
                self.importFile_View.nbTable_TableWidget.setItem(indexRank, 0, itemNb)

                itemFmValue = absSortedValues[threshold - 1]
                itemFm = QTableWidgetItem(str(self.RoundInitialization(itemFmValue)))
                itemFm.setTextAlignment(Qt.AlignCenter)
                self.importFile_View.nbTable_TableWidget.setItem(indexRank, 1, itemFm)

    def InformationsInitialization(self):
        """
        Initialize and display various information metrics related to the graph.
        """

        # Nb Nodes / Connections
        if not self.connGraph.numberOfNodes:
            self.importFile_View.nbNodesValue_Label.setText("...")
        else:
            self.importFile_View.nbNodesValue_Label.setText(str(self.connGraph.numberOfNodes))
        self.importFile_View.nbConnectionsValue_Label.setText(str(self.connGraph.numberOfEdges))

        # ABS Mean / ABS Sum
        if len(self.graphValues) < 2:
            self.importFile_View.meanAbsValue_Label.setText("None")
            self.importFile_View.sumAbsValue_Label.setText("None")
        else:
            meanAbs = statistics.fmean(map(abs, self.graphValues))
            sumAbs = sum(map(abs, self.graphValues))

            self.importFile_View.meanAbsValue_Label.setText(str(self.RoundInitialization(meanAbs)))
            self.importFile_View.sumAbsValue_Label.setText(str(self.RoundInitialization(sumAbs)))

        if self.valueRound == 0:
            roundMinValue = round(self.plotMinMax[0])
        else:
            roundMinValue = round(self.plotMinMax[0], self.valueRound) - math.pow(10, -(self.valueRound))

        self.importFile_View.minValue_Label.setText(str(roundMinValue))
        self.importFile_View.maxValue_Label.setText(str(self.RoundInitialization(self.plotMinMax[1])))

        # Standard Deviation
        if len(self.graphValues) < 2:
            self.importFile_View.standardDeviationValue_Label.setText("None")
        else:
            stddev = statistics.stdev(self.graphValues)
            self.importFile_View.standardDeviationValue_Label.setText(str(self.RoundInitialization(stddev)))

        # Rank
        self.rank = self.connGraph.numberOfEdges
        self.importFile_View.rankValue_Label.setText(str(self.rank))


    # =============================
    # ===== INTERFACE ACTIONS =====
    # =============================

    def UpdateOpenedDataFile(self, fileName: str):
        """
        Update the label with the name of the opened data file.

        Parameters
        ----------
        fileName : str
            The name of the opened data file.
        """

        fileName_basename = os.path.basename(fileName)
        self.importFile_View.openedDataFile_Label.setText("Opened Data File : {}".format(fileName_basename))

    def UpdateOpenedFlutFile(self, fileName: str):
        """
        Update the label with the name of the opened FLUT file.

        Parameters
        ----------
        fileName : str
            The name of the opened FLUT file.
        """

        fileName_basename = os.path.basename(fileName)
        self.importFile_View.openedFlutFile_Label.setText("Opened FLUT File : {}".format(fileName_basename))

    def UpdateOpenedFiltersFile(self, fileName: str):
        """
        Update the label with the name of the opened filters file.

        Parameters
        ----------
        fileName : str
            The name of the opened filters file.
        """

        fileName_basename = os.path.basename(fileName)
        self.importFile_View.openedFiltersFile_Label.setText("Opened Filters File : {}".format(fileName_basename))

    def UpdateOpenedNameFile(self, fileName: str):
        """
        Update the label with the name of the opened name file.

        Parameters
        ----------
        fileName : str
            The name of the opened name file.
        """

        fileName_basename = os.path.basename(fileName)
        self.importFile_View.openedNameFile_Label.setText("Opened Name File : {}".format(fileName_basename))

    def UpdatePreviousDataFiles(self, fileName: str):
        """
        Update the list of previously opened data files.

        Parameters
        ----------
        fileName : str
            The name of the data file to add to the list.
        """

        secondaryFileType = None

        # Hide or Display Name File Part if the Data File doesn't associate name with value
        if not self.connGraph.idName:
            self.DisplayImportNamePart()
            secondaryFileType = "DataFile"
        else:
            self.HideImportNamePart()
            secondaryFileType = "DataNameFile"
            self.nameFile = False  # Don't need Name File

        # Check if the File isn't already in the list
        if fileName not in self.project.previousFiles["DataFiles"]:

            if len(self.project.previousFiles["DataFiles"]) == 5:
                firstItem = self.importFile_View.previousDataFiles_List.item(0)
                del self.project.previousFiles["DataFiles"][firstItem.data(Qt.UserRole)[0]]
                self.importFile_View.previousDataFiles_List.takeItem(self.importFile_View.previousDataFiles_List.row(firstItem))

            fileName_basename = os.path.basename(fileName)
            self.project.previousFiles["DataFiles"][fileName] = secondaryFileType

            # Add the new File
            newItem = QListWidgetItem("\u21A6    ({}) {}".format(secondaryFileType, fileName_basename))
            newItem.setData(Qt.UserRole, [fileName])
            newItem.setToolTip("\u21A6 ({}) {}".format(secondaryFileType, fileName))
            self.importFile_View.previousDataFiles_List.addItem(newItem)

    def UpdatePreviousNameFiles(self, fileName: str):
        """
        Update the list of previously opened name files.

        Parameters
        ----------
        fileName : str
            The name of the name file to add to the list.
        """

        # Iterate through all items in the QListWidget
        for index in range(self.importFile_View.previousDataFiles_List.count()):

            # Get the item at the current index
            itemDataList = self.importFile_View.previousDataFiles_List.item(index)

            # Check if the item data matches the data_to_find
            if itemDataList.data(Qt.UserRole)[0] == self.dataFile:

                previousFileName_basename = os.path.basename(self.dataFile)
                fileName_basename = os.path.basename(fileName)

                itemDataList.setText("".join(["\u21A6    (Data File) ", previousFileName_basename, "\n", \
                                      "\u21AA    (Name File) ", fileName_basename]))
                itemDataList.setData(Qt.UserRole, [self.dataFile, fileName])
                itemDataList.setToolTip("".join(["\u21A6 (Data File) ", self.dataFile, "\n", \
                                                 "\u21AA (Name File) ", fileName]))

    def UpdatePreviousFlutFiles(self, fileName: str):
        """
        Update the list of previously opened FLUT files.

        Parameters
        ----------
        fileName : str
            The name of the FLUT file to add to the list.
        """

        # Check if the File isn't already in the list
        if fileName not in self.project.previousFiles["FlutFiles"]:
            if len(self.project.previousFiles["FlutFiles"]) == 5:
                firstItem = self.importFile_View.previousFlutFiles_List.item(0)
                self.project.previousFiles["FlutFiles"].remove(firstItem.data(Qt.UserRole))
                self.importFile_View.previousFlutFiles_List.takeItem(self.importFile_View.previousFlutFiles_List.row(firstItem))

            # Add the new File
            newItem = QListWidgetItem("\u21A6    {}".format(os.path.basename(fileName)))
            newItem.setData(Qt.UserRole, fileName)
            self.importFile_View.previousFlutFiles_List.addItem(newItem)
            self.project.previousFiles["FlutFiles"].append(fileName)

    def UpdatePreviousFiltersFiles(self, fileName: str):
        """
        Update the list of previously opened filters files.

        Parameters
        ----------
        fileName : str
            The name of the filters file to add to the list.
        """

        # Check if the File isn't already in the list
        if fileName not in self.project.previousFiles["FiltersFiles"]:

            if len(self.project.previousFiles["FiltersFiles"]) == 5:
                firstItem = self.importFile_View.previousFiltersFiles_List.item(0)
                self.project.previousFiles["FiltersFiles"].remove(firstItem.data(Qt.UserRole))
                self.importFile_View.previousFiltersFiles_List.takeItem(self.importFile_View.previousFiltersFiles_List.row(firstItem))

            # Add the new File
            newItem = QListWidgetItem("\u21A6    {}".format(os.path.basename(fileName)))
            newItem.setData(Qt.UserRole, fileName)
            self.importFile_View.previousFiltersFiles_List.addItem(newItem)
            self.project.previousFiles["FiltersFiles"].append(fileName)

    def DisplayImportNamePart(self):
        """
        Display the UI components related to the name file.
        """

        self.importFile_View.openedNameFile_Label.setText("No Name File Opened")
        self.importFile_View.openedNameFile_Label.show()
        self.importFile_View.importNameFile_Button.show()

    def HideImportNamePart(self):
        """
        Hide the UI components related to the name file.
        """

        self.importFile_View.openedNameFile_Label.hide()
        self.importFile_View.importNameFile_Button.hide()

    def SliderValue (self):
        """
        Update the threshold value based on the slider position.
        """

        factor = math.pow(10, self.valueRound)
        sliderValue = self.importFile_View.threshold_Slider.value() / factor

        # Return the minimal value instead of compute the logarithm value
        if sliderValue > self.absMinMax[0] and sliderValue < self.absMinMax[1]:

            # Change the value in logarithm scale
            sliderValue = self.absMinMax[0] * (self.absMinMax[1] / self.absMinMax[0]) \
                        ** (sliderValue / (self.absMinMax[1] - self.absMinMax[0]))
    
        # Re-Adjust
        if sliderValue > self.absMinMax[1]:
            sliderValue = self.absMinMax[1]
        
        # Update Value
        self.importFile_View.thresholdValue_DoubleSpinBox.blockSignals(True)
        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(sliderValue)
        self.importFile_View.thresholdValue_DoubleSpinBox.blockSignals(False)

        # Update Threshold (Filters)
        self.threshold = sliderValue

        # Update Graph
        self.UpdateGraph(sliderValue)
        self.UpdateRank(sliderValue)

    def SpinValue(self):
        """
        Update the slider position based on the spin box value.
        """

        spinValue = self.importFile_View.thresholdValue_DoubleSpinBox.value()
        logValueInversed = (self.absMinMax[1] - self.absMinMax[0]) \
                    * (math.log(spinValue / self.absMinMax[0]) / math.log(self.absMinMax[1] / self.absMinMax[0]))
        
        # Update Value
        self.importFile_View.threshold_Slider.setValue(int(logValueInversed * math.pow(10, self.valueRound)))

        # Update Threshold (Filters)
        self.threshold = spinValue

        # Update Graph
        self.UpdateGraph(spinValue)
        self.UpdateRank(spinValue)

    def UpdateRank(self, newValue: float):
        """
        Update and display the rank based on the new threshold value.

        Parameters
        ----------
        newValue : float
            The new threshold value to determine the rank.
        """

        self.rank = self.connGraph.numberOfEdges
        for value in self.sortedGraphValues:
            if abs(newValue) <= abs(value):
                break

            self.rank -= 1

        # Display the rank associate to the newValue
        self.importFile_View.rankValue_Label.setText(str(self.rank))

    def TablePercentageValue(self, item: QTableWidgetItem):
        """
        Update the threshold value based on the selected percentage table item.

        Parameters
        ----------
        item : QTableWidgetItem
            The item in the percentage table whose value is used to update the threshold.
        """

        self.importFile_View.nbTable_TableWidget.clearSelection()
        row = item.row()

        # Update Threshold (Filters)
        percentageValue = float(self.importFile_View.percentageTable_TableWidget.item(row, 0).data(Qt.UserRole))
        self.threshold = percentageValue

        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(percentageValue)

        # Update Graph
        self.UpdateGraph(percentageValue)

    def TableNbValue(self, item: QTableWidgetItem):
        """
        Update the threshold value based on the selected number table item.

        Parameters
        ----------
        item : QTableWidgetItem
            The item in the number table whose value is used to update the threshold.
        """

        self.importFile_View.percentageTable_TableWidget.clearSelection()
        row = item.row()

        # Update Threshold (Filters)
        nbValue = float(self.importFile_View.nbTable_TableWidget.item(row, 0).data(Qt.UserRole))
        
        self.threshold = nbValue

        self.importFile_View.thresholdValue_DoubleSpinBox.setValue(nbValue)
        
        # Update Graph 
        self.UpdateGraph(nbValue)


    # ==================================
    # ===== Graph Display / Update =====
    # ==================================

    def DisplayInitialGraph(self):
        """
        Display the initial graph with sorted values and annotations for min and max values.
        
        Clears the previous plot, creates a new one, sorts and plots the values, 
        sets the y-axis to a logarithmic scale, adds title and labels, and 
        annotates the min and max values outside the plot area.
        """

        # Clear the previous plot and Create a new one
        self.importFile_View.graph.clear()
        self.graph = self.importFile_View.graph.add_subplot(111)

        # Sort Values -> Initial value
        positiveValues = [value for value in self.graphValues if value > 0]
        negativeValues = [value for value in self.graphValues if value < 0]

        sortedValues = sorted(negativeValues, reverse=True) + sorted(positiveValues, reverse=True)

        x_coords = list(range(len(sortedValues)))
        y_coords = [abs(val) for val in sortedValues]

        self.graph.plot(x_coords, y_coords, label='Initial Curve')

        # Limited plot (initially empty)
        self.limitedCurve, = self.graph.plot(x_coords, y_coords, label='Limited Curve')

        # Set the y-axis to logarithmic scale
        self.graph.set_yscale('log')

        # Add title and labels
        self.graph.set_title('Connectivities Representative Curves\n(in absolute values)', fontsize=15)
        self.graph.set_ylabel('Absolute Value', fontsize=15)

        # Remove x-tick labels
        self.graph.set_xticks([])
        self.graph.set_xticklabels([])

        self.graph.tick_params(axis='y', which='major', labelsize=10)
        self.graph.legend(fontsize=15)

        minValue = self.absMinMax[0]
        maxValue = self.absMinMax[1]

        # Add min and max value annotations outside the plot area
        if type(minValue) == int:
            roundMinValue = minValue
        else:
            roundMinValue = round(minValue, self.valueRound) - math.pow(10, -(self.valueRound))

        roundMaxValue = round(maxValue, self.valueRound)

        # Add min and max value outside the plot area with a white background
        self.graph.text(
            -0.1, -0.05,  # Position near the bottom of the plot
            f'Min: {roundMinValue}', 
            fontsize=9, color='black',
            verticalalignment='bottom', 
            horizontalalignment='left',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
            transform=self.graph.transAxes
        )

        self.graph.text(
            -0.1, 1.05,
            f'Max: {roundMaxValue}', 
            fontsize=9, color='black',
            verticalalignment='top', 
            horizontalalignment='left',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
            transform=self.graph.transAxes
        )

        # Draw the canvas
        self.importFile_View.canvas.draw()

    def UpdateGraph(self, newValue: float):
        """
        Update the graph with the new threshold value, adjusting the displayed curve 
        based on the current threshold.

        Parameters
        ----------
        newValue : float
            The new threshold value used to filter and update the displayed curve.
        """
        
        # Update the limited curve data
        positiveValuesLimited = [value for value in self.graphValues if value > 0]
        negativeValuesLimited = [value for value in self.graphValues if value < 0]

        sortedValuesLimited = sorted(negativeValuesLimited, reverse=True) + sorted(positiveValuesLimited, reverse=True)

        x_coordsLimited = list(range(len(sortedValuesLimited)))
        y_coordsLimited = [abs(value) if abs(value) > newValue - math.pow(10, -(self.valueRound)) 
                            else None for value in sortedValuesLimited]

        # If only one point selected -> display a point 
        if y_coordsLimited.count(None) == len(y_coordsLimited) - 1:
            self.limitedCurve.set_data(x_coordsLimited, y_coordsLimited)
            self.limitedCurve.set_marker('o')
            self.limitedCurve.set_markersize(4)

        else:
            self.limitedCurve.set_data(x_coordsLimited, y_coordsLimited)
            self.limitedCurve.set_marker('')

        # Update the canvas
        self.graph.relim()
        self.graph.autoscale_view()
        self.importFile_View.canvas.draw()

    # =============================
    # ===== INTERFACE CLOSING =====
    # =============================

    def CloseImportWithoutValidation(self):
        """
        Close the import process without validating changes, resetting filters, 
        connection graph, and project to their saved states.
        """

        if not self.validation:

            # ===== Reset Filters =====
            self.filters.LoadSaveFilters(self.filtersSave.RecovertFiltersSave())

            # ===== Reset Conn Graph =====
            self.connGraph.LoadSaveConnGraph(self.connGraphSave.RecovertConnGraphSave())

            # ===== Reset Project
            self.project.InitRestore(self.projectSave)