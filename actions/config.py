from dotenv import load_dotenv

load_dotenv(verbose=True, override= True)

import os 

rest_api_host=os.environ.get("REST_API_HOST","localhost:8000/")
rest_api_schema=os.environ.get("REST_API_SCHEMA","http")
