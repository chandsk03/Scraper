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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
