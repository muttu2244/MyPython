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
def get_string_value(lang, id):
    """This function returns corresponding string value using string ID
    :param lang:
    :param id:
    :return: Value
    """
    if id in lang.keys():
        return lang.get(id)

def final_xml_string(tree):
    global final_xml
    final_xml.append(tree)
def dump1(id1):
    id = ET.Element(id1)
    croatian =ET.SubElement(id, "croatian")
    croatian.text = get_string_value(croatian_di, id1)
    danish =ET.SubElement(id, "danish")
    danish.text = get_string_value(danish_di, id1)
    dutch =ET.SubElement(id, "dutch")
    dutch.text = get_string_value(dutch_di, id1)
    english = ET.SubElement(id, "english")
    english.text = get_string_value(english_di, id1)
    finnish = ET.SubElement(id, "finnish")
    finnish.text = get_string_value(finnish_di, id1)
    french = ET.SubElement(id, "french")
    french.text = get_string_value(french_di, id1)
    german = ET.SubElement(id, "german")
    german.text = get_string_value(german_di, id1)
    greek = ET.SubElement(id, "greek")
    greek.text = get_string_value(greek_di, id1)
    italian = ET.SubElement(id, "italian")
    italian.text = get_string_value(italian_di, id1)
    norwegian = ET.SubElement(id, "norwegian")
    norwegian.text = get_string_value(norwegian_di, id1)
    polish = ET.SubElement(id, "polish")
    polish.text = get_string_value(polish_di, id1)
    portugal = ET.SubElement(id, "portugal")
    portugal.text = get_string_value(portugal_di, id1)
    slovenian = ET.SubElement(id, "slovenian")
    slovenian.text = get_string_value(slovenian_di, id1)
    spanish = ET.SubElement(id, "spanish")
    spanish.text = get_string_value(spanish_di, id1)
    swedish = ET.SubElement(id, "swedish")
    swedish.text = get_string_value(swedish_di, id1)
    print "Processing String ID" + id1
    final_xml_string(id)
system_map = 'D:\LTP-2.0\LTPScripts_14_languages\LTPscripts\EditEntryLTP.xml'
# Please provide the complete path of the xml as reference document for corresponing feature
name_string = system_map.split('\\')
file_name = name_string[len(name_string) - 1].split(".")[0]
path = "D:\\LTP-2.0\\14-Languages\\"
# please provide the complete path for all 14 langauges . Rename each file with corresponding  specified name
filelist = os.listdir(path)
final_xml = ET.Element("root")
croatian_di = {}
danish_di = {}
dutch_di = {}
english_di = {}
finnish_di = {}
french_di = {}
german_di = {}
greek_di = {}
italian_di = {}
norwegian_di = {}
polish_di = {}
portugal_di = {}
slovenian_di = {}
spanish_di = {}
swedish_di = {}

for file1 in filelist:
    print "Parsing %s Master String Table" % (file1)
    if file1 == "Croatian.xml":
        croatian_di = parse_xmls(path + file1, system_map)
    elif file1 == "Danish.xml":
        danish_di = parse_xmls(path + file1, system_map)
    elif file1 == "Dutch.xml":
        dutch_di = parse_xmls(path + file1, system_map)
    elif file1 == "English.xml":
        english_di = parse_xmls(path + file1, system_map)
    elif file1 == "Finnish.xml":
        finnish_di = parse_xmls(path + file1, system_map)
    elif file1 == "French.xml":
        french_di = parse_xmls(path + file1, system_map)
    elif file1 == "German.xml":
        german_di = parse_xmls(path + file1, system_map)
    elif file1 == "Greek.xml":
        greek_di = parse_xmls(path + file1, system_map)
    elif file1 == "Italian.xml":
        italian_di = parse_xmls(path + file1, system_map)
    elif file1 == "Norwegian.xml":
        norwegian_di = parse_xmls(path + file1, system_map)
    elif file1 == "Polish.xml":
        polish_di = parse_xmls(path + file1, system_map)
    elif file1 == "Portugal.xml":
        portugal_di = parse_xmls(path + file1, system_map)
    elif file1 == "Slovenian.xml":
        slovenian_di = parse_xmls(path + file1, system_map)
    elif file1 == "Spanish.xml":
        spanish_di = parse_xmls(path + file1, system_map)
    elif file1 == "Swedish.xml":
        swedish_di = parse_xmls(path + file1, system_map)
    else:
        print "No match"
objList = extractid_from_xml(system_map)
print "Total Number of strings ", len(objList)
for id in objList:
    dump1(id)
ET.dump(final_xml)
tree = ET.ElementTree(final_xml)
dest_path = "D:\\LTP-2.0\\LTP_suite_integrated_ios_5_aprl\\extracted strings\\" + file_name + "String.xml"
# please provide the complete path for destination path to be saved
tree.write(dest_path)
print "File Available at the location: "+ dest_path
