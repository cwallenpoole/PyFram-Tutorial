#!/usr/bin/env python3
import view,os

renderer = view.BasicRenderer()
if os.environ["REQUEST_URI"].endswith(".svg"):
    renderer.setHeader("Content-Type", "image/svg+xml")
    renderer.append('''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <circle cx="100" cy="50" r="40" stroke="black"
  stroke-width="2" fill="red" />
</svg>''')
else:
    renderer.setHeader("Content-Type", "text/html")
    if os.environ["REQUEST_URI"].endswith("/"):
        renderer.append('''
<html><body><img src="http://localhost/pyftut/wk3/test.svg" /></body></html>
''')
renderer.render()
