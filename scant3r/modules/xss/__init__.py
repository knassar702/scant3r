import re
from typing import Any, Dict, List

from parsel import Selector
from rich.syntax import Syntax

from scant3r.core.htmlparser import HTMLocation
from scant3r.core.requester import httpSender
from scant3r.core.utils import (
    dump_request,
    dump_response,
    insert_to_params_urls,
    random_str,
)
from scant3r.modules.scan import Scan

from .payload_gen import XSS_PAYLOADS


class Main(Scan):
    def __init__(
        self,
        http: httpSender,
        methods: List[str],
        url: str,
        convert_body: bool = False,
        **_,
    ):
        self.opts = {
            "url": url,
            "methods": methods,
        }
        super().__init__(http, "scanner", convert_body)

    def start(self) -> Dict[str, str]:
        report = {
            "module": "xss",
            "name": "Reflected Cross-site scripting",
            "found": [],
        }
        XSS = XSS_PAYLOADS([], [])
        for method in self.opts["methods"]:
            # check for reflected params
            rand_str = random_str(3)
            reflect_payload = f"scan{rand_str}r".lower()
            new_url = insert_to_params_urls(self.opts["url"], reflect_payload)
            self.log.debug(f"XSS: GENERATE A NEW URL: {new_url}")
            response = self.send_request(method, new_url)
            if response.__class__.__name__ == "Response":
                find_location = HTMLocation(reflect_payload)
                find_location.feed(response.text)
                if find_location.data:
                    self.log.debug(
                        f"REFLECTED {reflect_payload} on {response.url} | {find_location.data}"
                    )
                    for xss_location in find_location.data:
                        # scan the target with the xss payloads
                        for payload_data in XSS.generate(reflect_payload, xss_location):
                            payload = payload_data[0]
                            payload_search = payload_data[1]
                            new_url = insert_to_params_urls(self.opts["url"], payload)
                            response = self.send_request(method, new_url)
                            if response.__class__.__name__ == "Response":
                                raw_response = response.text
                                tree = Selector(text=raw_response)
                                if tree.xpath(payload_search).extract_first():
                                    self.log.debug(f"XSS: MATCHED {response.url}")
                                    report["found"].append(
                                        {
                                            "type": xss_location.value,
                                            "url": response.url,
                                            "request": dump_request(response),
                                            "response": dump_response(response),
                                            "payload": payload,
                                            "matching": payload_search,
                                        }
                                    )
                                    the_location = ""
                                    for m in re.finditer(payload, raw_response):
                                        length = (m.end() + m.start()) - len(
                                            raw_response
                                        )
                                        if length < len(raw_response):
                                            right_location = m.start() - 20
                                            the_location = Syntax(
                                                raw_response[right_location : m.end()],
                                                "html",
                                            )
                                        else:
                                            the_location = Syntax(
                                                raw_response[m.start() : m.end()],
                                                "html",
                                            )
                                    self.show_report(
                                        *(
                                            "\n",
                                            ":fire: Reflected Cross-site scripting",
                                            f":dart: The Effected URL: {response.url}",
                                            f":page_facing_up: XSS Location: {xss_location.value}",
                                            f":syringe: The Used Payload: [bold red] {payload} [/bold red]",
                                            the_location,
                                        )
                                    )
                                    break
        return report
