import os

from core.args import Args
from core.module_loader import ModuleLoader
from core.requester import httpSender
from core.banner import display_banner

class Scantr:
    def __init__(self):
        self.options = Args().get_args()
        self.http = httpSender(self.options)

    def get_urls(self):
        if os.isatty(0):
            pass

    def start(self):
        display_banner(*["424",":snake: 42"])
        mod_loader = ModuleLoader()
        for module in self.options["modules"]:
            mod_loader.get(module)
            mod_loader.run(
                self.options,
                self.http,
                self.options["threads"],
                self.options["exit_after"],
            )
