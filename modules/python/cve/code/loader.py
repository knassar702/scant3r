#from modules import transform_path_to_module_import
from logging import getLogger
from importlib import import_module
from glob import glob
from urllib.parse import urljoin
from core.libs import alert_bug
import concurrent.futures , re , yaml

log = getLogger('scant3r')

def python_loader(self):
    for module in glob(f'templates/python/*.py'):
        module_imported = import_module(self.transform_path_to_module_import(module))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            log.debug(f'{self.transform_path_to_module_import(module)} started')
            executor.submit(module_imported.main(self.opts['url'], self.http))

def yaml_loader(self):
    
    for template in glob(f'templates/yaml/*.yaml'):
        template = yaml.safe_load(open(template,'r'))
        template_opts = template.copy()
        for data,value in template_opts.get('request').copy().items():
            if value:
                pass
            else:
                template_opts['request'][data] = {}

        log.debug('parsing Scanning template')
        request = template_opts.get('request')
        match = request.get('match')
        paths = request.get('paths')
        name = template_opts.get('id')
        urls = set()
        if paths:
            for path in paths:
                log.debug(f'Join Path : {path}')
                urls.add(urljoin(self.opts['url'],path))
        else:
            urls.add(self.opts['url'])
        log.debug(f'{template["id"]} Started')
        for url in urls:
            for method in request.get('method',['GET']):
                response = self.http.send(method=method,url=self.opts['url'],body=request.get('body',{}),headers=request.get('headers',{}),allow_redirects=request.get('follow_redirects',False))
                if type(response) != list:
                    if match['regex'] == True:
                        finder = re.findall(match['word'], response.text,re.DOTALL)
                        if finder:
                            if len(''.join(finder)) > 700:
                                for i in finder:
                                    if len(i) > 700:
                                        finder.remove(i)
                                        finder.append(i[0:700] + '   <<<<< ETC >>>>>')
                            alert_bug(name, response,match=match['word'],regex=True, found=finder)
                    else:
                        if match['word'] in response.text:
                            alert_bug(name, response,match=match['word'],regex=False)
