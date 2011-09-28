#!/usr/bin/env python3

import view
        
renderer = view.BasicRenderer(body=["hello world"])
renderer.setHeader("Content-type", "text")
renderer.setHeader("Content-Language", "en")
renderer.append("I am adding a line")
renderer.render()
