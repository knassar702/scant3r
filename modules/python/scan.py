from urllib.parse import urlparse as ur
PATH_PYTHON_MODULE = 'modules/python/'

class Scan: 
    def __init__(self, opts, http, path = PATH_PYTHON_MODULE): 
        self.opts = opts 
        self.http = http
        self.path = path 
        
    def open_yaml_file(self): 
        pass
    
    def send_request(self, method: str, url): 
        if method == 'GET': 
            return self.http.send(method, url)
        return self.http.send(method, url.split('?')[0], body=ur(url).query)