###### WIP
This branch to focus on token-based authentication using OAuth2 - JWT tokens<br>
a) Aim is /token endpoint where you "log in" with a username/password to get a JWT.<br>
b) A secured /data endpoint that needs a valid Bearer token in the Authorization header<br>


## Host an API

### Start API Server [use either method]
a) `uvicorn main:app --reload` <br>
b) `fastapi run .\main.py` OR to multiprocess `fastapi run --workers 4 .\main.py`<br>



### API Client Call : 30 Mins Expiration OAuth2 JSON Web Token (Header, Payload, Signature)
Check notebook : `client_script.ipynb`


### Reference : 
https://fastapi.tiangolo.com/#create-it

