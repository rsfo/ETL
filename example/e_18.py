import os
import logfire
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

app = FastAPI()

logfire.configure(token=LOGFIRE_TOKEN)
logfire.instrument_fastapi(app)

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/val")
def val():
    return {"message": "Val!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)