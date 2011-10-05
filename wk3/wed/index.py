#!/usr/bin/env python3
import view,os,pfhttp,cgitb
cgitb.enable()

request = pfhttp.getRequest()
renderer = view.HTMLRenderer()
renderer.append(['Hello there, you are visiting segments', 
                 request.uri_segments((1,2)), 
                 'I hope you like it!'])
renderer.render()
