import xml.etree.ElementTree as ET
import os
import re

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

objList = list()
tree = ET.parse('TargetRangesLTPenglish.xml')
root = tree.getroot()

for node in root.findall(".//trans-unit"):

    objList.append(node.attrib['id'])
print len(objList)

english = dict()
dutch = dict()
french = dict()
german = dict()
italian = dict()
polish = dict()
serbian = dict()
spanish = dict()
turkish = dict()
path="D:\\project\\2.x\\Language Xmls\\test_lang\\"
filelist = os.listdir("D:\\project\\2.x\\Language Xmls\\test_lang\\")
for file1 in filelist:
#file1 = "D:\\project\\2.x\\Language Xmls\\DutchMasterStringTable.xml"
    print file1
    data = open(path+file1, "r")
    l = []
    s = ''
    for line in data.readlines():
        l.append(line)
    s = '\n'.join(l)

    a1=s.split("</trans-unit>")


    ele = dict()
    print a1[len(a1)-1]
    for i in range(len(a1)):
        cleanr = re.compile('id=.*>')

        if cleanr:
            cleaned_text = re.search(cleanr,  a1[i])

            if cleaned_text is None:
                continue
            id=cleaned_text.group(0).split("=\"")[1].split("\">")[0]
        tarcleaner = re.compile('<target>.*<\/target>')
        if tarcleaner:
            cleaned_text = re.search(tarcleaner,  a1[i])
            if cleaned_text is None:
                continue
            target=cleaned_text.group(0).split("<target>")[1].split("</target>")[0]
        ele[id]=target
    print len(ele)
    #final_dict = {}
    for k,v in ele.items():
        if k in objList:
            if file1 == "Dutch.xml":
                newdict = {}
                newdict["dutch"]=v
                dutch[k]=newdict
            elif file1 == "English.xml":
                newdict = {}
                newdict["english"]=v
                english[k]=v
            elif file1 == "French.xml":
                french[k]=v
            elif file1 == "German.xml":
                german[k]=v
            elif file1 == "Italian.xml":
                italian[k]=v
            elif file1 == "polish.xml":
                polish[k]=v
            elif file1 == "Serbian.xml":
                serbian[k]=v
            elif file1 == "Spanish.xml":
                spanish[k]=v
            elif file1 == "Turkish.xml":
                turkish[k]=v
            else:
                print "No match"
print "dutch:",dutch
print "english:", len(english)

reduce(merge, [dutch, english])
print dutch

