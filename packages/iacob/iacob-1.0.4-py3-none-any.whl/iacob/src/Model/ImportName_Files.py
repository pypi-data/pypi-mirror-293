import os

from src.Model.Data_Storage.ConnGraph_Model import ConnGraph_Infos

class ParserName_Files:
    """
    A class to parse Name Files
    """
    def __init__(self):
        
        # File Part
        self.fileName = None
        self.connGraph = ConnGraph_Infos()
        
        self.allLines = None

        self.idName = {}  # {ID_Node: Name}


    def LoadFile(self):
        """
        Load the content of the file specified by `self.fileName`.
        
        Opens and reads the file. Raises an exception if the file cannot be found or is empty.

        Raises
        ------
        Exception
            If the file cannot be found or the file format is incorrect.
        """

        # Load the graph from the given file
        try:
            nameFile = open(os.path.abspath(self.fileName), 'r')
        except FileNotFoundError:
            raise Exception("Opening Error - {}".format(self.fileName))
        
        self.allLines = nameFile.readlines()

        # Handle Empty File
        if len(self.allLines) == 0:
            nameFile.close()
            raise Exception("Wrong Format Error - Empty Given File")
        
        nameFile.close()

    def OneLine_Parser(self):
        """
        Parse the file if it contains a single line with names separated by spaces.
        
        Maps each name to an arbitrary ID.
        """

        indexName = 0

        # Stock all Name with an abitratry ID
        for name in self.allLines[0].split():

            self.idName[indexName] = name
            indexName += 1

    def OneColumn_Parser(self):
        """
        Parse the file if it contains multiple lines, each with a single name.
        
        Maps each name to an arbitrary ID.
        """

        indexName = 0

        # Stock all Name with an abitratry ID
        for line in self.allLines:

            lineSplit = line.split()

            if lineSplit != []:
                self.idName[indexName] = "".join(lineSplit)
                indexName += 1

    def NameFile_Parser(self, fileName: str):
        """
        Parse the name file based on its format and update the ConnGraph_Infos object.
        
        Parameters
        ----------
        fileName : str
            The path to the name file to be parsed.
        
        Raises
        ------
        Exception
            If the file extension is not '.txt'.
        """

        self.fileName = fileName
        
        # Recovert and verify the file extension
        extension = os.path.splitext(self.fileName)[1]

        if extension != ".txt":
            raise Exception("Wrong Extension Error - Extension not allowed")

        # Load and Recovert All Lines from the File
        print("\u27A2 Loading Name File")
        self.LoadFile()
        
        if len(self.allLines) == 1:
            self.OneLine_Parser()
        else:
            self.OneColumn_Parser()        

        # Complete the ConnGraph Object
        self.connGraph.idName = self.idName