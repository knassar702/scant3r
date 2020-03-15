import logging
import requests,urllib3
from core.colors import *
logging.basicConfig(
	format=f'{bold}[{cyan}%(asctime)s{end}{bold}]{gray}[{end}{bold}{green}%(levelname)s{gray}]{end} %(message)s',datefmt='%H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
"""
logger.info('SQLI not found')
logger.debug('This a Debug Message')
logger.warning('Im Sorry i can hack this system')
logger.error('HTTP ERROR')
logger.critical('Internet Down')
"""