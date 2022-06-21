# band resource load SCANNER
import time
from typing import List, Dict

from scant3r.core.oast import Interactsh
from scant3r.core.requester import httpSender
from scant3r.core.utils import dump_request, dump_response, insert_to_params_urls
from scant3r.modules.scan import Scan

proto = (
    "http",
    "https",
)


class Main(Scan):
    def __init__(
        self,
        http: httpSender,
        methods: List[str],
        url: str,
        callback_time: int,
        convert_body: bool = False,
        **_,
    ):
        self.opts = {
            "url": url,
            "methods": methods,
            "callback_time": callback_time,
        }
        super().__init__(http, "scanner", convert_body)

    def start(self) -> Dict[str, str]:
        report = {}
        for method in self.opts["methods"]:
            callback = Interactsh()
            for protocole in proto:
                new_url = insert_to_params_urls(
                    self.opts["url"], f"{protocole}://{callback.domain}", True
                )
                response = self.send_request(method, new_url)
                if response.__class__.__name__ == "Response":
                    time.sleep(self.opts.get("callback_time", 2))
                    callback_results = callback.pull_logs()
                    if len(callback_results) > 0:
                        report = {
                            "module": "req_callback",
                            "name": "Out-of-band resource load",
                            "url": response.url,
                            "request": dump_request(response),
                            "response": dump_response(response),
                            "payload": f"{protocole}://{callback.domain}",
                            "callback": callback_results,
                        }
                        report_msg = (
                            "\n",
                            ":satellite: Out-of-band resource load",
                            f":dart: The Effected URL: {response.url}",
                            f":syringe: The Used Payload: [bold red]{protocole}://{callback.domain} [/bold red]",
                            f":mag: Callback log: [bold yellow] {callback_results} [/bold yellow]",
                        )
                        self.show_report(*report_msg)
        return report
