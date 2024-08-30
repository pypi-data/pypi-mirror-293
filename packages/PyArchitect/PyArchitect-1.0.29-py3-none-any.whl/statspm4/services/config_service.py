import os
import configparser

from utils.filenames import sanitize_folder_name

class Config():
    root_dir: str = None
    project: str = None
    source_dir: str = None

    plantuml_dir: str = None
   
    # calculated paths 
    source_path : str = None
    output: str = None
    output_png: str = None
        
    def read(self, config_path: str):
        parser = configparser.ConfigParser()
        parser.read(config_path)
        self.zip_file = parser.get('STM', 'zip_file')
        self.csv_paths = parser.get('STM', 'csv_paths')
        


config = Config()