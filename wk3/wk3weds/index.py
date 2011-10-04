#!/usr/bin/env python3
import view,os

renderer = view.HTMLRenderer()
renderer.append(['Hello there, you are visiting ', request.path, ' I hope you like it!])
renderer.render()
