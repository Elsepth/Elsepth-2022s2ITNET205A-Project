# Requirements
* Python 3.8+
* Pip
* virtualenv

# instructions
* Global install virtualenv
```
$ sudo pip3 install virtualenv 
```
* run virtualenv 
```
$ virtualenv .venv
```
* activate virtualenv
```
$ source .venv/bin/activate
(.venv)$
```
* install required modules (requirements.txt is created via `pip freeze > requirements.txt`)
```
(.venv)$ pip install -r requirements.txt
```
* run python app
```
(.venv)$ python main.py
```