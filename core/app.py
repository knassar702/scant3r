import os
import sys

from core.args import Args
from core.banner import display_banner
from core.data import console
from core.module_loader import ModuleLoader
from core.requester import httpSender


class Scantr:
    def __init__(self):
        self.options = Args().get_args()
        self.http = httpSender(self.options)

    def get_urls(self):
        if len(self.options.get("urls", [])) == 0:
            if os.isatty(0):
                console.print(
                    "[bold red][-][/bold red] PIPE is empty, you need to use [bold yellow]-l[/bold yellow] option"
                )
                console.print("[bold cyan][!][/bold cyan] Exit ...")
                exit()
            for url in sys.stdin:
                url = url.rstrip()
                self.options.get("urls").append(url)

    def start(self):
        display_banner(*[])
        self.get_urls()
        mod_loader = ModuleLoader()
        for module in self.options["modules"]:
            mod_loader.get(module)
        mod_loader.run(
            self.options,
            self.http,
            self.options["threads"],
            self.options["exit_after"],
        )
