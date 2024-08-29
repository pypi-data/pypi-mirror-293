import argparse
import logging

from services.config_service import config
from classes.zip_file import ZipFileHandler
from classes.pm4_stats import Pm4Stats

logger = logging.getLogger("pyarchitect")

def main():
    parser = argparse.ArgumentParser(description='Stats for PM4.')
    parser.add_argument('config_path', type=str, help='Path to the config file')

    args = parser.parse_args()
    config.read(args.config_path)
    
    ZipFileHandler.unzip_csv(config.zip_file, config.csv_paths)
    Pm4Stats.process(config.csv_paths)
main()