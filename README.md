
## Start Server
`uvicorn main:app --reload` <br>

### Start a client
In a separate terminal <br>
`python client.py`


Steps : <br>
1. Install the requirements into a virtual env <br>
`py -3.11 -m venv venv` <br>
`pip install -r requirements` <br>
2. Start Server API <br>
`uvicorn main:app --reload` <br>
3. Below is the API Structure at : http://127.0.0.1:8000/docs#/ <br>
![FastAPI Doc](./data/apidoc_snap.png) <br>
4. Run Client Script <br>
In separate terminal run : `python client.py`