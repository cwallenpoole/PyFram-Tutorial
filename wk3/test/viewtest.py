if __name__ == '__main__':
    import sys
    import os
    # make sure the parent directory is in sys.path
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),'..')))

import unittest
import view
class Appender:
    ''' merely creates a list of everything which is sent to its append method '''
    def __init__(self):
        self.body = []
    
    def append(self, line):
        ''' all this method does is collect the lines '''
        self.body.append(str(line))

class TestBasicRenderer(unittest.TestCase):
    def test_noHeaderNoBody(self):
        ''' make sure everything works if there is no input '''
        appender = Appender()
        render = view.BasicRenderer(output=appender.append)
        render.render()
        self.assertEqual(appender.body,[''])
    
    def test_headerNoBody(self):
        ''' make sure everything works if there is no body but a header '''
        appender = Appender()
        render = view.BasicRenderer(headers={'foo':'bar', 'baz':'bat'}, output=appender.append)
        render.render()
        self.assertEqual(appender.body,['foo: bar', 'baz: bat', ''])
        
    def test_bodyNoHeader(self):
        ''' make sure everything works if there is no header but a body '''
        appender = Appender()
        render = view.BasicRenderer(body=[1,2,3], output=appender.append)
        render.render()
        self.assertEqual(appender.body,['', '1', '2', '3'])
        
    def test_headerAndBody(self):
        ''' make sure everything works if there is both a header and body '''
        appender = Appender()
        render = view.BasicRenderer(headers={'foo':'bar', 'baz':'bat'},body=[1,2,3], output=appender.append)
        render.render()
        self.assertEqual(appender.body,['foo: bar', 'baz: bat', '', '1', '2', '3'])
        
if __name__ == '__main__':
    unittest.main()
