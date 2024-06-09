import argparse

from Window import MainWindow
from ETools import ETools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='External tool for asset download')
    
    parser.add_argument('--app', required=False, action='store_true', help='run as GUI')
    parser.add_argument('--config_folder', required=True, help='where to store tool db')
    
    args = parser.parse_args()

    ETools.ConfigFolder = args.config_folder

    if args.app:
        MainWindow.show_window()
    else:
        print("Hello")