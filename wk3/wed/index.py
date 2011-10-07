#!c:/Python32/python.exe
import view,sys,cgitb
sys.excepthook = cgitb.Hook(file = view.ErrorRenderer(),format='text')
import os,pfhttp

request = pfhttp.getRequest()
renderer = view.HTMLRenderer()
renderer.append(['Hello there, you are visiting segments', 
                 request.uri_segmnts((1,2)), 
                 'I hope you like it!'])
renderer.render()
