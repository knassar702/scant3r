#!/usr/bin/env python3

import concurrent.futures
import importlib
import logging
from glob import glob
from os.path import isfile
from typing import Any, Dict, List

from core.data import base_dir
from core.requester import httpSender

log = logging.getLogger("scant3r")


class ModuleLoader:
    def __init__(self):
        self.started_tasks: List[Any] = []
        self.modules: Dict[str, Any] = {}
        self.scripts: Dict[str, str] = {}

    def get(self, name: str):
        for the_modfile in glob(f"{base_dir}/modules/python/{name}"):
            mod_init = isfile(f"{the_modfile}/__init__.py")
            if mod_init:
                import_path = f"modules.python.{name}"
                try:
                    import_obj = importlib.import_module(import_path)
                    self.modules[name] = import_obj
                except Exception as err:
                    print(err)
                    return err

    def run(
        self, user_opts: Dict[str, Any], http_opts: httpSender, max_workers: int = 10
    ):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            started_threads: List[Any] = []
            # TO-DO: ADD THE SAME HOST NAME TO CUSTOM LIST
            user_opts["urls"] = ["http://google.com/?test=2"]
            for url in user_opts["urls"]:
                opts = user_opts.copy()
                opts["url"] = url
                for _, current_module in self.modules.items():
                    loaded_mod = current_module.Main(opts, http_opts)
                    started_threads.append(
                        executor.submit(loaded_mod.start(), opts, http_opts)
                    )
            for future in concurrent.futures.as_completed(started_threads):
                try:
                    print(future)
                except Exception as err:
                    print(f" BRUHH ERROR : {err}")
