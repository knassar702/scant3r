__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from core.libs import post_data,urlencoder,bad,force_insert_to_params_urls
from urllib.parse import urlparse # url parsing

def start(opts,url,http,methods=['GET','POST']):
    for method in methods:
        v = force_insert_to_params_urls(url,'http://burpcollaborator.net/')
        for nurl in v:
            for param in nurl.split('?')[1].split('&'):
                if method == 'GET':
                    r = http.send(method,nurl.replace(param,param))
                else:
                    r = http.send(method,url.split('?')[0],body=urlparse(url).query)
                if 'Burp Collaborator Server' in r.content.decode('utf-8'):
                    print(f'[SSRF]:> {method} | {nurl}')
                    return {method:nurl}

