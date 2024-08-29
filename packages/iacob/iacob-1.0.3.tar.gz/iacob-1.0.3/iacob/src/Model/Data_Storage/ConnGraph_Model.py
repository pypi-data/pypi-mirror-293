from copy import deepcopy
import networkx as nx

from src.Model.Data_Storage.Filters_Model import Filters_Infos
from src.Model.Data_Storage.DataSingleton_Model import DataSingleton

class ConnGraph_Infos(metaclass=DataSingleton):
    """
    A class to manage and store information about connectivity graphs

        - Saving & Loading Data
        - Compute Filtering Data
        - Compute graph-theoretic measures
    """
    
    def __init__(self):

        self.filters = Filters_Infos()
        self.InitReset()

    # ===================================
    # ===== Init / Reset Graph Data =====
    # ===================================

    def InitReset(self):
        """
        Reset or initialize the graph data to their default states.
        """

        self.nxGraph = None
        self.nxGraphBinary = None
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

    def SaveCurrentConnGraph(self):
        """
        Save the current state of the connectivity graph.

        Returns
        -------
        dict
            A dictionary containing deep copies of the current graph data.
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

    def LoadSaveConnGraph(self, connGraphSave: dict):
        """
        Load a previously saved connectivity graph state.

        Parameters
        ----------
        connGraphSave : dict
            A dictionary containing saved graph data.
        """

        self.nxGraph = connGraphSave["nxGraph"]
        self.dictGraph = connGraphSave["dictGraph"]

        self.allGraphValues = connGraphSave["allGraphValues"]
        self.idName = connGraphSave["idName"]
        self.areaInfos = connGraphSave["areaInfos"]
        self.areasOrder = connGraphSave["areasOrder"]
        self.colorMajorRegions = connGraphSave["colorMajorRegions"]

        self.valuesRank = connGraphSave["valuesRank"]
        self.edgesValues = connGraphSave["edgesValues"]
        self.edgesValues_withoutDuplicata = connGraphSave["edgesValues_withoutDuplicata"]
        self.edgesTypeConnexion = connGraphSave["edgesTypeConnexion"]

        self.minMax = connGraphSave["minMax"]
        self.plotMinMax = connGraphSave["plotMinMax"]
        self.absMinMax = connGraphSave["absMinMax"]

        self.numberOfNodes = connGraphSave["numberOfNodes"]
        self.numberOfEdges = connGraphSave["numberOfEdges"]
        self.adjacencyMatrix = connGraphSave["adjacencyMatrix"]

        # If the filters isn't totally initialize -> not SetEdgesValuesFiltered
        if self.filters.discardInterRegConn:
            self.SetEdgesValuesFiltered()
    

    # ========================
    # ===== Set Variable =====
    # ========================

    def SetGraph(self, nxGraph: nx.Graph):
        """
        Set the networkx graph object and update the internal dictionary representation.

        Parameters
        ----------
        nxGraph : nx.Graph
            The networkx graph object to be set.
        """

        self.nxGraph = nxGraph
        self.dictGraph = nx.to_dict_of_dicts(self.nxGraph)

        if nx.empty_graph(self.nxGraph):
            self.adjacencyMatrix = nx.adjacency_matrix(self.nxGraph).todense()

    def SetTypeConnexion(self):
        """
        Set the type of connections (Ipsilateral, Contralateral, Homotopic, Other) 
        for all edges in the graph based on the area information.
        """

        for edge_source, edgesDestValue in self.edgesValues.items():

            name_source = self.idName[edge_source]
            if edge_source not in self.edgesTypeConnexion:
                self.edgesTypeConnexion[edge_source] = {}

            for edge_dest in edgesDestValue.keys():

                name_dest = self.idName[edge_dest]

                # Ipsilateral Connexion
                if self.areaInfos[name_source]["Side"] == self.areaInfos[name_dest]["Side"]:
                    self.edgesTypeConnexion[edge_source][edge_dest] = "Ipsilateral"

                elif self.areaInfos[name_source]["Side"] != self.areaInfos[name_dest]["Side"]:

                    # 2 -> 0 or 0 -> 2 => Other Connexion
                    if self.areaInfos[name_source]["Side"] == 0 or self.areaInfos[name_dest]["Side"] == 0:
                        self.edgesTypeConnexion[edge_source][edge_dest] = "Other"

                    # Contralateral or Homotopic Connexion
                    else:
                        if self.areaInfos[name_source]["ID_Opposite"] == self.areaInfos[name_dest]["ID"]:
                            self.edgesTypeConnexion[edge_source][edge_dest] = "Homotopic"
                        else:
                            self.edgesTypeConnexion[edge_source][edge_dest] = "Contralateral"


    # ========================
    # ===== Get Variable =====
    # ========================

    def GetAllValues(self):
        """
        Return a list of all edge weights in the graph.

        Returns
        -------
        list
            A list of edge weights.
        """

        return list(self.edgesValues_withoutDuplicata.values())

    def GetAllAbsValues(self):
        """
        Return a list of all absolute edge weights in the graph.

        Returns
        -------
        list
            A list of absolute edge weights.
        """

        return [abs(value) for value in list(self.edgesValues_withoutDuplicata.values())]

    def GetRegionNameWithID(self, ID: int):
        """
        Return the name corresponding to a given region ID.

        Parameters
        ----------
        ID : int
            The ID of the region.

        Returns
        -------
        str
            The name of the region.
        """

        return self.idName[ID]

    def GetRegionIDWithName(self, name: str):
        """
        Return the ID corresponding to a given region name.

        Parameters
        ----------
        name : str
            The name of the region.

        Returns
        -------
        int or None
            The ID of the region, or None if not found.
        """

        for regionID, regionName in self.idName.items():
            if regionName == name:
                return regionID
        return None

    def GetAreasInWiderArea(self, widerAreaName : str):
        """
        Return a list of areas within a specified wider area (MajorRegion).

        Parameters
        ----------
        widerAreaName : str
            The name of the wider area (MajorRegion).

        Returns
        -------
        list
            A list of area names within the specified wider area.
        """

        areas = []
        for areaName, areaDetails in self.areaInfos.items():
            if widerAreaName == areaDetails["MajorRegion"]:
                areas.append(areaName)

        return areas

    def GetAllInterRegionalName(self):
        """
        Return a list of all inter-regional names (MajorRegions) present in the graph.

        Returns
        -------
        list
            A list of unique inter-regional names.
        """

        interRegionalNames = []
        for _, info in self.areaInfos.items():
            name = info["MajorRegion"]
            if name not in interRegionalNames :
                interRegionalNames.append(name)


        return interRegionalNames

    # ==============================
    # ===== Filtered Variables =====
    # ==============================
    
    def SetEdgesValuesFiltered(self):
        """
        Apply filters to the edges and update edgesValuesFiltered and edgesTypeConnexionFiltered.
        """

        self.edgesValuesFiltered = {}
        self.edgesTypeConnexionFiltered = {}
        
        if self.nxGraph:
            self.nxGraph.remove_edges_from(list(self.nxGraph.edges))

        # Sort element respecting filters
        for idEdge_source, destValue in self.edgesValues.items():

            nameEdge_source = self.GetRegionNameWithID(idEdge_source)
            for idEdge_dest, valueEdge in destValue.items():

                # ----- Sorted with the Weight / Rank -----

                # Relative Weight
                if self.filters.discardWeight:
                    if valueEdge < self.filters.weightBetween_threshold[0] or \
                        valueEdge > self.filters.weightBetween_threshold[1]:
                        continue
                
                # Absolute Weight
                elif self.filters.discardAbsWeight:
                    if abs(valueEdge) < self.filters.absWeightBetween_threshold[0] or \
                        abs(valueEdge) > self.filters.absWeightBetween_threshold[1]:
                        continue

                # Rank
                elif self.filters.discardRank:
                    if self.valuesRank[valueEdge] < self.filters.rankBetween_threshold[0] or \
                        self.valuesRank[valueEdge] > self.filters.rankBetween_threshold[1]:
                        continue

                nameEdge_dest = self.GetRegionNameWithID(idEdge_dest)

                # Sorted with Major Regions
                majorRegion_source = self.areaInfos[nameEdge_source]["MajorRegion"]
                majorRegion_dest = self.areaInfos[nameEdge_dest]["MajorRegion"]

                if not self.filters.discardInterRegConn[(majorRegion_source, majorRegion_dest)]:
                    continue

                # Sorted with Connection Type
                connType_sourceDest = self.edgesTypeConnexion[idEdge_source][idEdge_dest]

                if not self.filters.contralateral_connType:
                    if connType_sourceDest == "Contralateral":
                        continue

                if not self.filters.homotopic_connType:
                    if connType_sourceDest == "Homotopic":
                        continue
                
                if not self.filters.ipsilateral_connType:
                    if connType_sourceDest == "Ipsilateral":
                        continue

                if not self.filters.other_connType:
                    if connType_sourceDest == "Other":
                        continue

                # Initializes the dictionnary
                if idEdge_source not in self.edgesValuesFiltered:
                    self.edgesValuesFiltered[idEdge_source] = {} 
                    self.edgesTypeConnexionFiltered[idEdge_source] = {} 

                # Update Variables
                self.edgesValuesFiltered[idEdge_source][idEdge_dest] = valueEdge
                self.edgesTypeConnexionFiltered[idEdge_source][idEdge_dest] = connType_sourceDest
                self.nxGraph.add_weighted_edges_from([(nameEdge_source, nameEdge_dest, abs(valueEdge))])

    # =========================================
    # ===== Method with by MainController =====
    # =========================================

    # ----- List Part -----

    def GetEdgesDetails_List(self):
        """
        Get a list of detailed information for each edge in the filtered graph.

        Returns
        -------
        list
            A list of lists, where each inner list contains details for an edge, including:
            - Source node ID
            - Destination node ID
            - Source region name
            - Destination region name
            - Source major region
            - Destination major region
            - Type of connection
            - Edge weight
            - Edge rank
        """

        edgesDetails = []

        for edge_source, nextEdgeValues in self.edgesValuesFiltered.items():
            for edge_dest, value in nextEdgeValues.items():

                area_1 = self.GetRegionNameWithID(edge_source)
                area_2 = self.GetRegionNameWithID(edge_dest)

                region_1 = self.areaInfos[area_1]["MajorRegion"]
                region_2 = self.areaInfos[area_2]["MajorRegion"]

                connectionType = self.edgesTypeConnexion[edge_source][edge_dest]

                rank = self.valuesRank[value]

                details = [edge_source, edge_dest, area_1, area_2, region_1, region_2, connectionType, value, rank]

                edgesDetails.append(details)

        return edgesDetails


    # ----- Pie Chart Part -----    

    def GetAllNameWithConnectivity_PieChart(self):
        """
        Get a list of region names that have connectivity in the filtered graph.

        Returns
        -------
        list
            A list of region names.
        """

        namesWithConnectivity = []
        for id in self.edgesValuesFiltered.keys():
            namesWithConnectivity.append(self.GetRegionNameWithID(id))

        return namesWithConnectivity

    def GetAllConnectivityWithName_PieChart(self, name: str):
        """
        Get a dictionary of connected regions with their connectivity values and colors for a specific region.

        Parameters
        ----------
        name : str
            The name of the region to check connectivity for.

        Returns
        -------
        dict
            A dictionary where the keys are connected region names, and the values are tuples containing
            the absolute connectivity value and the region's RGBA color.
        """

        id_name = self.GetRegionIDWithName(name)

        connectivities = {}
        for edge_dest, value in self.edgesValuesFiltered[id_name].items():
            nextName = self.GetRegionNameWithID(edge_dest)
            connectivities[nextName] = (abs(value), self.areaInfos[nextName]["RGBA"])

        return connectivities

    def GetAllMajorRegionsWithName_PieChart(self, name: str):
        """
        Get a dictionary of major regions with their total connectivity values for a specific region.

        Parameters
        ----------
        name : str
            The name of the region to check major region connectivity for.

        Returns
        -------
        dict
            A dictionary where the keys are major region names, and the values are the total connectivity values.
        """

        id_name = self.GetRegionIDWithName(name)

        majorRegions = {}
        for edge_dest, edge_value in self.edgesValuesFiltered[id_name].items():

            majorRegion = self.areaInfos[self.GetRegionNameWithID(edge_dest)]["MajorRegion"]
            if majorRegion not in majorRegions:
                majorRegions[majorRegion] = 0.0

            majorRegions[majorRegion] += abs(edge_value)

        return majorRegions

    def GetAllConnectionTypeWithName_PieChart(self, name: str):
        """
        Get a dictionary of connection types with their total values for a specific region.

        Parameters
        ----------
        name : str
            The name of the region to check connection types for.

        Returns
        -------
        dict
            A dictionary where the keys are connection types (Ipsilateral, Contralateral, Homotopic, Other),
            and the values are the total connectivity values for each type.
        """

        id_name = self.GetRegionIDWithName(name)

        connectionsType = {"Ipsilateral": 0.0, "Contralateral": 0.0, "Homotopic": 0.0, "Other": 0.0}
        for edge_dest, connectionType in self.edgesTypeConnexionFiltered[id_name].items():
            connectionsType[connectionType] += abs(self.edgesValues[id_name][edge_dest])

        return connectionsType


    # ----- GT Measures -----

    def local_efficiency(self, graph):
        """
        Calculate the local efficiency for each node in the graph.

        Parameters
        ----------
        graph : nx.Graph
            The graph for which to calculate local efficiency.

        Returns
        -------
        dict
            A dictionary where the keys are node IDs, and the values are their local efficiency values.
        """
        efficiency = {}

        for node in graph.nodes():
            # Determine the neighbors
            neighbors = list(graph.neighbors(node))

            if len(neighbors) < 2:
                efficiency[node] = 0
            else:
                # Create the subgraph of neighbors
                subgraph = graph.subgraph(neighbors)
                
                # Ensure the subgraph is connected before calculating global efficiency
                if nx.is_connected(subgraph):
                    efficiency[node] = nx.global_efficiency(subgraph)
                else:
                    # Calculate efficiency for each connected component
                    component_efficiencies = []
                    for component in nx.connected_components(subgraph):
                        component_subgraph = subgraph.subgraph(component)
                        component_efficiencies.append(nx.global_efficiency(component_subgraph))
                    efficiency[node] = sum(component_efficiencies) / len(component_efficiencies)

        return efficiency

    def eccentricity(self, graph, weight):
        """
        Calculate the eccentricity for each node in the graph, considering edge weights.

        Parameters
        ----------
        graph : nx.Graph
            The graph for which to calculate eccentricity.
        weight : str or None
            The name of the edge attribute used as weight. If None, treats the graph as unweighted.

        Returns
        -------
        dict
            A dictionary where the keys are node IDs, and the values are their eccentricity values.
        """
        eccentricity = {}
        
        # Iterate over each connected component of the graph
        for component in nx.connected_components(graph):
            subgraph = graph.subgraph(component)
            
            # Calculate the lengths of the shortest paths with weights
            path_lengths = dict(nx.all_pairs_dijkstra_path_length(subgraph, weight=weight))
            
            # Calculate eccentricity for subgraph
            subgraph_eccentricity = {}

            for node in subgraph.nodes():
                max_distance = max(path_lengths[node].values(), default=0)
                subgraph_eccentricity[node] = max_distance
            
            eccentricity.update(subgraph_eccentricity)
        
        return eccentricity
    
    def GetLocalMeasures(self, localMeasure):
        """
        Retrieve local graph-theoretic measures for each node in the graph.

        Parameters
        ----------
        localMeasure : str
            The name of the local measure to retrieve. Must match a case in this method.

        Returns
        -------
        dict
            A dictionary where the keys are node IDs, and the values are the computed measure values.
        """
        match localMeasure:
            # ---- Weighted ----

            case "degree (weighted)":
                return dict(self.nxGraph.degree(weight='weight'))
            case "cluster coef (weighted)":
                return nx.clustering(self.nxGraph, weight='weight')
            case "local efficiency (weighted)":
                return self.local_efficiency(self.nxGraph)
            case "betweenness centrality (weighted)":
                return nx.betweenness_centrality(self.nxGraph, weight="weight", normalized=False)
            case "eigenvector centrality (weighted)":
                try:
                    return nx.eigenvector_centrality(self.nxGraph, max_iter=1000, tol=1e-5, weight='weight')
                except nx.PowerIterationFailedConvergence:
                    return nx.eigenvector_centrality_numpy(self.nxGraph, weight='weight')
            case "eccentricity (weighted)":
                return self.eccentricity(self.nxGraph, "weight")

            # ---- Binary ----
            case "degree (binary)":
                return dict(self.nxGraphBinary.degree())
            case "cluster coef (binary)":
                return nx.clustering(self.nxGraphBinary)
            case "local efficiency (binary)":
                return self.local_efficiency(self.nxGraphBinary)
            case "betweenness centrality (binary)":
                return nx.betweenness_centrality(self.nxGraphBinary, normalized=False)
            case "eigenvector centrality (binary)":
                return nx.eigenvector_centrality(self.nxGraphBinary)
            case "eccentricity (binary)":
                return self.eccentricity(self.nxGraphBinary, None)