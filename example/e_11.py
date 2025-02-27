import os
import logfire
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logfire.configure(token=LOGFIRE_TOKEN)

app = Flask(__name__)
logfire.instrument_flask(app)

@app.route("/", methods=['GET'])
def home():
    return "<h1>Hello, World!</h1>"

@app.route("/val", methods=['GET'])
def albert():
    return "<h1>Val!</h1>"

if __name__ == "__main__":
    app.run(debug=True)