# Cinarra test app

Using Flask to build a API service of taxi calls with Swagger UI.


## Installation
### Create venv:

For Linux:
```
python3 -m venv /path/to/new/virtual/environment
```
For Windows:
```
c:\>c:\Python35\python -m venv c:\path\to\myenv
```
### Activate venv:

For Linux
```
$ source <venv>/bin/activate
```

For Windows: 
in cmd.exe
```
C:\> <venv>\Scripts\activate.bat
```
Install with pip:

```
$ pip install -r requirements.txt
```
 
## Run Flask
### Run flask
```
$ flask run
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/swagger`
## Flask Application Structure 
```
.
|──────schemas/
| |────__init__.py
| |────client_schema.py
| |────driver_schema.py
| |────order_schema.py
|──────static/
| |────swagger.yaml
|──────tests/
| |────__init__.py
| |────test_cllient_api.py
| |────test_cllient.py
| |────test_driver_api.py
| |────test_driver.py
| |────test_order_api.py
| |────test_order.py
|──────app.py
|──────config.py
|──────models.py
|──────order_iteracrions.py
|──────requirements.txt
|──────README.md

```

## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```


## SWAGGER settings

```
SWAGGER_DOC_URL = '/swagger'
```



