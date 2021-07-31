import nimporter
from core.libs import Http
from .hackerman import main as Url
from logging import getLogger


log = getLogger('scant3r')

def main(opts: dict,http: Http) -> str:
    c = Url(opts['url'])
    log.info(f"NIM: YOUR URL: {c}")
    return c
