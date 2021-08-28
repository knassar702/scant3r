#!/usr/bin/env python3
from logging import getLogger
from modules import Scan
from importlib import import_module
from glob import glob
from urllib.parse import urljoin
from core.libs import alert_bug
import concurrent.futures
from core.libs import Http
import re 

log = getLogger('scant3r')

class Cve(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)

    def start(self) -> dict:
        results = []
        # load python CVE modules
        for module in glob(f'{self.path}cve/list/python/*.py'):
            nmodule = import_module(self.transform_path_to_module_import(module))
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                log.debug(f'{self.transform_path_to_module_import(module)} Started')
                results.append(executor.submit(nmodule.main(self.opts['url'], self.http)))

        # load YAML CVE templates
        for template in glob(f'{self.path}cve/list/templates/*.yaml'):
            template = self.open_yaml_file(template, False)
            log.debug('parsing Scanning template')
            name = template['id']
            methods = template['request']['method']
            paths = template['request']['paths']
            body = template['request']['body']
            match = template['request']['match']
            all_headers = template['request']['headers']
            follow_redirects = template['request']['follow_redirects']

            headers = {}
            if all_headers:
                log.debug('Add Headers')
                for header in all_headers:
                    for the_header,the_value in header.items():
                        headers[the_header] = the_value

            if body == None: body = {}

            urls = []
            if paths:
                for path in paths:
                    log.debug(f'Join Path : {path}')
                    urls.append(urljoin(self.opts['url'],path))
            else:
                urls.append(self.opts['url'])
            log.debug(f'{template["id"]} Started')
            for url in urls:
                for method in methods:
                    request = self.http.send(method, url, allow_redirects=follow_redirects, headers=headers)
                    if type(request) != list:
                        if match['regex'] == True:
                            finder = re.findall(match['word'], request.text,re.DOTALL)
                            if finder:
                                if len(''.join(finder)) > 700:
                                    for i in finder:
                                        if len(i) > 700:
                                            finder.remove(i)
                                            finder.append(i[0:700] + '   <<<<< ETC >>>>>')
                                alert_bug(name, request,match=match['word'],regex=True, found=finder)
                        else:
                            if match['word'] in request.text:
                                alert_bug(name,request,match=match['word'],regex=False)
        return {}

