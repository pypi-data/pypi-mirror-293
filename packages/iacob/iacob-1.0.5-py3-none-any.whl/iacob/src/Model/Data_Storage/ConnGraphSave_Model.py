from copy import deepcopy

class ConnGraphSave_Infos():
    """
    A class to store a current state of the Singleton ConnGraph_Model class
    """
    
    def __init__(self):
        """
        Initialize the ConnGraphSave_Infos class with default values and structures 
        for storing graph information.
        """

        self.nxGraph = None
        self.dictGraph = None

        self.allGraphValues = []

        self.idName = {}  # Link between ID and Name of each area -> {ID_Node: Name}
        self.areaInfos = {}  # Area Informations
                             # {Name: {ID, RGBA, Side, MajorRegion, ID_Opposite, 3D_Coos}} -> FLUT File
        self.areasOrder = []  # Order of areas (with blanks)
        self.colorMajorRegions = {}
        self.numberOfNodes = None
        
        self.valuesRank = {}
        self.numberOfNodesInData = None
        self.edgesValues = {}  # Value of each edge in the graph -> {ID_Node: {ID_Next: Value}}
        self.edgesValuesFiltered = {}
        self.edgesValues_withoutDuplicata = {}
        self.edgesTypeConnexion = {}  # Connexion Type -> ID_Node: {ID_Next: Value}
                                      # Value in ("Contralateral", "Homotopic", "Ipsilateral", "Other")
        self.edgesTypeConnexionFiltered = {}
        self.numberOfEdges = 0

        self.minMax = None
        self.plotMinMax = None
        self.absMinMax = None

        self.adjacencyMatrix = []

    def RecovertConnGraphSave(self):
        """
        Create a deep copy of the save of the graph information and return it as a dictionary.

        Returns
        -------
        dict
            A dictionary containing deep copies of all the graph attributes.
        """

        return {
            "nxGraph": deepcopy(self.nxGraph),
            "dictGraph": deepcopy(self.dictGraph),

            "allGraphValues": deepcopy(self.allGraphValues),
            "idName": deepcopy(self.idName),
            "areaInfos": deepcopy(self.areaInfos),
            "areasOrder": deepcopy(self.areasOrder),
            "colorMajorRegions": deepcopy(self.colorMajorRegions),

            "valuesRank": deepcopy(self.valuesRank),
            "edgesValues": deepcopy(self.edgesValues),
            "edgesValues_withoutDuplicata": deepcopy(self.edgesValues_withoutDuplicata),
            "edgesTypeConnexion": deepcopy(self.edgesTypeConnexion),

            "minMax": deepcopy(self.minMax),
            "plotMinMax": deepcopy(self.plotMinMax),
            "absMinMax": deepcopy(self.absMinMax),

            "numberOfNodes": self.numberOfNodes,
            "numberOfEdges": self.numberOfEdges,
            "adjacencyMatrix": deepcopy(self.adjacencyMatrix)
        }

    def LoadCurrentConnGraph(self, connGraphCurrent: dict):
        """
        Load the graph information from a given dictionary provided from the current instance.

        Parameters
        ----------
        connGraphCurrent : dict
            A dictionary containing the graph attributes to be loaded from the current instance.
        """

        self.nxGraph = connGraphCurrent["nxGraph"]
        self.dictGraph = connGraphCurrent["dictGraph"]

        self.allGraphValues = connGraphCurrent["allGraphValues"]
        self.idName = connGraphCurrent["idName"]
        self.areaInfos = connGraphCurrent["areaInfos"]
        self.areasOrder = connGraphCurrent["areasOrder"]
        self.colorMajorRegions = connGraphCurrent["colorMajorRegions"]

        self.valuesRank = connGraphCurrent["valuesRank"]
        self.edgesValues = connGraphCurrent["edgesValues"]
        self.edgesValues_withoutDuplicata = connGraphCurrent["edgesValues_withoutDuplicata"]
        self.edgesTypeConnexion = connGraphCurrent["edgesTypeConnexion"]

        self.minMax = connGraphCurrent["minMax"]
        self.plotMinMax = connGraphCurrent["plotMinMax"]
        self.absMinMax = connGraphCurrent["absMinMax"]

        self.numberOfNodes = connGraphCurrent["numberOfNodes"]
        self.numberOfEdges = connGraphCurrent["numberOfEdges"]
        self.adjacencyMatrix = connGraphCurrent["adjacencyMatrix"]