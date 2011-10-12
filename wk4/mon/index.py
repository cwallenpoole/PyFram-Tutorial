#!c:/Python32/python.exe
import view,cgitb,sys
sys.excepthook = cgitb.Hook(file = view.ErrorRenderer(),format='text')
import app
