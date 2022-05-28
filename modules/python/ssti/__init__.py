from typing import Any, Dict

from core.data import SSTI as SSTI_PAYLOADS
from core.requester import httpSender
from core.utils import insert_to_params_urls, dump_response, random_str
from modules.python.scan import Scan


class Main(Scan):
    def __init__(self, opts: Dict[str, Any], http: httpSender):
        super().__init__(opts, http, "scanning")

    def start(self) -> Dict[str, str]:
        report = {}
        for method in self.opts["methods"]:
            for payload in SSTI_PAYLOADS:
                reflect_payload = random_str(3)
                new_url = insert_to_params_urls(self.opts["url"], f"scan{reflect_payload}r")
                self.log.debug(f"SSTI: GENERATE A NEW URL: {new_url}")
                response = self.send_request(method, new_url, self.opts["url"])
                if response.__class__.__name__ == "Response":
                    raw_response = dump_response(response)
                    if reflect_payload in raw_response:
                        self.log.debug(f"REFLECTED {payload} on {response.url}")
                        self.log.debug("SSTI: MATCHING  WITH scan10tr")

                        new_url = insert_to_params_urls(self.opts["url"], payload)
                        response = self.send_request(method, new_url)
                        if response.__class__.__name__ == "Response":
                            raw_response = dump_response(response)
                            if "scan10tr" in dump_response(response):
                                self.log.debug(f"SSTI: MATCHED {response.url}")
                                report = {
                                    "name": "Server-Side template injection",
                                    "url": response.url,
                                    "payload": payload,
                                    "matching": "scan10tr",
                                }
                                self.show_report(**report)
        return report
