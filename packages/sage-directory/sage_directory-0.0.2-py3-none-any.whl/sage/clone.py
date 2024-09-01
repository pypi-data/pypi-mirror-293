import os
import shutil

# __all__ = ["copy_num_folders", "copy_folders","batch_file_overwrite"]

def copy_num_folders(ref_dir:str, src_dir:str, dest_dir:str, num_folders=None):
    folders = [folder for folder in os.listdir(src_dir) if os.path.isdir(os.path.join(ref_dir, folder))]

    count = 0
    if(num_folders==None):
        for folder in folders[:]:
            count = count+1
            src_folder = os.path.join(src_dir, folder)
            dest_folder = os.path.join(dest_dir, folder)

            try:
                shutil.copytree(src_folder, dest_folder)
                print(str(count),"Copied "+src_folder+" to "+dest_folder)
            except Exception as e:
                print("Failed to copy "+src_folder+" to "+dest_folder+":" +str(e))
    else:
        for folder in folders[:num_folders]:
            count = count+1
            src_folder = os.path.join(src_dir, folder)
            dest_folder = os.path.join(dest_dir, folder)

            try:
                shutil.copytree(src_folder, dest_folder)
                print(str(count),"Copied "+src_folder+" to "+dest_folder)
            except Exception as e:
                print("Failed to copy "+src_folder+" to "+dest_folder+":" +str(e))        

    return None



def copy_folders(ref_dir:str, src_dir:str, dest_dir:str):
    folders = [folder for folder in os.listdir(ref_dir) if os.path.isdir(os.path.join(ref_dir,folder))]

    count = 0
    for folder in folders:
        count = count + 1
        src_folder = os.path.join(src_dir, folder)
        dest_folder = os.path.join(dest_dir, folder)

        try:
            shutil.copytree(src_folder, dest_folder)
            print(str(count), "Copied "+src_folder+" to "+dest_folder)
        except Exception as e:
            print("Failed to copy "+src_folder+" to "+dest_folder+": "+str(e))
            
    return None



def batch_file_overwrite(src_dir: str, dest_dir:str, filename: str):
    dest_folders = [folder for folder in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, folder))]
    src_folders = [folder for folder in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, folder))]

    count = 0
    for folder in dest_folders:
        if folder in src_folders:
            file_to_copy_from_src = os.path.join(src_dir, folder, filename)
            file_to_copy_over_in_dest_folder = os.path.join(dest_dir, folder, filename)

            try:
                count = count + 1
                shutil.copy(file_to_copy_from_src, file_to_copy_over_in_dest_folder)
                print(str(count), "Updated "+file_to_copy_over_in_dest_folder+" to "+file_to_copy_from_src)
            except Exception as e:
                print("Failed to update "+file_to_copy_over_in_dest_folder+" to "+file_to_copy_from_src+": "+str(e))
    return None