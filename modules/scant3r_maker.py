#!/usr/bin/env python3
import importlib
import sys

class ImportModule:
    def Get(name):
        name = f'modules.{name}'
        try:
            c = importlib.import_module(name)
            return c
        except Exception as e:
            print(e)
            sys.exit()
def module_process(module,all_options):
    try:
        c = ImportModule.Get(module)
        c.run(all_options)
    finally:
        pass
