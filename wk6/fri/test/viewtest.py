if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),'..')))

import unittest
import html.parser
import view

NO_TAGS = """The rain in Spain does not normally fall on the plains despite
             the frankly overzealous beliefs of one Henry Higgins."""
             
MISMATCHED_TAGS = """<i>This first set is correct
<u>The <b>u</b> tag is not matched correctly</em></i>"""

MISSING_CLOSE_TAG = """<a style="yourmom=1">This first set is correct
<i>The <b>a</b> tag is not matched correctly</i>"""

DISALLOWED_TYPE_TAG = """<!-- comment --> comments should not be allowed"""

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
        self.assertEqual(cleaner.cleaned_data,NO_TAGS)
        
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
        
    def test_noAllowedStripsAllTags(self):
        ''' if allowed is set to an empty list, and escape is false, then there should be no tags in the output '''
        cleaner = view.HTMLCleaner(escape=False, allowed = [])
        cleaner.feed('''<div><script><b>The <a href="your mom">rain</a><!-- foo --> in <span>Spain</span></b></script></div>''')
        
        self.assertEqual(cleaner.cleaned_data.strip(), '''The rain in Spain''')
        
    def test_overallResultNonStrictNonEscape(self):
        ''' Overall result matches as expected '''
        cleaner = view.HTMLCleaner(False,False)
        cleaner.feed('''
        <div><script><b>The <a href="your mom">rain</a><!-- foo --> in <span>Spain</span></b></script></div>
        ''')
        
        self.assertEqual(cleaner.cleaned_data.strip(), '''<b>The <a href="your mom">rain</a> in Spain</b>''')
        
    def test_overallResultNonStrictEscape(self):
        ''' Overall result matches as expected while escaping'''
        cleaner = view.HTMLCleaner()
        cleaner.feed('''
        <div><script><b>The <a href="your mom">rain</a><!-- foo --> in <span>Spain</span></b></script></div>
        ''')
        
        self.assertEqual(cleaner.cleaned_data.strip(), '''&lt;div&gt;&lt;script&gt;<b>The <a href="your mom">rain</a> in &lt;span&gt;Spain&lt;/span&gt;</b>&lt;/script&gt;&lt;/div&gt;''')
if __name__ == '__main__':
    unittest.main()
