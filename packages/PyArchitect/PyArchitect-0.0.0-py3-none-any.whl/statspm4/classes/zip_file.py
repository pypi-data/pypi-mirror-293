import logging
import os
import shutil
import zipfile

logger = logging.getLogger("pyarchitect")

class ZipFileHandler:
    def init(self):
        pass
        
    def verify(zip_file_path: str):
        # Check if the file exists
        if not os.path.isfile(zip_file_path):
            logger.error(f"The file {zip_file_path} does not exist.")
            return False

        # Check if the file is a zip file
        if not zipfile.is_zipfile(zip_file_path):
            logger.error(f"The file {zip_file_path} is not a valid zip file.")
            return False
        return True
        

    def get_main_folder(zip_file_path: str):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Get the list of all file and directory names in the zip
            all_names = zip_ref.namelist()
            
            # Extract the top-level directories
            top_level_dirs = set()
            for name in all_names:
                # Split the path and get the top-level directory
                top_level_dir = name.split(os.sep)[0]
                top_level_dirs.add(top_level_dir)
            
            # If there's exactly one top-level directory, return it
            if len(top_level_dirs) == 1:
                return top_level_dirs.pop()
            else:
                return None
            
                    
    def unzip(zip_file_path: str):
        # Extract the zip file to the same parent folder
        parent_folder = os.path.dirname(zip_file_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(parent_folder)
            logger.debug(f"Extracted {zip_file_path} to {parent_folder}")

        return parent_folder

    def unzip_csv(zip_file_path: str, csv_paths: str):
        if not ZipFileHandler.verify(zip_file_path):
            return False
        
        parent_folder = ZipFileHandler.unzip(zip_file_path)
        main_folder = ZipFileHandler.get_main_folder(zip_file_path)
        
        ZipFileHandler.move_csv_files(os.path.join(parent_folder, main_folder), csv_paths)

    def move_csv_files(input_folder, output_folder):
        """
        Move all .csv files from the input folder to the output folder.

        :param input_folder: Path to the input folder
        :param output_folder: Path to the output folder
        """
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        logger.info(f"Main folder: {input_folder}")
        # Iterate over all files in the input folder
        for filename in os.listdir(input_folder):
            # Check if the file has a .csv extension
            if filename.endswith('.csv'):
                # Construct full file path
                src_file = os.path.join(input_folder, filename)
                dest_file = os.path.join(output_folder, filename)
                # Move the file
                shutil.move(src_file, dest_file)
                logger.debug(f"Moved: {src_file}")
            
        shutil.rmtree(input_folder)