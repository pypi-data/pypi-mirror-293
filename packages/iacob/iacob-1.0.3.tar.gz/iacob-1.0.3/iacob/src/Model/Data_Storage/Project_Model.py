import os
import json

from src.Model.Data_Storage.DataSingleton_Model import DataSingleton
from src.Model.Data_Storage.Filters_Model import Filters_Infos

class Project_Infos(metaclass=DataSingleton):
    """
    A class to manage and store information about the project

        - Absolute Path to Files (Data, FLUT, Filters)
        - Previous files opened
        - Export Project (JSON)
    """
    def __init__(self):
        
        self.filters = Filters_Infos()
        self.previousFiles = {"DataFiles": {}, 
                              "NameFiles": {}, 
                              "FlutFiles": [], 
                              "FiltersFiles": [], 
                              "ProjectFiles": []}
        
        self.InitReset()

    def InitReset(self):
        """
        Reset the current file paths to None. This is useful for initializing the state
        of a new or empty project.
        """

        self.currentDataFile = None
        self.currentNameFile = None
        self.currentFlutFile = None
        self.currentFiltersFile = None

    def InitRestore(self, projectSave: 'Project_Infos'):
        """
        Restore the state of the current project using a saved Project_Infos object.

        Parameters
        ----------
        projectSave : Project_Infos
            An instance of Project_Infos containing the saved state to be restored.
        """

        self.currentDataFile = projectSave.currentDataFile
        self.currentNameFile = projectSave.currentNameFile
        self.currentFlutFile = projectSave.currentFlutFile

    def ExportToJSON(self, filePathFull):

        """
        Export the current project information to a JSON file. This includes saving the 
        current filter settings to a separate file.

        Parameters
        ----------
        filePathFull : str
            The full path where the project JSON file will be saved.
        """

        filePath = os.path.dirname(filePathFull)
        filePath_basename = ".".join(os.path.basename(filePathFull).split('.')[:-1])
        newFilePath = os.path.join(filePath, f"{filePath_basename}-Filters.json")
        self.filters.ExportToJSON(newFilePath)

        projectToJSON = {

            "currentDataFile": self.currentDataFile,
            "currentNameFile": self.currentNameFile,
            "currentFlutFile": self.currentFlutFile,
            "currentFiltersFile": newFilePath
        }

        with open(filePathFull, 'w', encoding='utf-8') as file:
            json.dump(projectToJSON, file, ensure_ascii=False, indent=4)