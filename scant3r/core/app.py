import json
import os
import sys

from scant3r.core.args import Args
from scant3r.core.banner import display_banner
from scant3r.core.data import console
from scant3r.core.module_loader import ModuleLoader
from scant3r.core.requester import httpSender


class Scantr:
    def __init__(self):
        self.options = Args().get_args()
        self.http = httpSender(self.options)

    def get_urls(self):
        if len(self.options.get("urls", [])) == 0:
            if self.options.get("url") != "":
                self.options["urls"].append(self.options.get("url"))
            else:
                if os.isatty(0):
                    console.print(
                        "[bold red][-][/bold red] PIPE is empty, you need to use [bold yellow]-l[/bold yellow] option"
                    )
                    console.print("[bold cyan][!][/bold cyan] Exit ...")
                    exit()
                for url in sys.stdin:
                    url = url.rstrip()
                    self.options.get("urls").append(url)

    def start(self, save_output: bool = True):
        display_banner(*[])
        self.get_urls()
        mod_loader = ModuleLoader()
        for module in self.options["modules"]:
            mod_loader.get(module)
        the_output = mod_loader.run(
            self.options,
            self.http,
            self.options["threads"],
            self.options["exit_after"],
        )

        if save_output:
            if self.options.get("output"):
                output_file = open(self.options.get("output"), "w")
                if output_file.writable():
                    output_file.write(json.dumps(the_output))
                    output_file.close()
                else:
                    console.print(
                        "[/bold red][-][/bold red] File is not writable, please check your permission, Exit .."
                    )
                    exit()
