import unittest, os


class cMSHParseTest(unittest.TestCase):
    def test_3EncodingChars(self):
        #plan = hl7.create_parse_plan(sample_hl7)
        #self.assertEqual(plan.separators, [u'\r', '|', '~', '^', '&'])
        #self.assertEqual(mshData[2], actualMshResultsList[1])
        self.assertEqual('^~\\&amp;', actualMshResultsList[1])