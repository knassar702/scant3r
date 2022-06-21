import concurrent.futures
import logging
from typing import Dict, List
from urllib.parse import urljoin

import tldextract

from scant3r.core.data import FIREBASE_URL
from scant3r.core.data import TLD as TLD_PAYLOADS
from scant3r.core.requester import httpSender
from scant3r.core.utils import dump_request, dump_response
from scant3r.modules.scan import Scan

log = logging.getLogger("scant3r")


class Main(Scan):
    def __init__(self, http: httpSender, url: str, convert_body: bool = False, **_):
        self.opts = {
            "url": url,
        }
        super().__init__(http, "recon", convert_body)

    def scan(self, target_host: str) -> Dict[str, str]:
        firebase = FIREBASE_URL % target_host
        report = {"host": firebase, "read": {}, "write": {}}
        read_request = self.http.send(urljoin(firebase, "/.json"), "GET")
        if read_request.__class__.__name__ == "Response":
            log.debug(f"Check for Read permission -> {firebase}")
            if read_request.status_code == 200:
                # check read permission
                report["read"]["url"] = urljoin(firebase, "/.json")
                report["read"]["content_length"] = (len(read_request.text),)
                report["read"]["content_length"] = len(read_request.text)
                report["read"]["status"] = 200
                report["read"]["request"] = dump_request(read_request)
                report["read"]["response"] = dump_response(read_request)

            log.debug(f"Check for Write permission -> {firebase}")
            write_request = self.http.send(
                urljoin(firebase, "/firebase/security.json"),
                method="PUT",
                body={"msg": "scant3r"},
                org=False,
            )

            if write_request.__class__.__name__ == "Response":
                # check write permission
                if write_request.status_code == 200:
                    report["write"]["url"] = urljoin(
                        firebase, "/firebase/security.json"
                    )
                    report["write"]["write"] = True
                    report["write"]["content_length"] = len(read_request.text)
                    report["write"]["status"] = 200
                    report["write"]["request"] = dump_request(read_request)
                    report["write"]["response"] = dump_response(read_request)

        return report

    def start(self) -> Dict[str, List[str]]:
        host = tldextract.extract(self.opts["url"]).domain
        all_hosts = [host]
        tasks = []
        report = {"module": "firebase"}
        for tld in TLD_PAYLOADS:
            all_hosts.append(host + tld.rstrip())
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for target_host in all_hosts:
                tasks.append(executor.submit(self.scan, target_host))

        for future in concurrent.futures.as_completed(tasks):
            future_output = future.result()
            report_msg = []
            if (
                len(future_output.get("read")) > 0
                or len(future_output.get("write")) > 0
            ):
                if future_output.get("read"):
                    report_msg.append(
                        f":mag: The reading permission is [red]enabled[/red]"
                    )
                if future_output.get("write"):
                    report_msg.append(
                        f":writing_hand:  The writing permission is [red]enabled[/red]"
                    )
                self.show_report(
                    "\n",
                    f":unlock: Open Firebase on [bold yellow]{future_output.get('host')}[/bold yellow]",
                    *report_msg,
                )
                report.update(future_output)
        return report
