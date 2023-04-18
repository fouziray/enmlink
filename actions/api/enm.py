import requests
from typing import Text
import logging
from .. import config
logger = logging.getLogger(__name__)

class CommandEventAPI:
    def __init__(self,
    schema: Text=  config.rest_api_schema,
    host: Text= config.rest_api_host
    ):
        self.schema = schema
        self.host = host
    
    def getMessage(self, message) -> requests.Response:
        url = f"{self.schema}://{self.host}/reponse/{message}"
        print(url)
        response = requests.get(url)
        print(response.content)
        return response