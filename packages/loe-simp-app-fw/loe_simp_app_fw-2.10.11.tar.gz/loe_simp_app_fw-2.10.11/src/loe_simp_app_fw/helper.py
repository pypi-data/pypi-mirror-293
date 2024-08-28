import os
import re
import sys

if "logger" not in sys.modules:
    # Bootstrap mode
    def create_folder_if_not_exists(folder_path: str) -> bool:
        # Return if the folder exists
        # It only create one folder at a time

        if not os.path.isfile(folder_path) and not os.path.isdir(folder_path):
            os.mkdir(folder_path)
            print(f"Folder {folder_path} does not exists. Creating a new one.")
            return True
        else:
            return False
else:
    # Normal mode
    from .logger import Logger
    def create_folder_if_not_exists(folder_path: str) -> bool:
        # Return if the folder exists
        # It only create one folder at a time

        if not os.path.isfile(folder_path) and not os.path.isdir(folder_path):
            os.mkdir(folder_path)
            Logger.info("Folder does not exists. Creating a new one.")
            return True
        else:
            Logger.debug("Folder exists. No further action.")
            return False

def remove_duplicate_space(input_str: str) -> str:
    # Remove excessive space
    reg = r'\s+'
    result = re.sub(reg, " ", input_str).strip()
    return result


class ProjectRootChanged(Exception):
    def __init__(self):
        pass
