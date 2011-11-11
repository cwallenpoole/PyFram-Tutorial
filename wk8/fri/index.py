#!c:\Python32\python.exe
import view.renderer,cgitb,sys
sys.excepthook = cgitb.Hook(file = view.renderer.ErrorRenderer(),format='text')
import app
