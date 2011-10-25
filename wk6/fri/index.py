#!/usr/bin/env python3
import view,cgitb,sys
sys.excepthook = cgitb.Hook(file = view.ErrorRenderer(),format='text')
import app
