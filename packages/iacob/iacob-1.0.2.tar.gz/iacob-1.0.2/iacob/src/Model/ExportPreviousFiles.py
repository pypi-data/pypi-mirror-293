import os
from pathlib import Path

class ExportPrevious_Files:

    def __init__(self):
         
        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        self.backupFiles = os.path.join(resourcedir, "Backup_PreviousFiles.txt")

    def SaveFile(self, previousFiles: dict):
        """
        Save information about previous files into a backup file.
        
        Parameters
        ----------
        previousFiles : dict
            A dictionary containing previous files categorized by type. Expected structure:
            {
                "DataFiles": {filename: filetype, ...},
                "NameFiles": {filename: name, ...},
                "FlutFiles": [filename, ...],
                "FiltersFiles": [filename, ...],
                "ProjectFiles": [filename, ...]
            }
        
        Raises
        ------
        ValueError
            If the previousFiles dictionary is not in the expected format.
        FileNotFoundError
            If the backup file cannot be created or opened.
        """

        try:
            backupFilenames = open(os.path.abspath(self.backupFiles), 'w')
        except FileNotFoundError:
            raise Exception("Creation Error - {}".format(self.backupFiles))
        
        # Write all Previous File in the Backup File

        # DATA File Part
        backupFilenames.write("DataFiles\n")
        
        for dataFile, fileType in previousFiles["DataFiles"].items():

            backupFilenames.write(dataFile + "|" + fileType + "\n")

        # Name File Part
        backupFilenames.write("NameFiles\n")
        
        for dataFile, nameFile in previousFiles["NameFiles"].items():

            backupFilenames.write(dataFile + "|" + nameFile + "\n")

        # Flut File Part
        backupFilenames.write("FlutFiles\n")

        for flutFile  in previousFiles["FlutFiles"]:

            backupFilenames.write(flutFile + "\n")

        # CONFIG File Part
        backupFilenames.write("FiltersFiles\n")
        
        for filtersFile in previousFiles["FiltersFiles"]:

            backupFilenames.write(filtersFile + "\n")

        # PROJECT File Part
        backupFilenames.write("ProjectFiles\n")
        
        for projectFile in previousFiles["ProjectFiles"]:

            backupFilenames.write(projectFile + "\n")

        backupFilenames.close()


