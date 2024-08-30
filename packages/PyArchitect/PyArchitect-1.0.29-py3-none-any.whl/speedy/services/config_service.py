import os
import configparser

#from utils.filenames import sanitize_folder_name

class Config():

    # Database configuration
    db_user: str = None 
    db_password: str = None 
    db_host: str = None 
    db_database: str = None 
    db_raise_on_warnings: str = None

    root_dir: str = None

    def read(self, config_path: str):
        parser = configparser.ConfigParser()
        if not os.path.isfile(config_path):
            raise  FileNotFoundError(f"The config file '{config_path}' does not exist.")
        
        if not config_path:
            config_path = 'speedy.ini'
            
            
        parser.read(config_path)
        self.root_dir = os.path.dirname(os.path.dirname( os.path.dirname(__file__) ))

        # database configurations
        self.db_user = parser.get('DATABASE', 'db_user')
        self.db_password = parser.get('DATABASE', 'db_password')
        self.db_host = parser.get('DATABASE', 'db_host')
        self.db_database = parser.get('DATABASE', 'db_database')

        # security_log
        self.sl_num_workers = int(parser.get('SECURITY_LOGS', 'num_workers'))
        self.sl_batch_size  = int(parser.get('SECURITY_LOGS', 'batch_size'))
        self.sl_buffer_size = int(parser.get('SECURITY_LOGS', 'buffer_size'))
        self.sl_goal        = int(parser.get('SECURITY_LOGS', 'goal'))

config = Config()