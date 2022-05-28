import re
from typing import Any, Dict

from rich.syntax import Syntax

from core.data import SSTI as SSTI_PAYLOADS
from core.requester import httpSender
from core.utils import dump_response, insert_to_params_urls, random_str
from modules.python.scan import Scan


class Main(Scan):
    def __init__(self, opts: Dict[str, Any], http: httpSender):
        super().__init__(opts, http, "scanning")

    def start(self) -> Dict[str, str]:
        report = {}
        for method in self.opts["methods"]:
            # check for reflected params
            reflect_payload = random_str(3)
            new_url = insert_to_params_urls(self.opts["url"], f"scan{reflect_payload}r")
            self.log.debug(f"SSTI: GENERATE A NEW URL: {new_url}")
            response = self.send_request(method, new_url)
            if response.__class__.__name__ == "Response":
                raw_response = dump_response(response)
                if reflect_payload in raw_response:
                    self.log.debug(f"REFLECTED {reflect_payload} on {response.url}")
                    self.log.debug("SSTI: MATCHING  WITH scan10tr")

                    # scan the target with ssti payloads
                    for payload in SSTI_PAYLOADS:
                        new_url = insert_to_params_urls(self.opts["url"], payload)
                        response = self.send_request(method, new_url)
                        if response.__class__.__name__ == "Response":
                            raw_response = dump_response(response)
                            if "scan10tr" in raw_response:
                                self.log.debug(f"SSTI: MATCHED {response.url}")
                                report = {
                                    "name": "Server-Side template injection",
                                    "url": response.url,
                                    "payload": payload,
                                    "matching": "scan10tr",
                                }
                                report_msg = [
                                    "\n",
                                    ":fire: Server-Side template injection",
                                    f":dart: The Effected URL: {response.url}",
                                    f":syringe: The Used Payload: [bold red] {payload} [/bold red]",
                                    ":mag: Matched with : [bold yellow] scan10tr [/bold yellow]",
                                ]
                                the_location = ""
                                for m in re.finditer("scan10tr", raw_response):
                                    length = (m.end() + m.start()) - len(raw_response)
                                    if length < len(raw_response):
                                        right_location = m.start() - 20
                                        the_location = Syntax(
                                            raw_response[right_location : m.end()],
                                            "html",
                                        )
                                    else:
                                        the_location = Syntax(
                                            raw_response[m.start() : m.end()], "html"
                                        )
                                report_msg.append(the_location)
                                self.show_report(*report_msg)
        return report
