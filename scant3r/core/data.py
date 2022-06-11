import os.path
from pathlib import Path

from rich.console import Console

base_dir = Path(__file__).resolve().parent.parent

# interact.sh public servers
INTERACT_SERVERS = (
    "interact.sh",
    "oast.pro",
    "oast.live",
    "oast.site",
    "oast.online",
    "oast.me",
)
LOGGING_FORMAT = "%(name)-12s: %(levelname)-8s %(message)s"
LOGGING_FILE = os.path.join(Path.home(), ".scant3r.log")
CLEAR_LOGGING_FILE = True


# ENABLED Modules ( after using `-m all` option)
ENABLED_MODS = ("ssti", "firebase", "req_callback", "xss")

# CLI
LOGO = open(f"{base_dir}/conf/logo.txt", "r").read()
console = Console()
FIREBASE_URL = "https://%s.firebaseio.com"

# SQLI PAYLOADS
SQLI_PAYLOADS = tuple(Path(f"{base_dir}/db/txt/sqli.txt").read_text().splitlines())
SQL_ERRORS = tuple(Path(f"{base_dir}/db/txt/sqli_errors.txt").read_text().splitlines())

PATH_TRAVERSAL = tuple(
    Path(f"{base_dir}/db/txt/traversal.txt").read_text().splitlines()
)
TLD = tuple(Path(f"{base_dir}/db/txt/tld.txt").read_text().splitlines())

# RCE PAYLOADS
RCE_PAYLOADS_PWD = tuple(Path(f"{base_dir}/db/txt/pwd.txt").read_text().splitlines())
RCE_PAYLOADS_PASSWD = tuple(
    Path(f"{base_dir}/db/txt/passwd.txt").read_text().splitlines()
)

SSTI = tuple(Path(f"{base_dir}/db/txt/ssti.txt").read_text().splitlines())
SSRF_PARAMS = tuple(
    Path(f"{base_dir}/db/txt/ssrf_parameters.txt").read_text().splitlines()
)

# XSS WORDLIST
XSS_JS_FUNC = tuple(Path(f"{base_dir}/db/txt/js_func.txt").read_text().splitlines())
XSS_JS_VALUE = tuple(Path(f"{base_dir}/db/txt/js_value.txt").read_text().splitlines())

XSS_TAGS = tuple(Path(f"{base_dir}/db/txt/xss.txt").read_text().splitlines())
XSS_ATTR = tuple(Path(f"{base_dir}/db/txt/xss_attr.txt").read_text().splitlines())

CSP_LIST = (
    ".doubleclick.net",
    ".googleadservices.com",
    "cse.google.com",
    "accounts.google.com",
    "*.google.com",
    "www.blogger.com",
    "*.blogger.com",
    "translate.yandex.net",
    "api-metrika.yandex.ru",
    "api.vk.comm",
    "*.vk.com",
    "*.yandex.ru",
    "*.yandex.net",
    "app-sjint.marketo.com",
    "app-e.marketo.com",
    "*.marketo.com",
    "detector.alicdn.com",
    "suggest.taobao.com",
    "ount.tbcdn.cn",
    "bebezoo.1688.com",
    "wb.amap.com",
    "a.sm.cn",
    "api.m.sm.cn",
    "*.taobao.com",
    "*.tbcdn.cn",
    "*.1688.com",
    "*.amap.com",
    "*.sm.cn",
    "mkto.uber.com",
    "*.uber.com",
    "ads.yap.yahoo.com",
    "mempf.yahoo.co.jp",
    "suggest-shop.yahooapis.jp",
    "www.aol.com",
    "df-webservices.comet.aol.com",
    "api.cmi.aol.com",
    "ui.comet.aol.com",
    "portal.pf.aol.com",
    "*.yahoo.com",
    "*.yahoo.jp",
    "*.yahooapis.jp",
    "*.aol.com",
    "search.twitter.com",
    "*.twitter.com",
    "twitter.com",
    "ajax.googleapis.com",
    "*.googleapis.com",
)


BLOCK_CONTENT_TYPE = (
    "application/json",
    "application/javascript",
    "text/javascript",
    "text/plain",
    "text/css",
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/gif",
    "application/rss+xml",
)
