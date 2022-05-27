#!/usr/bin/env python3

import concurrent.futures
import importlib
import logging
import time
from glob import glob
from os.path import isfile
from typing import Any, Dict, List

from rich.progress import BarColumn, Progress, SpinnerColumn

from core.data import base_dir, console
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
                    return err

    def run(
        self,
        user_opts: Dict[str, Any],
        http_opts: httpSender,
        max_workers: int = 10,
        exit_after: int = 500,
    ):

        errs = 0
        with Progress(
            "{task.description}", SpinnerColumn(), BarColumn(), console=console
        ) as progress:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                started_threads: List[Any] = []
                # TO-DO: ADD THE SAME HOST NAME TO CUSTOM LIST
                task1 = progress.add_task(
                    "[green] Scanning ...",
                    total=len(user_opts["urls"] * len(self.modules.keys())),
                )
                for url in user_opts["urls"]:
                    opts = user_opts.copy()
                    opts["url"] = url
                    for _, current_module in self.modules.items():
                        loaded_mod = current_module.Main(opts, http_opts)
                        started_threads.append(
                            executor.submit(loaded_mod.start(), opts, http_opts)
                        )
                for _ in concurrent.futures.as_completed(started_threads):
                    try:
                        progress.update(task1, advance=1)
                        time.sleep(2)
                    except:
                        errs += 1
                        console.print_exception()
                        if errs >= exit_after:
                            exit()
