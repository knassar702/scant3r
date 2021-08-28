from secrets import token_bytes
from base64 import b64encode


class OOB:
    def __init__(self,http):
        self.http = http
        self.last_results = []
        self.key = ""
        self.host = ""

    def poll(self,_all=False) -> list :
        req = self.http.custom(url='https://odiss.eu:1337/events',headers={"Authorization":f"Secret {self.key}"})
        if len(req.json()['events']) != self.last_results:
            self.last_results = len(req.json()['events'])
            return self.last_results
        if _all:
            return self.last_results

        return []
    
    def new(self) -> str:
        self.key = b64encode(token_bytes(32)).decode()
        req = self.http.custom(url='https://odiss.eu:1337/events',headers={"Authorization":f"Secret {self.key}"})
        self.host = req.json()['id'] + '.odiss.eu'
        return self.host
