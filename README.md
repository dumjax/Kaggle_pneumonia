# kag_rsna

## Before starting

### Create virtualenvironment folder

mkdir venv3

### install python3 in case (If needed choose a specific version of python (eg 3.5 etc)

https://brew.sh/

brew install python3

### Create virtualenvironment (if you know the exact python you want to use you can replace python3 by its complete path, for example usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7)

virtualenv --system-site-packages -p python3 venv3

### Activate the virtual environment

source ./venv3/bin/activate


-- Install needed libraries

pip install -r requirements.txt

### NOTE 

the folder venv3 will not be commited as it is contained in the file .gitignore


