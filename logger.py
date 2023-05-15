import time
import re
from time import ctime
import requests
import json

class Maps:
    STATION = 'Station_P'
    BRIGHT_SANDS = 'MP_Map01_P'
    CRESCENT_FALLS = 'MP_Map02_P'
    THARIS_ISLAND = 'MP_AlienCaverns_P'
    PLAYABLE = (BRIGHT_SANDS, CRESCENT_FALLS, THARIS_ISLAND)
    ICONS = {
        STATION: None,
        BRIGHT_SANDS: 'https://cdn.discordapp.com/attachments/497220074101276682/1093700948297261056/image.png',
        CRESCENT_FALLS: 'https://cdn.discordapp.com/attachments/497220074101276682/1093700998696026122/image.png',
        THARIS_ISLAND: 'https://cdn.discordapp.com/attachments/1093694623957917776/1104121582655393883/image.png'
    }
    NAMES = {
        STATION: 'Station',
        BRIGHT_SANDS: 'Bright Sands',
        CRESCENT_FALLS: 'Crescent Falls',
        THARIS_ISLAND: 'Tharis Island'
    }

class Cyclogger:
    instances = []
    servers = []

    def __init__(self, logfolder: str = None) -> None:
        with open('data.json') as dfile:
            self.data = json.load(dfile)
        self.name = self.data.get('name', '')
        self.path = self.data.get('location', '')
        self.url = self.data.get('url', '')
        with open(self.path, "r") as file:
            file.seek(0,2)
            while True:
                try:
                    line = file.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    self.parseLine(line = str(line))
                except Exception:
                    pass

    def isServer(self, sid: str, smap: str) -> None:
        print(f'JOIN => {ctime()}: {sid} on {smap}')

        self.logServer(sid = sid, smap = smap)
        if self.url:
            self.sendServer(sid = sid, smap = smap)
        if len(self.servers) > 1 and (ls := self.servers[-2:] and ls[0].sid == ls[1].sid):
            print('SAME => Joined same server as last')

    def sendServer(self, sid: str, smap: str) -> None:
        data = {
            "content": None,
            "embeds": [
                {
                "title": f"Deployed to {Maps.NAMES.get(smap, '')}",
                "description": f"Server ID: \n{sid}",
                "color": 4876156,
                "author": {
                    "name": f"{self.name}"
                },
                "thumbnail": {
                    "url": f"{Maps.ICONS.get(smap, '')}"
                }
                }
            ],
            "avatar_url": "https://yt3.googleusercontent.com/CJ4b0OKg5izpM6wl0LxIOcZ9cixUtOM0ZO6_-4B8lQnAJTjkzb3Th6pXVneSV1wPFcSo_B3bl8o=s900-c-k-c0x00ffffff-no-rj",
            "attachments": [],
            "name": "The Cycle: Frontier Stats"
        }
        result = requests.post(self.url, json = data)
        

    def logServer(self, sid: str, smap: str) -> None:
        if smap in Maps.PLAYABLE:
            self.servers.append({
                sid: sid,
                smap: smap
            })

    def parseLine(self, line: str) -> None:
        for r, f in {
            r'LogYMatch: AYGameState_Base::OnRep_BattleServerId SessionId (.*) Map:(MP_Map01_P|MP_Map02_P|MP_AlienCaverns_P|Station_P)' : self.isServer,
        }.items():
            if match := re.search(r, line, re.IGNORECASE):
                f(*match.groups())

    def findLogfileRecent(self, folder: str) -> str:
        return 'latest.log'

def main():
    logger = Cyclogger()

if __name__ == "__main__":
    main()
