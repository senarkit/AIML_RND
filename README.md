

## Host an API

### Start API Server [use either method]
a) `uvicorn main:app --reload`
b) `fastapi run .\main.py` OR to multiprocess `fastapi run --workers 4 .\main.py`



### API Client Call : Phase 1
a) Check notebook : `client_script.ipynb`
```
import requests
response = requests.get("http://127.0.0.1:8000/data")
data = response.json()
```


### Reference : 
https://fastapi.tiangolo.com/#create-it