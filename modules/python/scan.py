from base64 import b64encode
from logging import getLogger
from secrets import token_bytes
from typing import Any, Dict, Union
from urllib.parse import parse_qsl, urlparse

from requests.models import Response
from yaml import safe_load

from core.data import base_dir, console
from core.requester import httpSender

PATH_PYTHON_MODULE = f"{base_dir}/modules/python/"


class Scan:
    def __init__(
        self,
        opts: Dict[str, Any],
        http: httpSender,
        tag: str,
        path: str = PATH_PYTHON_MODULE,
    ):
        self.opts = opts
        self.http = http
        self.path = path
        self.tag = tag
        self.log = getLogger("scant3r")

    def open_yaml_file(self, file_name: str, add_path: bool):
        try:
            path = file_name
            if add_path == True:
                path = f"{self.path}{file_name}"
            return safe_load(open(path, "r"))
        except Exception as e:
            self.log.error(e)
            return None

    def send_request(
        self, method: str, url: str, second_url: Union[str, None] = None
    ) -> Response:
        convert_body = self.opts.get("convert_body",False)
        if method == "GET":
            return self.http.send(url, method,org=convert_body)

        if convert_body:
            params = dict(parse_qsl(urlparse(url).query))
            if second_url is not None:
                second_url = second_url.split("?")[0]
            url = url.split("?")[0]
        else:
            params = {}
        if second_url is not None:
            return self.http.send(second_url, method, body=params,org=convert_body)
        return self.http.send(url, method, body=params,org=convert_body)

    def transform_path_to_module_import(self, path: str) -> str:
        path = path.replace("/", ".").replace("\\", ".").strip()
        if path[-3:] == ".py":
            path = path[:-3]
        return path

    # simple function for out-of-band host
    def oob_host(self, key: str = None) -> dict:
        if key:  # for get resutls of host
            req = self.http.custom(
                url="https://odiss.eu:1337/events",
                headers={"Authorization": f"Secret {key}"},
            )
            return req.json()["events"][0]
        else:  # for generate a new host
            key = b64encode(token_bytes(32)).decode()
            req = self.http.custom(
                url="https://odiss.eu:1337/events",
                headers={"Authorization": f"Secret {key}"},
            )
            return {"host": req.json()["id"] + ".odiss.eu", "key": key}

    # In some module if we have a # in the url it's doesn't work
    # Clean the url
    def transform_url(self, url: str) -> str:
        parse_url = urlparse(url)
        new_url = f"{parse_url.scheme}://{parse_url.netloc}{parse_url.path}"
        if parse_url.query:
            new_url += f"?{parse_url.query}"
        return new_url

    def show_report(self, name: str, url: str, payload: str, matching: str):
        console.print(
            f"""
[bold blue]-----------------------[/bold blue] 
:fire: {name}
:dart: The Effected URL: {url}
:syringe: The Used Payload: [bold red] {payload} [/bold red]
:mag: Matched with : [bold yellow] {matching} [/bold yellow]
:file_folder: Saved: data.json
[bold blue]-----------------------[/bold blue] 
                        """
        )
