#!/usr/bin/env python3
import importlib

def runApplication(package, app):
    try:
        # importlib allows for the import of a module based on 
        # the module's name
        module = importlib.import_module(package)
        # loop up the attribute provided -- it must be something 
        # which can be "executable"
        app = getattr(module, app)
        # This will need to have a couple of parameters eventually,
        # but for now, we'll just instantiate it.
        app();
    except Exception e:
        # 500 status is an internal server error + two newlines
        # means that this automatically creates
        print("""Status: 500\n\n""" + e.value)

