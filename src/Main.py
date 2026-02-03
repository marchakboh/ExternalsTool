import argparse
from Window import MainWindow
from ConsoleWindow import ConsoleWindow
from ETools import ETools

def run_as_window():
    MainWindow.show_window()

def run_as_console():
    ConsoleWindow.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='External tool for asset download')
    
    parser.add_argument('--app',            required=False, action='store_true',    help='run as GUI')
    parser.add_argument('--root_folder',    required=True,                          help='root of project')
    parser.add_argument('--config_folder',  required=True,                          help='where to store tool db')
    
    args = parser.parse_args()

    ETools.get().set_root_folder(args.root_folder)
    ETools.get().set_config_folder(args.config_folder)

    if args.app:
        run_as_window()
    else:
        run_as_console()