###### WIP
This branch to focus on token-based authentication using OAuth2 - JWT tokens<br>
a) Aim is /token endpoint where you "log in" with a username/password to get a JWT.<br>
b) A secured /data endpoint that needs a valid Bearer token in the Authorization header<br>


## Host an API

### Start API Server [use either method]
a) `uvicorn main:app --reload` <br>
b) `fastapi run .\main.py` OR to multiprocess `fastapi run --workers 4 .\main.py`<br>



### API Client Call : Phase 1
a) Check notebook : `client_script.ipynb`
```
import requests
API_KEY = "XXXX"
headers = {
    "X-API-Key": API_KEY
}
response = requests.get("http://127.0.0.1:8000/data", headers=headers)
data = response.json()
```


### Reference : 
https://fastapi.tiangolo.com/#create-it

