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
    
    def saveMoState(self,stateManagedObject)-> requests.Response:
        url = f"{self.schema}://{self.host}/stateMo/"
        payload1={'NodeId': 'BLDEVO2', 'BscFunctionId': '1', 'BscMId': '1', 'GeranCellMId': '1', 'GeranCellId': '09620D', 'ChannelGroupId': '0', 'connectedG12Tg': 'null', 'connectedG31Tg': 'SubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1020', 'state': 'ACTIVE'}
        payload2={'NodeId': 'BLDEVO2', 'BscFunctionId': '1', 'BscMId': '1', 'GeranCellMId': '1', 'GeranCellId': '09620E', 'ChannelGroupId': '0', 'connectedG12Tg': 'null', 'connectedG31Tg': 'SubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1120', 'state': 'ACTIVE'}
        payload3={'NodeId': 'BLDEVO2', 'BscFunctionId': '1', 'BscMId': '1', 'GeranCellMId': '1', 'GeranCellId': '09620F', 'ChannelGroupId': '0', 'connectedG12Tg': 'null', 'connectedG31Tg': 'SubNetwork=ONRM_ROOT_MO,SubNetwork=GRAN,MeContext=BLDEVO2,ManagedElement=BLDEVO2,BscFunction=1,BscM=1,Bts=1,G31Tg=1220', 'state': 'ACTIVE'}

        response = requests.post(url=url,json=payload1)
        