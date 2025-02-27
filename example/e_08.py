import os
import logfire
from dotenv import load_dotenv

load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logfire.configure(token=LOGFIRE_TOKEN)

logfire.info('Hello, {name}!', name='World')

if __name__ == "__main__": 
    pass