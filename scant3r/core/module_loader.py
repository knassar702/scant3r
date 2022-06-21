#!/usr/bin/env python3

import concurrent.futures
import importlib
import logging
from glob import glob
from os.path import isfile
from typing import Any, Dict, List, Union
from urllib.parse import urljoin

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Column

from scant3r.core.data import base_dir, console
from scant3r.core.requester import httpSender

log = logging.getLogger("scant3r")


class ModuleLoader:
    def __init__(self):
        self.started_tasks: List[Any] = []
        self.modules: Dict[str, Any] = {}
        self.scripts: Dict[str, str] = {}

    def get(self, name: str) -> Union[None, Exception]:
        for the_modfile in glob(f"{base_dir}/modules/{name}"):
            mod_init = isfile(f"{the_modfile}/__init__.py")
            if mod_init:
                import_path = f"scant3r.modules.{name}"
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
    ) -> List[Dict[str, Any]]:

        errs = 0
        report = []
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
                hosts = []
                # TO-DO: ADD THE SAME HOST NAME TO CUSTOM LIST

                for url in user_opts["urls"]:
                    opts = user_opts.copy()
                    opts["url"] = url
                    parsed_host = urljoin(url, "/")
                    if parsed_host not in hosts:
                        hosts.append(parsed_host)
                    for _, current_module in self.modules.items():
                        loaded_mod = current_module.Main(http_opts, **opts)
                        if loaded_mod.tag == "recon":
                            continue
                        log.debug(f"Trynig to Start {loaded_mod}")
                        started_threads.append(executor.submit(loaded_mod.start))
                        log.debug(f"STARTED {loaded_mod}")
                for host in hosts:
                    opts = user_opts.copy()
                    opts["url"] = host
                    for _, current_module in self.modules.items():
                        loaded_mod = current_module.Main(http_opts, **opts)
                        if loaded_mod.tag != "recon":
                            continue
                        log.debug(f"Trynig to Start {loaded_mod}")
                        started_threads.append(executor.submit(loaded_mod.start))
                        log.debug(f"STARTED {loaded_mod}")

                for future in concurrent.futures.as_completed(started_threads):
                    try:
                        future_output = future.result()
                        log.debug(f"TASK FINISHED: {future} | {future_output}")
                        try:
                            if len(future_output[list(future_output)[1]]) > 0:
                                report.append(future_output)
                        except:
                            pass
                    except Exception as e:
                        errs += 1
                        log.exception(e)
                        console.print_exception()
                        if errs >= exit_after:
                            log.debug(f"Exit because of errors counter : {errs}")
                            log.debug("Cancle all workers ...")
                            executor.shutdown(cancel_futures=True, wait=False)
                            log.debug("Exit ..")
                            exit()
                    finally:
                        progress.update(task1, advance=1)
                while not progress.finished:
                    progress.update(task1, advance=1)

        return report
