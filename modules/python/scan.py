from typing import Union
from urllib.parse import urlparse
from logging import getLogger
from core.libs import Http
from requests.models import Response

PATH_PYTHON_MODULE = 'modules/python/'

class Scan: 
    def __init__(self, opts: dict, http: Http, path: str = PATH_PYTHON_MODULE): 
        self.opts = opts 
        self.http = http
        self.path = path 
        self.log = getLogger('scant3r')
        
    def open_yaml_file(self,file_name: str): 
        try:
            read_file = open(file_name,'r')
        except Exception as e:
            self.log.error(e)
            return None

    def send_request(self, method: str, url: str, second_url: Union[str, None] = None) -> Response:
        if method == 'GET':
            return self.http.send(method, url)
        if second_url is None:
            return self.http.send(method, second_url.split('?')[0], body = urlparse(url).query)
        return self.http.send(method, url.split('?')[0], body = urlparse(url).query)

