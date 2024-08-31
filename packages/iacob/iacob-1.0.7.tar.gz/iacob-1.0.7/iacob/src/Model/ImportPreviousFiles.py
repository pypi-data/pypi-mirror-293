import os
from pathlib import Path

class ParserPrevious_Files:
    """
    A class to parse Previous File
    """
    def __init__(self):
        
        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        self.backupFile = os.path.join(resourcedir, "Backup_PreviousFiles.txt")
        self.previousFiles = {"DataFiles": {}, "NameFiles": {}, "FlutFiles": [], "FiltersFiles": [], "ProjectFiles": []}

    def LoadFile(self) -> dict:
        """
        Load and parse the backup file.

        Reads the backup file, categorizes lines into different lists or dictionaries based on the category, and handles errors.

        Returns
        -------
        dict
            A dictionary with lists and dictionaries of previous file paths, categorized by type.

        Raises
        ------
        Exception
            If the file cannot be found or the file format is incorrect.
        """
        
        # Ensure file exist (already created or not deleted)
        if os.path.exists(self.backupFile):
            
            try:
                previousFilenames = open(os.path.abspath(self.backupFile), 'r')
            except FileNotFoundError:
                raise Exception("Opening Error - {}".format(self.backupFile))

            category = None
            for line in previousFilenames.readlines():

                # Check the current category
                cleanLines = line.replace("\n", '') 
                if cleanLines == "DataFiles" or cleanLines == "NameFiles" or cleanLines == "FlutFiles" \
                    or cleanLines == "FiltersFiles" or cleanLines == "ProjectFiles":
                    
                    category = cleanLines
                    continue

                # Append File Name in the dictionary
                try:

                    if len(self.previousFiles[category]) == 5:
                        continue

                    # All element before a Category will be ignored
                    if category == "NameFiles" or category == "DataFiles":
                        
                        cleanLinesSepared = cleanLines.split("|")
                        self.previousFiles[category][cleanLinesSepared[0]] = cleanLinesSepared[1]

                    elif category != None:

                        self.previousFiles[category].append(cleanLines)

                except KeyError:
                    raise Exception("Wrong Format Error - Category Error")

            previousFilenames.close()

        return self.previousFiles
