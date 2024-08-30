import os
import platform
import shutil
import argparse
import sys
import logging
from .constants import FILE_TYPES
from .utils import print_red, print_yellow, print_green

__version__ = "1.0.2"

# def get_system_user_directories():
#     if platform.system() == 'Darwin':
#         print("MAC OS")
#     elif platform.system() == 'Linux':
#         print("Linux")
#     elif platform.system() == 'Windows':
#         print("Windows")
#     else:
#         print("Warning for use this script on your OS")

def remove_empty_dir(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return False

    if not os.listdir(directory):
        try:
            os.rmdir(directory)
            return True
        except Exception as e:
            print_red(f"Error while deleting directory '{directory}': {e}")
            return False
    else:
        print_red(f"Directory '{directory}' is not empty, deletion not performed.")
        return False

def create_master_folder(source_folder, simulation, custom_folder_name=None):
    folder_name = custom_folder_name if custom_folder_name else 'TidySorter'
    master_folder = os.path.join(source_folder, folder_name)
    
    if not simulation and not os.path.exists(master_folder):
        os.makedirs(master_folder)
    
    return master_folder

def handle_shortcuts(item_name, item_path, simulation, safe, master_folder):
    folder_path = os.path.join(master_folder, 'Shortcuts')

    if simulation:
        if safe:
            print_yellow(f'[SIMULATION] {item_name} would be moved to {folder_path}')
        else:
            print_red(f'[SIMULATION] Shortcut file "{item_name}" would be deleted.')
    elif safe:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        shutil.move(item_path, os.path.join(folder_path, item_name))
        print_green(f'Shortcut file "{item_name}" moved to "{folder_path}".')
    else:
        os.remove(item_path)
        print_red(f'Shortcut file "{item_name}" deleted.')

def organize_files(source_folder, simulation=False, recursive=False, custom_folder_name=None, safe=False, quiet=False):
    master_folder = create_master_folder(source_folder, simulation, custom_folder_name)
    
    for item_name in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item_name)
        
        if item_name == 'TidySorter':
            continue

        if item_name.lower().endswith('.lnk'):
            handle_shortcuts(item_name, item_path, simulation, safe, master_folder)
            continue

        if os.path.isdir(item_path):
            folder_path = os.path.join(master_folder, 'Folders')
            if simulation:
                print_yellow(f'[SIMULATION] Folder "{item_name}" would be checked and potentially moved to {folder_path}')
            else:
                if remove_empty_dir(item_path):
                    print_red(f"Empty directory '{item_path}' deleted.")
                else:
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(item_path, os.path.join(folder_path, item_name))
                    print_green(f'Folder "{item_name}" moved to {folder_path}')
            continue
        
        if os.path.isfile(item_path):
            file_ext = os.path.splitext(item_name)[1].lower()
            moved = False
            for folder_name, extensions in FILE_TYPES.items():
                if file_ext in extensions:
                    folder_path = os.path.join(master_folder, folder_name)
                    if simulation:
                        print_yellow(f'[SIMULATION] {item_name} would be moved to {folder_path}')
                    else:
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        shutil.move(item_path, os.path.join(folder_path, item_name))
                        print_green(f'{item_name} moved to {folder_path}')
                    moved = True
                    break

            if not moved and simulation:
                print_yellow(f'[SIMULATION] {item_name} does not match any defined category.')

def main() -> None:
    parser = argparse.ArgumentParser(description="Effortlessly organize your files into neatly categorized folders, making it easier to prepare for system formatting or reinstallation, or simply to clean up cluttered directories filled with accumulated files. Compatible with macOS, Linux, and Windows.")
    parser.add_argument('source_folder', nargs='?', help="The source folder to sort")
    parser.add_argument("-f", "--folder", type=str, help="Custom name of the master folder.")
    # parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all console output (quiet mode)")
    # parser.add_argument('-r', '--revert', action='store_true', help="Revert everything (requires log)")
    # parser.add_argument("-R", "--recursive", action="store_true", help="Apply sorting recursively to subfolders")
    parser.add_argument('-s', '--simulate', action='store_true', help='Enable simulation mode (no changes will be made)')
    parser.add_argument("-S", "--safe", action="store_true", help="Prevent deletion of empty folders and shortcut files. By default, empty folders and shortcut files will be removed during sorting.")
    parser.add_argument("-v", "--version", action="version", version=__version__, help="Display the version number")
    # parser.add_argument('-w', '--without-log', action='store_true', help='Without logs')

    args = parser.parse_args()

    # if args.recursive:
    #     try:
    #         print("\033[93mWarning: You have selected recursive sorting. This will process all subdirectories.\033[0m")
    #         confirmation = input("Do you want to continue? (y/yes to confirm): ").strip().lower()

    #         if confirmation not in ['y', 'yes']:
    #             print("\033[91mOperation cancelled by the user.\033[0m")
    #             sys.exit(1)
        
    #     except KeyboardInterrupt:
    #         print("\n\033[91mOperation cancelled by the user via Ctrl+C.\033[0m")
    #         sys.exit(1)

    if args.source_folder:
        print(f"Processing folder: {args.source_folder}")
    else:
        print("No source folder provided. Use -h for help.")
        sys.exit()
        
    if not os.path.isdir(args.source_folder):
        print(f"Error: {args.source_folder} is not a valid folder.")
        sys.exit()

    organize_files(
        args.source_folder,
        simulation=args.simulate,
        # recursive=args.recursive,
        safe=args.safe,
        # quiet=args.quiet,
        custom_folder_name=args.folder
    )

if __name__ == "__main__":
    main()