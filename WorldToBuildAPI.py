import requests
import json
from enum import Enum

class wtbRequestType(Enum):
    Player = 1
    Club = 2
    World = 3

class WorldToBuildAPIClient():
    def getInfoByID(self, requestType : wtbRequestType, ID : int):
        if ID < 0:
            return None
        
        url = None
        match requestType:
            case wtbRequestType.Player:
                url = 'https://api.worldtobuild.com/WebService/Player/FetchPlayerDataById?PlayerID='+str(ID)
            case wtbRequestType.Club:
                url = 'https://api.worldtobuild.com/WebService/Club/FetchClubDataById?ClubID='+str(ID)
            case wtbRequestType.World:
                url = 'https://api.worldtobuild.com/WebService/World/FetchWorldDataById?WorldID='+str(ID)
                       
        url = url + str(ID)

        return requests.get(url)


