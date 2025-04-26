
## Start Server
`uvicorn main:app --reload` <br>

### Start a client
In a separate terminal <br>
`python client.py`


<b>Steps :</b> <br>
1. Install the requirements into a virtual env <br>
Create Env : `py -3.11 -m venv venv` <br>
Activate : `.\venv\Scripts\activate` <br>
Install Reqs : `pip install -r requirements` <br><br>
2. Start Server API <br>
`uvicorn main:app --reload` <br><br>
3. Below is the API Structure at : http://127.0.0.1:8000/docs#/ <br>
![FastAPI Doc](./data/apidoc_snap.png) <br><br>
4. Run Client Script <br>
In separate terminal run : `python client.py`<br><br>
5. The Code can : <br>
a) Register / SignUp a new user. If the user already exists it skips updating <br>
![Client Run - Terminal](./data/client_terminal.png) <br>
b) It updates a SQL DB at the backend. Use the below code or check Notebook : `peek_db.ipynb` <br>
'''
import pandas as pd
import sqlite3
conn = sqlite3.connect("./data/db.sqlite3")
df_users = pd.read_sql_query("SELECT * FROM Users", conn)
df_token = pd.read_sql_query("SELECT * FROM tbl_token", conn)
print(df_token.tokenVal.values[0])
'''
<br>
c) Additionally corresponding websocket and http endpoint is available in transcriber.py