if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),'..')))

import unittest
import view
class Appender:
    def __init__(self):
        self.body = []
    
    def append(self, line):
        self.body.append(str(line))

class TestBasicRenderer(unittest.TestCase):
    def test_headerNoBody(self):
        appender = Appender()
        render = view.BasicRenderer(headers={'foo':'bar', 'baz':'bat'}, output=appender.append)
        render.render()
        self.assertEqual(appender.body,['foo: bar', 'baz: bat'])
    
    def test_bodyNoHeader(self):
        appender = Appender()
        render = view.BasicRenderer(body=[1,2,3], output=appender.append)
        render.render()
        self.assertEqual(appender.body,['', '1', '2', '3'])
        
    def test_headerAndBody(self):
        appender = Appender()
        render = view.BasicRenderer(headers={'foo':'bar', 'baz':'bat'},body=[1,2,3], output=appender.append)
        render.render()
        self.assertEqual(appender.body,['foo: bar', 'baz: bat', '', '1', '2', '3'])
        
if __name__ == '__main__':
    unittest.main()
