# healthCenterPortal
Portal for six health centers with predictive analytics for disease outbreaks

# Requirements
|  Install | Download links |
|--------------------------------------------|--------------------------------------------|
| Python 3.11 or latest | [Click here to downlod python](https://www.python.org/downloads/) |
| Visual Studio Code | [Click here to download xampp](https://code.visualstudio.com/) |
| Download Extension in Visual Studio Code: Python |


# Setup
1. Run command prompt and change directory to project folder.
    - mas best if yung clone mo ng repo nasa Desktop para i execute mo lang to sa command prompt 
        cd Desktop
        cd healthCenterPortal

2. Install virtual environment
```cmd
pip install virtualenv
```
3. Create virtual environment
```cmd
virtualenv env
or
python -m venv env
```
4. Activate virtual environment

if using bash:
```bash
$ source ./env/Scripts/Activate
```
if using cmd
```cmd
env
```
or
```cmd
env\scripts\activate
```
5. Install dependencies
```cmd
pip install -r requirements.txt
```
6. Collect static files. After running command wait for a while then type **yes**
```cmd
py manage.py collectstatic
```
7. Run server
```cmd
run
```
if not working
```cmd
./run
```
or
```cmd
python manage.py runserver
```
8. Server address = 127.0.0.1:8000
    for admin
    127.0.0.1:8000/admin


If you installed Vistual Studio Code and virtual environment
1. Open Project Folder
    Go to File -> Open Folder -> healthCenterPortal then Open
2. Go to View -> Command Palette (or Crtl + Shift + P)-> Type Python Interpreter -> Select it -> Select the Recommended (Mine is Python 3.11.2('env': venv) \env\Scripts\python.exe)
3. Now you can use the terminal of Visual Studio Code and instantly executes going to virtual environment
4. Just enter ./run to run the server

If you have any changes to models.py/admin.py make sure to
1. Go to terminal with env on
2. type python manage.py makemigrations
3. If no error type, python manage.py migrate
