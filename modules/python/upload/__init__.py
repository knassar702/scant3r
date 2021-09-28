from core.libs import Http
from .upload import Upload


def main(opts: dict, http: Http):
    Upload(opts, http).start()
