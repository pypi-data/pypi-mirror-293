# Sage

sage-directory is a python package that offers a detailed overview of folder contents and streamlines the process of copying and managing directories. It is designed to enhance productivity and simplify file management. It provides details of folder contents, including the file types, size, and subfolder structures, enabling quick insights into the organization of your directory. 

Beyond analysis, the tool offers robust functionality for copying entire folders, ensuring seamless management and replication of data environments. Whether you're organizing complex project files, backing up critical datasets, or duplicating environments, this tool is built to optimize your workflow.

## Installation
```
pip install sage-directory
```

## Usage
### Main Features
Comprehensive Folder Overview
##
Generate detailed summaries of folder contents, including file types, sizes, and subfolder structures, 

```python
import sage

sage.get_folder_overview('.')
```

<table>
    <tr>
        <td>Path</td>
        <td>Folder Name</td>
        <td>Is Folder?</td>
        <td>File Name</td>
        <td>File Size (Bytes)</td>
        <td>File Extensions</td>
        <td>Number of Files in Folder</td>
        <td>Depth</td>
    </tr>
     <tr>
        <td>./bathoom.py</td>
        <td>.</td>
        <td>False</td>
        <td>bathoom_cal.py</td>
        <td>2151</td>
        <td>.py</td>
        <td>0</td>
        <td>0</td>
    </tr>
     <tr>
        <td>./kitchen.png</td>
        <td>.</td>
        <td>False</td>
        <td>kitchen.png</td>
        <td>2151</td>
        <td>.png</td>
        <td>0</td>
        <td>0</td>
    </tr>
     <tr>
        <td>./shops</td>
        <td>shops</td>
        <td>True</td>
        <td>N/A</td>
        <td>0</td>
        <td>N/A</td>
        <td>2</td>
        <td>1</td>
    </tr>
</table>


Selective Copying
##
Choose a specific file to overwrite another in multiple directories

```python
import sage

# overwrites the entered filename (basement.png) in the renovated_kitchen folder with the file in kitchen_catelog folder

sage.batch_file_overwrite(./kitchen_catelog, ./renovated_kitchen, "basement.png")

```


Batch Operations
##
Perform operations on multiple directories

```python
import sage

# only copies 10 folders that are in the kitchen_catelog that share the same folder names as those in the old_kitchen folder in the renovated_kitchen folder

sage.copy_num_folders(./old_kitchen, ./kitchen_catelog, ./renovated_kitchen, 10)

# only copies folders that are in the kitchen_catelog that share the same folder names as those in the old_kitchen folder in the renovated_kitchen folder

sage.copy_folders(./old_kitchen, ./kitchen_catelog, ./renovated_kitchen)

```
