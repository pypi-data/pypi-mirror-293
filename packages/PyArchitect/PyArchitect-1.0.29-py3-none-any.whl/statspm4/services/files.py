import os
from pathlib import Path
import string

class Files():
    
    staticmethod 
    def get_root_path() -> str:
        root_path = os.path.dirname(os.path.dirname( __file__))
        return root_path
       
    staticmethod
    def get_prompt(name: str):
        root_path = Files.get_root_path()
        template_path = os.path.join(root_path, 'resources', 'prompts', f'{name}.txt')
        content = Path(template_path).read_text()
        return content 

        
    def sanitize_folder_name(folder_name):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        temp = ''.join(c for c in folder_name if c in valid_chars)
        return temp.lower()

    def sanitize_package_name(package_name):
        valid_chars = "_.%s%s" % (string.ascii_letters, string.digits)
        temp = ''.join(c for c in package_name if c in valid_chars)
        return temp.lower()


    def create_directory(path):
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Directory '{path}' has been created successfully.")
        except Exception as e:
            print(f"Failed to create directory '{path}'. Reason: {e}")