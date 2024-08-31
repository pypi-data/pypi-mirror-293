from copy import deepcopy

from PyQt5.QtGui import QColor

class FiltersSave_Infos():
    """
    A class to store a current state of the Singleton Filters_Model class
    """

    def __init__(self):
        """
        Initialize the FiltersSave_Infos class with default values for all filter settings.
        """

        self.Save = False
        self.thresholdPostFiltering: float = 0.0

        # Connection types
        self.contralateral_connType: bool = True
        self.homotopic_connType: bool = True
        self.ipsilateral_connType: bool = True
        self.other_connType: bool = True

        # Inter regional connections -> {(name1, name2) : visible}
        self.discardInterRegConn: dict[(str, str), bool] = {}

        # Thresholds
        self.discardWeight: bool = False
        self.discardAbsWeight: bool = False
        self.discardRank: bool = False

        self.weightBetween_threshold: list[float] = [0.0, 0.0]
        self.absWeightBetween_threshold: list[float] = [0.0, 0.0]
        self.rankBetween_threshold: list[int] = [0, 0]

        self.coefWidthEdges: int  = 5
        self.colorEdges: list[QColor] = []
        
    def RecovertFiltersSave(self):
        """
        Save the current filter settings to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the current filter settings.
        """

        return {
            
            "thresholdPostFiltering": self.thresholdPostFiltering,
            
            "WeightAndRank": {

                "Weight": {
                    "discardWeight": self.discardWeight,
                    "weightBetween_threshold": deepcopy(self.weightBetween_threshold),
                },

                "AbsWeight": {

                    "discardAbsWeight": self.discardAbsWeight,
                    "absWeightBetween_threshold": deepcopy(self.absWeightBetween_threshold),
                },

                "Rank": {

                    "discardRank": self.discardRank,
                    "rankBetween_threshold": deepcopy(self.rankBetween_threshold),
                }
            },

            "InterRegConn": deepcopy(self.discardInterRegConn),

            "ConnType": {

                "contralateral_connType": self.contralateral_connType,
                "homotopic_connType": self.homotopic_connType,
                "ipsilateral_connType": self.ipsilateral_connType,
                "other_connType": self.other_connType,
            }
        }

    def LoadCurrentFilters(self, filtersCurrent: dict):
        """
        Load filter settings from a dictionary provided from the current instance.

        Parameters
        ----------
        filtersCurrent : dict
            A dictionary containing filter settings to be loaded.
        """

        self.Save = True
        self.thresholdPostFiltering = filtersCurrent["thresholdPostFiltering"]

        conn_types = filtersCurrent["ConnType"]
        self.contralateral_connType = conn_types["contralateral_connType"]
        self.homotopic_connType = conn_types["homotopic_connType"]
        self.ipsilateral_connType = conn_types["ipsilateral_connType"]
        self.other_connType = conn_types["other_connType"]

        self.discardInterRegConn = filtersCurrent["InterRegConn"]

        weight_and_rank = filtersCurrent["WeightAndRank"]

        weight = weight_and_rank["Weight"]
        self.discardWeight = weight["discardWeight"]
        self.weightBetween_threshold = weight["weightBetween_threshold"]

        abs_weight = weight_and_rank["AbsWeight"]
        self.discardAbsWeight = abs_weight["discardAbsWeight"]
        self.absWeightBetween_threshold = abs_weight["absWeightBetween_threshold"]

        rank = weight_and_rank["Rank"]
        self.discardRank = rank["discardRank"]
        self.rankBetween_threshold = rank["rankBetween_threshold"]

    def InitInterRegConnDict(self, names: list[str]):
        """
        Initialize the dictionary for interregional connections with the given names.

        Parameters
        ----------
        names : list[str]
            A list of region names to initialize the interregional connection dictionary.
        """

        for name1 in names:
            for name2 in names:
                self.discardInterRegConn[(name1, name2)] = True

    
    # =============================
    # ===== Filters Accessors =====
    # =============================

    # ----- Weight threshold -----

    def WeightMin(self) -> float:
        """
        Get the minimum weight threshold.

        Returns
        -------
        float
            The minimum weight threshold.
        """

        return self.weightBetween_threshold[0]

    def WeightMax(self) -> float:
        """
        Get the maximum weight threshold.

        Returns
        -------
        float
            The maximum weight threshold.
        """

        return self.weightBetween_threshold[1]

    def SetWeightMin(self, weightMin: float):
        """
        Set the minimum weight threshold.

        Parameters
        ----------
        weightMin : float
            The minimum weight threshold to set.
        """

        self.weightBetween_threshold[0] = weightMin

    def SetWeightMax(self, weightMax: float):
        """
        Set the maximum weight threshold.

        Parameters
        ----------
        weightMax : float
            The maximum weight threshold to set.
        """

        self.weightBetween_threshold[1] = weightMax


    # ----- Abs weight threshold ------

    def AbsWeightMin(self) -> float:
        """
        Get the minimum absolute weight threshold.

        Returns
        -------
        float
            The minimum absolute weight threshold.
        """

        return self.absWeightBetween_threshold[0]

    def AbsWeightMax(self) -> float:
        """
        Get the maximum absolute weight threshold.

        Returns
        -------
        float
            The maximum absolute weight threshold.
        """

        return self.absWeightBetween_threshold[1]

    def SetAbsWeightMin(self, absWeightMin: float):
        """
        Set the minimum absolute weight threshold.

        Parameters
        ----------
        absWeightMin : float
            The minimum absolute weight threshold to set.
        """

        self.absWeightBetween_threshold[0] = absWeightMin

    def SetAbsWeightMax(self, absWeightMax: float):
        """
        Set the maximum absolute weight threshold.

        Parameters
        ----------
        absWeightMax : float
            The maximum absolute weight threshold to set.
        """

        self.absWeightBetween_threshold[1] = absWeightMax


    # ----- Rank threshold -----

    def RankMin(self) -> int:
        """
        Get the minimum rank threshold.

        Returns
        -------
        int
            The minimum rank threshold.
        """

        return self.rankBetween_threshold[0]

    def RankMax(self) -> int:
        """
        Get the maximum rank threshold.

        Returns
        -------
        int
            The maximum rank threshold.
        """

        return self.rankBetween_threshold[1]

    def SetRankMin(self, rankMin: int):
        """
        Set the minimum rank threshold.

        Parameters
        ----------
        rankMin : int
            The minimum rank threshold to set.
        """

        self.rankBetween_threshold[0] = rankMin

    def SetRankMax(self, rankMax: int):
        """
        Set the maximum rank threshold.

        Parameters
        ----------
        rankMax : int
            The maximum rank threshold to set.
        """

        self.rankBetween_threshold[1] = rankMax

    
    # ----- InterRegion Dictionary ------

    def InterRegConnEnabled(self, name1: str, name2: str) -> bool:
        """
        Check if the interregional connection between two regions is enabled.

        Parameters
        ----------
        name1 : str
            The first region name.
        name2 : str
            The second region name.

        Returns
        -------
        bool
            True if the interregional connection is enabled, False otherwise.
        """

        if (name1, name2) in self.discardInterRegConn:
            return self.discardInterRegConn[(name1, name2)]

    def SetInterRegConnEnabled(self, name1: str, name2: str, state: bool):
        """
        Enable or disable the interregional connection between two regions.

        Parameters
        ----------
        name1 : str
            The first region name.
        name2 : str
            The second region name.
        state : bool
            The state to set for the connection (True for enabled, False for disabled).
        """

        self.discardInterRegConn[(name1, name2)] = state
        self.discardInterRegConn[(name2, name1)] = state
