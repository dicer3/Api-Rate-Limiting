Open https://www.python.org/downloads/release/python-368/
Choose executable installer option for installing python
add this path to enviorment variables C:\Users\{Your PC name}\AppData\Local\Programs\Python\Python36

Isnstalling PiP-
open https://bootstrap.pypa.io/get-pip.py
Save this file
Run this file 
Pip would be installed

Create Virtual Enviorment

pip install virtualenv
pip install virtualwrapper-win
mkvirtualenv BO_project(virtualenv name)

to deactivate Virtual Enviorment

deactivate

To activate Virtual Enviorment

workon BO_project

Open Redis Folder
start redis-server.exe to start redis server

To Run Flask Server
Execute the Following commands on Command Prompt
set FLASK_APP=RateLimiting.py
flask run --host=0.0.0.0
