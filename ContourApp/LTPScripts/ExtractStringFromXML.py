import xml.etree.ElementTree as ET
import os
import re
def extractid_from_xml(file):
    objList = list()
    tree = ET.parse(file)
    root = tree.getroot()

    for node in root.findall(".//trans-unit"):
        objList.append(node.attrib['id'])
    # print objList
    return objList
def parse_xmls(file, system_map):
    tree = ET.parse(file)
    root = tree.getroot()
    id = ""
    country = ""
    id_target = {}
    objList = extractid_from_xml(system_map)
    # print objList
    for child in root.findall(".//trans-unit"):
        try:
            id = child.attrib['id']
            country = child.find("target").text
        except:
            "  "
        if id and country:
            # print id,country
            # print id
            if id in objList:
                id_target[id] = country
    return id_target
def dutch_value():
    if id in dutch.keys():
        dutch1 = dutch.get(id)
        return dutch1
def english_value():
    if id in english.keys():
        english1 = english.get(id)
        return english1

def french_value():
    if id in french.keys():
        french1 = french.get(id)
        return french1
def german_value():
    if id in german.keys():
        german1 = german.get(id)
        return german1
def italian_value():
    if id in italian.keys():
        italian1 = italian.get(id)
        return italian1
def polish_value():
    if id in polish.keys():
        polish1 = italian.get(id)
        return polish1
def serbian_value():
    if id in serbian.keys():
        serbian1 = serbian.get(id)
        return serbian1
def spanish_value():
    if id in spanish.keys():
        spanish1 = spanish.get(id)
        return spanish1
def turkish_value():
    if id in turkish.keys():
        turkish1 = turkish.get(id)
        return turkish1
def final_xml_string(tree):
    global final_xml
    final_xml.append(tree)
def dump1(id1):
    id = ET.Element(id1)
    english = ET.SubElement(id, "english")
    english.text = english_value()
    # dutch = ET.SubElement(id, 'dutch')
    # dutch.text = dutch_value()
    # french = ET.SubElement(id, 'french')
    # french.text = french_value()
    german = ET.SubElement(id, 'german')
    german.text = german_value()
    # italian = ET.SubElement(id, 'italian')
    # italian.text = italian_value()
    # polish = ET.SubElement(id, 'polish')
    # polish.text = polish_value()
    # serbian = ET.SubElement(id, 'serbian')
    # serbian.text = serbian_value()
    # spanish = ET.SubElement(id, 'spanish')
    # spanish.text = spanish_value()
    # turkish = ET.SubElement(id, 'turkish')
    # turkish.text = turkish_value()
    # ET.dump(id)
    # final_xml.ET.SubElement(id)
    print "Processing String ID" + id1
    final_xml_string(id)
system_map = 'C:\Users\U0065170\Desktop\LTP Scripts WIth Config_feb-23\LTP_Updated_German_14-3-2017\AppHelpLTP2.xml'
name_string = system_map.split('\\')
file_name = name_string[len(name_string) - 1].split(".")[0]
path = "D:\\LTP-2.0\\file\\"
filelist = os.listdir(path)
final_xml = ET.Element("root")
english = {}
dutch = {}
german = {}
french = {}
italian = {}
polish = {}
serbian = {}
turkish = {}
spanish = {}

for file1 in filelist:
    print "Parsing %s Master String Table" % (file1)
    if file1 == "Dutch.xml":
        dutch = parse_xmls(path + file1, system_map)
    elif file1 == "English.xml":
        english = parse_xmls(path + file1, system_map)
    elif file1 == "French.xml":
        french = parse_xmls(path + file1, system_map)
    elif file1 == "German.xml":
        german = parse_xmls(path + file1, system_map)
    elif file1 == "Italian.xml":
        italian = parse_xmls(path + file1, system_map)
    elif file1 == "polish.xml":
        polish = parse_xmls(path + file1, system_map)
    elif file1 == "Serbian.xml":
        serbian = parse_xmls(path + file1, system_map)
    elif file1 == "Spanish.xml":
        spanish = parse_xmls(path + file1, system_map)
    elif file1 == "Turkish.xml":
        turkish = parse_xmls(path + file1, system_map)
    else:
        print "No match"
objList = extractid_from_xml(system_map)
print "Total Number of strings ", len(objList)
print dutch
print len(english)
print english
for id in objList:
    dump1(id)
ET.dump(final_xml)
tree = ET.ElementTree(final_xml)
tree.write("C:\\Users\\U0065170\\Desktop\\LTP Scripts WIth Config_feb-23\\converted Strings\\" + file_name + "String.xml")
