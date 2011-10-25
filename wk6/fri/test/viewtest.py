if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),'..')))

import unittest
import html.parser
import view

NO_TAGS = """The rain in Spain does not normally fall on the plains despite
             the frankly overzealous beliefs of one Henry Higgins."""
             
MISMATCHED_TAGS = """<p>This first set is correct
<div>The <b>div</b> tag is not matched correctly</span></p>"""

MISSING_CLOSE_TAG = """<p style="yourmom=1">This first set is correct
<div>The <b>p</b> tag is not matched correctly</div>"""

class TestHTMLCleaner(unittest.TestCase):

    def test_basicStringSetsSource(self):
        ''' make sure source works if there are no tags '''
        cleaner = view.HTMLCleaner()
        cleaner.feed(NO_TAGS)
        self.assertEqual(cleaner.source,NO_TAGS)
        
    def test_basicStringSetsResult(self):
        ''' make sure result works if there are no tags '''
        cleaner = view.HTMLCleaner()
        cleaner.feed(NO_TAGS)
        self.assertEqual(cleaner.result,NO_TAGS)
        
    def test_mismatchedTagsCausesErrorInStrictMode(self):
        ''' make sure mismatched tags causes error in strict mode '''
        cleaner = view.HTMLCleaner(True)
        self.assertRaises(html.parser.HTMLParseError,cleaner.feed,MISMATCHED_TAGS)        
        
    def test_mismatchedTagsDoesNotCauseErrorInNonStrictMode(self):
        ''' make sure mismatched tags does not cause error outside of strict mode '''
        cleaner = view.HTMLCleaner(False)
        cleaner.feed(MISMATCHED_TAGS)
        # if we've gotten here, simply pass something.
        self.assertTrue(1)
        
    def test_missingClosingCausesErrorInStrictMode(self):
        ''' make sure missing end tags causes error in strict mode '''
        cleaner = view.HTMLCleaner(True)
        self.assertRaises(html.parser.HTMLParseError,cleaner.feed,MISSING_CLOSE_TAG)        
        
    def test_missingClosingDoesNotCauseErrorInNonStrictMode(self):
        ''' make sure missing end tags does not cause error outside of strict mode '''
        cleaner = view.HTMLCleaner(False)
        cleaner.feed(MISSING_CLOSE_TAG)
        # if we've gotten here, simply pass something.
        self.assertTrue(1)     
        
   
if __name__ == '__main__':
    unittest.main()
