import os
import jenkins
import json
from pathlib import Path
from utils import *




def process_file(file_path):
    """Process a single XML file and create a Jenkins job."""
    with open(file_path, 'r') as config:
        config_xml = config.read()
        job_url = str(file_path).replace(f"{PARENT_FOLDER}\\", "").replace(".xml", "").replace("\\", "/")
        try:
            create_job(SERVER, job_url, config_xml)
        except Exception as e:
            print(f"ERROR: Skipping {job_url} due to following error: {e}")

def sort_files_and_folders(folder_path):
    """Sort files first, then folders in a given directory."""
    items = os.listdir(folder_path)
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
    return files + folders

def process_folder(folder_path):
    """Process all files and subfolders in a given folder, files first."""
    for item in sort_files_and_folders(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.endswith('.xml'):
            process_file(item_path)
        elif os.path.isdir(item_path):
            process_folder(item_path)

def main():
    """Main function to start the job creation process."""
    global SERVER
    global PARENT_FOLDER
    config = load_config('secrets/secret.json')
    SERVER = connect_to_jenkins(config, skip_ssl_verification=True)
    PARENT_FOLDER = config.get('config_folder')
    process_folder(PARENT_FOLDER)

if __name__ == "__main__":
    main()