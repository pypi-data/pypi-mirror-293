import pandas as pd
import os
import glob
from pathlib import Path

# __all__ = ["get_folder_overview"]

def get_folder_overview(path: str):
    sub_folder_names = []
    file_names = []
    file_sizes = []
    file_extenstions = []
    num_files_folder = []
    folder_paths = []
    is_folder = []
    depth_count = []

    files = glob.glob(pathname=path+"/**/*", recursive=True)
    for file in files:

        # get the relative path from the base path ("path") to the target
        # path ("file")
        p = Path(os.path.relpath(file, path))
       
        
        if os.path.isfile(file):
            # print(file)
            
            dir_path = os.path.dirname(file)
            folder_paths.append(file)

            dir_name = os.path.basename(dir_path)
            sub_folder_names.append(dir_name)

            file_name = os.path.basename(file)
            file_names.append(file_name)

            file_size = os.path.getsize(file)
            file_sizes.append(file_size)

            file_extension = os.path.splitext(file_name)[1]
            file_extenstions.append(file_extension)

            num_files_folder.append(0)
            
            is_folder.append(False)

            depth_count.append(len(p.parents)-1)
            
        else:
            dir_name = os.path.basename(file)
            sub_folder_names.append(dir_name)
            
            file_names.append("N/A")
            file_size = os.path.getsize(0)
            file_sizes.append(file_size)

            file_extenstions.append("N/A")

            f = os.listdir(file)
            num_files = len(f)
            num_files_folder.append(num_files)

            folder_paths.append(file)
            is_folder.append(True)

            depth_count.append(len(p.parents)-1)

        
    df = pd.DataFrame({
        'Path':folder_paths,
        'Folder Name':sub_folder_names,
        'Is Folder?': is_folder,
        'File Name':file_names,
        'File Size (Bytes)': file_sizes,
        'File Extensions': file_extenstions,
        'Number of Files in Folder': num_files_folder,
        'Depth': depth_count
        }   
    )

    return df