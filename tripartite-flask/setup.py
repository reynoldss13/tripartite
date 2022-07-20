# Used to setup a virtual environment and install all dependencies when
# a developer has cloned the tripartite-flask repo
# To run:
#   - right click setup.py file
#   - select 'run python file in terminal'

import os

def setup():
    os.system('python -m venv venv')
    os.system('venv\Scripts\pip install flask')
    os.system('venv\Scripts\pip install apscheduler')
    os.system('venv\Scripts\pip install bcrypt')
    os.system('venv\Scripts\pip install bson')
    os.system('venv\Scripts\pip install faker')
    os.system('venv\Scripts\pip install flask_cors')
    os.system('venv\Scripts\pip install flask_jwt_extended')
    os.system('venv\Scripts\pip install pymongo')

setup()