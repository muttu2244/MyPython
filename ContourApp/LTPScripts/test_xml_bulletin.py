import os,sys
from BaseAPI import Utility
util = Utility()
string_xml = util.open_xml("AppHelpLTP2.xml")
actual_text = util.get_text_from_xml(string_xml, "Reports", "trans-unit", "english")
for i in actual_text:
    actual_text2 = []
    for str1 in actual_text:
        if "<br>" in str1:
            str_li = str1.split("<br>")
            for i in str_li:
                actual_text2.append(i)
        else:
            actual_text2.append(str1)
for i in actual_text2:
    print " befor   --" +i
    act = util.parse_html_tag(i.strip())
    print"after --------- "+ act

