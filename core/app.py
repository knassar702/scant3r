from core.args import Args
from core.module_loader import ModuleLoader
from core.requester import httpSender


class Scantr:
    def __init__(self):
        self.options = Args().get_args()
        self.http = httpSender(self.options)

    def start(self):
        mod_loader = ModuleLoader()
        for module in self.options["modules"]:
            mod_loader.get(module)
            mod_loader.run(self.options, self.http)
