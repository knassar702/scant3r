#!/usr/bin/env python3
from logging import getLogger
from modules import Scan
from importlib import import_module
from glob import glob
from urllib.parse import urljoin
from core.libs import alert_bug, extract_headers
import concurrent.futures


log = getLogger('scant3r')


class Cve(Scan):
    def __init__(self,opts,http):
        super().__init__(opts,http)

    def start(self) -> dict:
        results = []
        # load python CVE modules
        for module in glob('modules/python/cve/list/python/CVE*.py'):
            module = 'modules.python.cve.list.python.' + module.split('/')[-1].rstrip('.py')
            module = import_module(module)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                results.append(executor.submit(module.main(self.opts['url'],self.http)))
        # load YAML CVE templates
        for template in glob('modules/cve/list/templates/CVE*.yaml'):
            template = self.open_yaml_file(template)
            log.debug('parsing CVE template')
            name = template['id']
            methods = template['request']['method']
            paths = template['request']['paths']
            body = template['request']['body']
            match = template['request']['match']
            all_headers = template['request']['headers']
            follow_redirects = template['request']['follow_redirects']

            if all_headers:
                headers = {}
                for header in all_headers:
                    for the_header,the_value in header.items():
                        headers[the_header] = the_value
            else:
                headers = {}
            if body == None: body = {}
            urls = []
            if paths:
                for path in paths:
                    urls.append(urljoin(url,path))
            else:
                urls.append(self.opts['url'])
            for url in urls:
                for method in methods:
                    request = self.http.send(method,url,allow_redirects=follow_redirects,headers=headers)
                    if type(request) != list:
                        if match[1]['regex'] == True:
                            finder = re.findall(match[0]['word'],request.text)
                            if finder:
                                alert_bug(name,request,match=finder,regex=True)
                        else:
                            if match[0]['word'] in request.text:
                                alert_bug(name,request,match=match[0]['word'],regex=False)

