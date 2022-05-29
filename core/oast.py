import json
import random
from base64 import b64decode, b64encode
from secrets import token_bytes
from uuid import uuid4

import requests
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from core.data import INTERACT_SERVERS

requests.packages.urllib3.disable_warnings()  # ignore ssl warning messages


class Interactsh:
    def __init__(self, token="", server=""):
        rsa = RSA.generate(2048)
        self.public_key = rsa.publickey().exportKey()
        self.private_key = rsa.exportKey()
        self.token = token
        self.server = server.lstrip(".") or random.choice(INTERACT_SERVERS)
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            self.headers["Authorization"] = self.token
        self.secret = str(uuid4())
        self.encoded = b64encode(self.public_key).decode("utf8")
        guid = uuid4().hex.ljust(33, "a")
        guid = "".join(
            i if i.isdigit() else chr(ord(i) + random.randint(0, 20)) for i in guid
        )
        self.domain = f"{guid}.{self.server}"
        self.correlation_id = self.domain[:20]
        self.session = requests.session()
        self.session.headers = self.headers
        self.session.verify = False
        self.register()

    def register(self):
        data = {
            "public-key": self.encoded,
            "secret-key": self.secret,
            "correlation-id": self.correlation_id,
        }
        res = self.session.post(
            f"https://{self.server}/register",
            headers=self.headers,
            json=data,
            timeout=30,
        )
        if "success" not in res.text:
            raise Exception("Can not initiate interact.sh DNS callback client")

    def pull_logs(self):
        result = []
        url = (
            f"https://{self.server}/poll?id={self.correlation_id}&secret={self.secret}"
        )
        res = self.session.get(url, headers=self.headers, timeout=30).json()
        aes_key, data_list = res["aes_key"], res["data"]
        for i in data_list:
            decrypt_data = self.__decrypt_data(aes_key, i)
            result.append(self.__parse_log(decrypt_data))
        return result

    def __decrypt_data(self, aes_key, data):
        private_key = RSA.importKey(self.private_key)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        aes_plain_key = cipher.decrypt(b64decode(aes_key))
        decode = b64decode(data)
        bs = AES.block_size
        iv = decode[:bs]
        cryptor = AES.new(key=aes_plain_key, mode=AES.MODE_CFB, IV=iv, segment_size=128)
        plain_text = cryptor.decrypt(decode)
        return json.loads(plain_text[16:])

    def __parse_log(self, log_entry):
        new_log_entry = {
            "timestamp": log_entry["timestamp"],
            "host": f'{log_entry["full-id"]}.{self.domain}',
            "remote_address": log_entry["remote-address"],
        }
        return new_log_entry


class Odiss:
    def __init__(self, http):
        self.http = http
        self.last_results = []
        self.key = ""
        self.host = ""

    def poll(self, _all=False) -> list:
        req = self.http.custom(
            url="https://odiss.eu:1337/events",
            headers={"Authorization": f"Secret {self.key}"},
        )
        if len(req.json()["events"]) != self.last_results:
            self.last_results = len(req.json()["events"])
            return self.last_results
        if _all:
            return self.last_results

        return []

    def new(self) -> str:
        self.key = b64encode(token_bytes(32)).decode()
        req = self.http.custom(
            url="https://odiss.eu:1337/events",
            headers={"Authorization": f"Secret {self.key}"},
        )
        self.host = req.json()["id"] + ".odiss.eu"
        return self.host
