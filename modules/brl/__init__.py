# band resource load SCANNER
import time
from typing import Any, Dict

from core.requester import httpSender
from core.oast import Interactsh
from core.utils import dump_request, dump_response, insert_to_params_urls 
from modules.scan import Scan

proto = [
    "http",
    "https",
]

class Main(Scan):
    def __init__(self, opts: Dict[str, Any], http: httpSender):
        super().__init__(opts, http, "scanning")

    def start(self) -> Dict[str, str]:
        report = {}
        for method in self.opts["methods"]:
            callback = Interactsh()
            for protocole in proto:
                new_url = insert_to_params_urls(self.opts["url"], f"{protocole}://{callback.domain}")
                response = self.send_request(method, new_url)
                if response.__class__.__name__ == "Response":
                    time.sleep(0.3)
                    if callback.pull_logs():
                        report = {
                            "module": "ssti",
                            "name": "Server-Side template injection",
                            "url": response.url,
                            "request": dump_request(response),
                            "response": dump_response(response),
                            "paylod": f"{protocole}://{callback.domain}",
                            "callback": callback.pull_logs(),
                        }
                        report_msg = [
                            "\n",
                            ":satellite: Out-of-band resource load",
                            f":dart: The Effected URL: {response.url}",
                            f":syringe: The Used Payload: [bold red]{protocole}://{callback.domain} [/bold red]",
                            ":mag: Callback log: [bold yellow] {callback.pull_logs()} [/bold yellow]",
                        ]
                        self.show_report(*report_msg)
        return report

