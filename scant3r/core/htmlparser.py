from enum import Enum
from html.parser import HTMLParser


class HTMLMatch(Enum):
    TAG_NAME = "tagname"
    EndTag = "endtag"
    AttrName = "attrname"
    AttrValue = "attrvalue"
    Comment = "comment"
    Text = "text"


class HTMLocation(HTMLParser):
    def __init__(self, pattern: str):
        super().__init__()
        self.data = []
        self.pattern = pattern

    def handle_starttag(self, tag, attrs):
        if self.pattern in tag:
            self.data.append(HTMLMatch.TAG_NAME)
        for attr in attrs:
            if self.pattern in attr[0]:
                self.data.append(HTMLMatch.AttrName)
            if attr[1] is not None:
                if self.pattern in attr[1]:
                    self.data.append(HTMLMatch.AttrValue)

    def handle_data(self, data):
        if self.pattern in data:
            self.data.append(HTMLMatch.Text)

    def handle_comment(self, data):
        if self.pattern in data:
            self.data.append(HTMLMatch.Comment)

    def handle_endtag(self, tag):
        if self.pattern in tag:
            self.data.append(HTMLMatch.EndTag)


class HTMLForXpath(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = "//"

    def handle_starttag(self, tag, attrs):
        self.data += tag
        for attr in attrs:
            if attr[1] is None:
                self.data += "[@{}]".format(attr[0])
            elif attr[0] is None:
                self.data += "[{}]".format(attr[1])
            else:
                self.data += '[@{}="{}"]'.format(attr[0], attr[1].replace('"', ""))
