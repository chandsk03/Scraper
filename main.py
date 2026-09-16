from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from plugins.automation import scrap
from plugins.database import add_userdata
app = FastAPI()

class login_data(BaseModel):
    username : str
    password : str

@app.post("/login")
def login(Data : login_data):
    result = scrap(Data.username, Data.password)
    # add_userdata(result)
    return{"Data": Data, "Result": result}

@app.get("/")
def home():
    return{"API running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)