
import os,shutil
import xml.etree.ElementTree as ET
tree = ET.parse('ContourTestSuite.xml')
root = tree.getroot()
print root

'''def empty_dir():
    head, tail = os.path.split(os.getcwd())
    print head
    report_dir = os.path.join(head, "Reports")
    print report_dir
    for file_object in os.listdir(report_dir):
        file_object_path = os.path.join(report_dir, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)'''

def readXML(root, element,subElement=None):
    objList = list()
    #index = 0
    for node in root.findall(element):
        #for j in node.findall(subElement):
        element = dict()
        element['name'] = node.find('name').text.strip()
        element['status'] = node.find('status').text.strip()
        #objList[].append('zone', j.find('zone').text.strip())
        objList.append(element)
    return objList
'''def rename_dir(scripts):
    head, tail = os.path.split(os.getcwd())
    report_dir = os.path.join(head, "Reports")
    dir_list=os.listdir(report_dir)
    i=0
    pass
    for dir in dir_list:
        print dir,scripts[i]['name']
        os.rename("hi"+str(i),os.path.join(report_dir,dir))
        i+=1'''''

scripts=readXML(root,"Script")
print scripts
#result=os.system(scripts[0]['name'])
# print result
print len(scripts)
for index in range(len(scripts)):
    if scripts[index]['status']=='fail':
        print("Running Script is :"+scripts[index]['name'])
        if os.system(scripts[index]['name'])==True:
            scripts[index]['status']='pass'
