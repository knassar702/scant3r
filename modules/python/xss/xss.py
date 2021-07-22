#!/usr/bin/env python3
from core.libs import remove_dups_urls, random_str, alert_bug, insert_to_params_urls, Http
from urllib.parse import urlparse
from wordlists import XSS
from modules import Scan

class Xss(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        self.payloads = XSS(opts['blindxss']).payloads
        
    def check_method(self, methods: list, url: str) -> dict:
        method_allowed = dict()
        for method in methods:
            method_allowed[method] = {}
            response = self.http.send(method,url)
            if response != 0 and response.status_code != 405:
                method_allowed[method] = {url: response.status_code}
        return method_allowed
    
    def start(self):
        bugs = []
        for method in self.opts['methods']:
            list_potential_vulnerable_url: list = []
            txt = f'scan{random_str(3)}tr'
            # Create a list of url with value for each parameter 
            # if text is display append it in ref list
            target_url = self.transform_url(self.opts['url'])
            list_url = remove_dups_urls(insert_to_params_urls(target_url, txt))
            for url in list_url:
                response = self.send_request(method, url)
                if response != 0 and txt in response.text:
                    list_potential_vulnerable_url.append(url)
            
            for potential_vulnerable_url in list_potential_vulnerable_url:
                for P in self.payloads:
                    # remove new lines from payloads
                    P = P.rstrip()  
                    # replace the text by the payload
                    payload_url = potential_vulnerable_url.replace(txt,P)
                    response = self.send_request(method, payload_url)
                    # If the payload in the response show this message
                    if response != 0 and P in response.text:
                        bugs.append({
                            'params':urlparse(payload_url).query,
                            'payload':P,
                            'http': response
                        })
                        break
                    
        result_list = []
        for bug in bugs:             
            result_list.append(alert_bug('XSS',**bug))
        
        return result_list

