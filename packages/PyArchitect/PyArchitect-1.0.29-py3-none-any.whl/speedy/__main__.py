import argparse
import os
import sys
import traceback

import mysql.connector


# Add this directory to sys.path
package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package_dir)

from speedy.services.config_service import config
from speedy.services.security_logs_service import SecurityLogsService


def main():
    parser = argparse.ArgumentParser(description='Database utils.')
    parser.add_argument('command', type=str, help="Command to execute 'fake', 'copy' ")
    parser.add_argument('--config_path', type=str, help='Path to the config file')

    args = parser.parse_args()
    command = args.command
    
    try:
        config.read(args.config_path)
        
        securityLogsService = SecurityLogsService()
        
        if command == 'fake':
            securityLogsService.execute_fake_rows()
        if command == 'copy':
            securityLogsService.execute_fast_copy()

        if command == 'prt':
            securityLogsService.execute_queue_prt_copy()

    except mysql.connector.errors.DatabaseError as dbe: 
        print(dbe)
        return
    except Exception as e: 
        print( e)
        print(f"Exception class: {type(e).__name__}")
        traceback.print_exc()
        
main()
