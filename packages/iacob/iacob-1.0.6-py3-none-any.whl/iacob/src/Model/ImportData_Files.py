import os
import math
import numpy as np

from scipy.io import loadmat

from src.Model.Data_Storage.ConnGraph_Model import ConnGraph_Infos

class ParserData_Files:
    """
    A class to parser Data Files
    """

    connGraph: ConnGraph_Infos

    def __init__(self):

        # File Part
        self.fileName = None
        self.fileType = None  # File Type (.mat / .txt / .flut)
        self.allLines = None

        self.idName = {}  # {ID_Node: Name} -> Matrix Files
        self.edgesValues = {}  # {ID_Node: {ID_Next: Value}}
        self.edgesValues_withoutDuplicata = {}

        self.numberOfNodesInData = 0
        self.numberOfEdges = 0

        # Graph Part
        self.connGraph = ConnGraph_Infos()


    # ==================================
    # ===== Parser Seperation Part =====
    # ==================================

    def LoadFile(self):
        """
        Load and process the file based on its extension.
        
        Raises
        ------
        ValueError
            If the file extension is not supported (.txt or .mat).
        FileNotFoundError
            If the file specified by `fileName` cannot be found.
        """

        # Recovert and verify the file extension
        extension = os.path.splitext(self.fileName)[1]

        if extension not in ['.txt', '.mat']:
            raise Exception("Wrong Extension Error - Extension not allowed")

        # Load the graph from the given file
        try:
            dataFile = open(os.path.abspath(self.fileName), 'r')
        except FileNotFoundError:
            raise Exception("Opening Error - {}".format(self.fileName))

        match extension:
            case '.txt':
                self.ReadTXT(dataFile)

            case '.mat':
                dataFile.close()
                self.fileType = "MatLab File"
                self.ReadMAT()

        dataFile.close()

    def ReadTXT(self, dataFile):
        """
        Read and parse a .txt file.
        
        Parameters
        ----------
        dataFile : file object
            The opened .txt file to read from.
        
        Raises
        ------
        ValueError
            If the file format is incorrect or contains unexpected data.
        """

        self.allLines = dataFile.readlines()

        # Recovert Line / Column Number
        linesNumber = len(self.allLines)

        # Handle Empty File Exception
        if linesNumber == 0:
            dataFile.close()
            raise Exception("Wrong Format Error - Empty Given File")

        columnsNumber = len(self.allLines[0].split())

        try:
            # Determine the File Type
            if linesNumber == 1:
                self.fileType = "Single Line - TXT File"
                self.SingleLineFile_Parser()

            else:
                if columnsNumber == 3:

                    self.fileType = "Triplet - TXT File"
                    self.TripletFile_Parser()

                else:
                    self.fileType = "Matrix - TXT File"
                    self.MatrixFile_Parser()

        except Exception as exception:
            dataFile.close()
            raise Exception(exception.args[0])

    def ReadMAT(self):
        """
        Read and parse a .mat file.
        
        Raises
        ------
        KeyError
            If required variables are missing in the .mat file.
        """

        try:
            # Load MatLab File
            loadMatLabFile = loadmat(self.fileName)

            # Name List Parsing
            if "name" in loadMatLabFile:
                self.MatLabNameList_Parser(loadMatLabFile["name"][0])

            # Data Matrix Parsing
            for variableValue in loadMatLabFile.values():
                
                if isinstance(variableValue, np.ndarray):
                    if variableValue.shape[0] == variableValue.shape[1] and len(variableValue.shape) == 2:
                        self.allLines = variableValue

            self.MatLabConnectivityMatrix_Parser()

        except KeyError:
            raise Exception("Wrong Format Error - Variable Connectivity Inexistance")

    # ----- Update Graph -----

    def AddEdgeInGraph (self, idCurrent, idNext, edgeValue):
        """
        Add an edge to the graph and update node counts.
        
        Parameters
        ----------
        idCurrent : int
            The ID of the current node.
        idNext : int
            The ID of the next node.
        edgeValue : float
            The value of the edge connecting the two nodes.
        """

        # If it is the first appearance of the node 
        if idCurrent not in self.edgesValues:
            self.edgesValues[idCurrent] = {}
            self.numberOfNodesInData += 1

        if idNext not in self.edgesValues:
            self.edgesValues[idNext] = {}
            self.numberOfNodesInData += 1

        self.edgesValues[idCurrent][idNext] = edgeValue
        self.edgesValues[idNext][idCurrent] = edgeValue

        self.edgesValues_withoutDuplicata[(idCurrent, idNext)] = edgeValue


    # ===================
    # ===== Parsers =====
    # ===================

    # ----- TXT Parsers -----

    def SingleLineFile_Parser(self):
        """
        Parse a single-line .txt file.
        
        Raises
        ------
        ValueError
            If the line format is incorrect or contains unexpected data.
        """

        print("\u27A2 Loading Single Line - TXT file")

        lineSplit = self.allLines[0].split()
        
        if lineSplit % 3 != 0:
            raise Exception("Wrong Format - Not only Triple")

        index = 2
        while index < len(lineSplit):

            idCurrent = int(index)
            idNext = int(index + 1)

            try:
                edgeValue = float(index + 2)
                if edgeValue.is_integer():
                    edgeValue = math.floor(edgeValue)

            except ValueError:
                raise Exception("Wrong Data Type - Need to be Int/Float")

            self.AddEdgeInGraph(idCurrent, idNext, edgeValue)

            index += 3

    def MatrixFile_Parser(self):
        """
        Parse a matrix file format .txt.
        
        Raises
        ------
        ValueError
            If the file format is incorrect, contains unexpected data, or has mismatched line lengths.
        """

        print("\u27A2 Loading Matrix - TXT file")

        firstLine = self.allLines[0].split()
        skipLine = firstLine.count("data")

        # In the case of matrix with ID/Name
        if skipLine != 0:

            namesLine = None
            lengthLine = len(firstLine) - skipLine
            for infosLine in self.allLines[:skipLine]:  # Recovert the n lines that provide informations
                infosLine = infosLine.split()[skipLine:]

                # Handle Exception (different lenght of lines)
                if len(infosLine) != lengthLine:
                    raise Exception("Wrong Format - Different lenght of lines")
                
                # Check element of the line
                isNamesLine = False
                for element in infosLine:
                    try:
                        float(element)
                    except ValueError:
                        isNamesLine = True
                        break
                
                # Recovert the names Line
                if isNamesLine:
                    namesLine = infosLine
            
            # Associate ID (manually) with Name area (if it exist a names Line)
            if not namesLine:
                namesLine = firstLine[skipLine:]
                print("No string Name Find - Taking Integer/Float as Name")

            for indexName, name in enumerate(namesLine):
                self.idName[indexName] = name

        else:
            lengthLine = len(firstLine)

        # Assign manual ID to each area
        idLines = [indexLine for indexLine in range(lengthLine)]

        # For each (other) line in the File
        for indexLine, line in enumerate(self.allLines[skipLine:]):

            lineSplit = line.split()[skipLine:]

            # Handle Exception (different lenght of lines)
            if len(lineSplit) != lengthLine:
                raise Exception("Wrong Format - Different lenght of lines")

            for indexElement, element in enumerate(lineSplit[:indexLine]):
                
                try:
                    # If the connectivity value isn't NULL
                    if float(element) == 0.0:
                        continue

                except ValueError:
                    raise Exception("Wrong Data Type - Need to be Int/Float")

                idCurrent = int(idLines[indexLine])
                idNext = int(idLines[indexElement])

                edgeValue = float(element)
                if edgeValue.is_integer():
                    edgeValue = math.floor(edgeValue)

                self.AddEdgeInGraph(idCurrent, idNext, edgeValue)

        self.numberOfNodesInData = lengthLine

    def TripletFile_Parser(self):
        """
        Parse a triplet file format .txt.
        
        Raises
        ------
        ValueError
            If the line format is incorrect or contains unexpected data.
        """

        print("\u27A2 Loading Triplet - TXT file")

        # For each line in the File
        for indexLine, line in enumerate(self.allLines):

            lineSplit = line.split()

            if len(lineSplit) != 3:
                raise Exception("Wrong Format - Line {}".format(indexLine))

            idCurrent = int(lineSplit[0])
            idNext = int(lineSplit[1])

            try:
                edgeValue = float(lineSplit[2])
                if edgeValue.is_integer():
                    edgeValue = math.floor(edgeValue)

            except ValueError:
                    raise Exception("Wrong Data Type - Need to be Int/Float")

            self.AddEdgeInGraph(idCurrent, idNext, edgeValue)

    # ----- MatLab Parser -----

    def MatLabConnectivityMatrix_Parser(self):
        """
        Parse a MATLAB connectivity matrix.
        
        Raises
        ------
        ValueError
            If the matrix format is incorrect or contains unexpected data.
        """

        lengthLine = len(self.allLines[0]) 

        # Assign manual ID to each area
        idLines = [indexLine for indexLine in range(lengthLine)]

        # For each (other) line in the File
        for indexLine, line in enumerate(self.allLines):
            for indexElement, element in enumerate(line[:indexLine]):

                try:
                    # If the connectivity value isn't NULL
                    if float(element) == 0.0 or np.isnan(element):
                        continue

                except ValueError:
                    raise Exception("Wrong Data Type - Need to be Int/Float")
                
                idCurrent = int(idLines[indexLine])
                idNext = int(idLines[indexElement])
                
                edgeValue = float(element)
                if edgeValue.is_integer():
                    edgeValue = math.floor(edgeValue)

                self.AddEdgeInGraph(idCurrent, idNext, edgeValue)

        self.numberOfNodesInData = lengthLine

    def MatLabNameList_Parser(self, nameList: list):
        """
        Parse a list of names from a MATLAB file.
        
        Parameters
        ----------
        nameList : list
            List of ASCII values representing names.
        
        Raises
        ------
        ValueError
            If the name list contains invalid data.
        """

        currentIndex = 0
        name = ''

        # Using chr() Method
        for value in nameList:
            if value == 10:  # Value 10 is the end of the name

                # Don't add empty Name
                if name != '':
                    self.idName[currentIndex] = str(name)
                    currentIndex += 1
                    name = ''

                continue

            name = name + chr(value)

    # --------------------------
    
    def GraphCreation(self, FileName: str):
        """
        Create a connectivity graph from a file.
        
        Parameters
        ----------
        FileName : str
            The name of the file to parse.
        """

        self.fileName = FileName

        print("\u27A2 Loading Connectivity Graph")

        # Load the File -> generate Arcs Dictionary
        self.LoadFile()

        print("\u27A2 Loading Connectivity Graph Done")

        # Complete the ConnGraph Object 
        self.connGraph.edgesValues = self.edgesValues
        self.connGraph.numberOfNodesInData = self.numberOfNodesInData
        self.connGraph.edgesValues_withoutDuplicata = self.edgesValues_withoutDuplicata
        self.connGraph.numberOfEdges = len(self.edgesValues_withoutDuplicata)

        # Can be Completed or Empty
        self.connGraph.idName = self.idName

