from setuptools import setup, find_packages
from pathlib import Path
import os

VERSION = "0.0.3"
# readme information
dir = Path(__file__).absolute().parent
with open(os.path.join(dir, "README.md")) as file: 
    README = file.read()

# required python packages
try: 
    dir = Path(__file__).absolute().parent
    with open(os.path.join(dir, "requirements.txt"), encoding='utf-8') as file: 
        packages = file.readlines()
    REQUIREMENTS = [package.strip() for package in packages]
except FileNotFoundError:
    REQUIREMENTS =[]


DESCRIPTION = "Sage is a python package that offers a detailed overview of folder contents and streamlines the process of copying and managing directories."
LONG_DESCRIPTION = README




# setting up
setup(
    name="sage_directory",
    version=VERSION,
    author="Maxine Attobrah",
    author_email="maxineattobrah@gmail.com",
    url = "https://github.com/maxineattobrah/Sage",
    description=DESCRIPTION,

    long_description=LONG_DESCRIPTION,
    # packages = find_packages(),
    install_requires = REQUIREMENTS,
    long_description_content_type='text/markdown',
    keywords=["python","folder overview","folder management", "folder analysis","batch operations", "data science utility","data engineering utility", "IT operations"],
    classifiers=[
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python :: 3',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: Unix',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    platforms="any"

)