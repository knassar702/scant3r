#!/usr/bin/env python3

import concurrent.futures
import importlib
import logging
from glob import glob
from os.path import isfile
from typing import Any, Dict, List, Union

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Column

from core.data import base_dir, console
from core.requester import httpSender

log = logging.getLogger("scant3r")


class ModuleLoader:
    def __init__(self):
        self.started_tasks: List[Any] = []
        self.modules: Dict[str, Any] = {}
        self.scripts: Dict[str, str] = {}

    def get(self, name: str) -> Union[None, Exception]:
        for the_modfile in glob(f"{base_dir}/modules/python/{name}"):
            mod_init = isfile(f"{the_modfile}/__init__.py")
            if mod_init:
                import_path = f"modules.python.{name}"
                try:
                    log.debug(f"trying to load {import_path}")
                    import_obj = importlib.import_module(import_path)
                    log.debug("LOADED")
                    self.modules[name] = import_obj
                except Exception as err:
                    log.exception(err)
                    return err

    def run(
        self,
        user_opts: Dict[str, Any],
        http_opts: httpSender,
        max_workers: int = 50,
        exit_after: int = 500,
    ):

        errs = 0
        with Progress(
            TextColumn(
                "[progress.percentage] Scanning {task.completed}/{task.total} | {task.percentage:>3.0f}% ",
                table_column=Column(ratio=1),
            ),
            BarColumn(bar_width=50, table_column=Column(ratio=2)),
            SpinnerColumn(),
            console=console,
        ) as progress:
            pb_counter = len(user_opts["urls"] * len(self.modules.keys()))
            task1 = progress.add_task("[green] Scanning ...", total=pb_counter)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                started_threads: List[Any] = []
                # TO-DO: ADD THE SAME HOST NAME TO CUSTOM LIST

                for url in user_opts["urls"]:
                    opts = user_opts.copy()
                    opts["url"] = url
                    for _, current_module in self.modules.items():
                        loaded_mod = current_module.Main(opts, http_opts)
                        log.debug(f"Trynig to Start {loaded_mod}")
                        started_threads.append(executor.submit(loaded_mod.start))
                        log.debug(f"STARTED {loaded_mod}")
                for _ in concurrent.futures.as_completed(started_threads):
                    try:
                        log.debug("UPATED ")
                        # out_except = out.exception()
                        # console.print(out_except)
                    except Exception as e:
                        errs += 1
                        log.exception(e)
                        console.print_exception()
                        if errs >= exit_after:
                            log.debug(f"Exit because of errors counter : {errs}")
                            exit()
                    finally:
                        progress.update(task1, advance=1)
